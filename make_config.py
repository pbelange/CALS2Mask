import numpy as np
import pandas as pd
from ruamel.yaml import YAML


import Backend.Parser as parser
import Backend.Spark as spark



#=============================================
# SPECIFYING TIMESTAMP TO EXTRACT
#=============================================
snapshot_ts = '2022-07-23 19:30'
    
    
#=============================================
# FINDING CORRESPONDING FILL
#=============================================
# Initiating spark session
sparkspace  = spark.SparkSession()

# Finding fill info:
_start = str(pd.Timestamp(snapshot_ts)-pd.Timedelta(seconds = 24*3600))
_stop  = str(pd.Timestamp(snapshot_ts)+pd.Timedelta(seconds = 24*3600))

_var   = "HX:FILLN"
_df    = sparkspace.query(_var,_start,_stop)
_fillparser = parser.Parser(_df)
_fillparser.obs_timestamp(snapshot_ts)

fill_start,FILLN = _fillparser.get_previous(_var,returnTS=True)
fill_stop ,_     = _fillparser.get_next(_var,returnTS=True)


#=============================================
# EXTRACTING DATA FROM NXCALS
#=============================================

# Extracting main DataFrame for the config
allvars = _fillparser.get_varList()

data_list = []
for _var in list(set(allvars)):
    data_list.append(sparkspace.query(_var,fill_start,fill_stop))
data_df = pd.concat(data_list,axis=1)   


#=============================================
# CREATING YAML FILE FOR BOTH BEAM
#=============================================
mainParser = parser.Parser(data_df)
mainParser.obs_timestamp(snapshot_ts)

for beam in ['B1','B2']:
    #selecting beam
    mainParser.obs_beam(beam)

    # loading template
    yaml = YAML()
    with open('Backend/config_template.yaml','r') as yamlfile:
        config = yaml.load(yamlfile)    

    # updating values
    newConfig = mainParser.update_config(config)

    # saving to new file
    format_ts = pd.Timestamp(snapshot_ts).strftime('%Y%m%d_%H%M')
    with open(f'config_{format_ts}_{beam}.yaml','w') as yamlfile:
        yaml.dump(newConfig,yamlfile)

        
        
        
