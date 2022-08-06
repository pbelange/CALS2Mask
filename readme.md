# CALS2Mask

## About
The main tools of this package are found in `Backend/Parser.py` and `Backend/Spark.py`. To generate a `config` file to be used with `lhcmask`, one can modify the `snapshot_ts` in `/make_config.py` and run the script. `config` files for both B1 and B2 will be generated for the chosen timestamp.

The template used for the config file is found in `Backend/config_template.yaml`. The values to be replaced have been manually initialized to `000`, their `NXCALS` variable name is stored in `Backend/Parser -> Parser().varlist` and their (nested) location in the `config` file is found in `Backend/Parser -> Parser().configloc`


## Usage
### Parser
With a `DataFrame` of data from NXCALS, the properties required by the `config` file from `lhcmask` can be extracted using the parsing module:
```python
# linking DataFrame to Parser object
mainParser = parser.Parser(data_df)

# setting the observation timestamp:
mainParser.obs_timestamp('2022-07-23 19:30')

# setting the observation beam
mainParser.obs_beam('B1')
```

Then all the relevant quantities can be readily extracted from the `DataFrame` individually:
```python
# Reading the attribute:
mainParser.beam_energy_tot

# Or equivalently, accessing the attribute:
mainParser['beam_energy_tot']
```

Or all at once:
```python
>>> print(40*'-')
    for varName in mainParser.configloc.keys():
        print(f'{varName.ljust(18)}\t{mainParser[varName]}')
    print(40*'-')
    
----------------------------------------
mode              	b4_from_b2_with_bb
optics_file       	acc-models-lhc/operation/optics/R2022a_A30cmC30cmA10mL200cm.madx
beam_norm_emit_x  	1.4367134905573662
beam_norm_emit_y  	1.359021165398161
beam_sigt         	0.30069127446113253
beam_npart        	85156221602825
beam_energy_tot   	6799.6796875
nco_IP1           	974.0
nco_IP5           	974.0
nco_IP2           	876.0
nco_IP8           	912.0
on_x1             	-160.0
on_x2v            	200.0
on_x5             	160.0
on_x8h            	-200.0
----------------------------------------
```


All the required `NXCALS` variables can be listed to facilitate the extraction using the `Spark` module, using:
```python
allvars = mainParser.get_varList()
```



### Spark
To extract a `DataFrame` of data from NXCALS, one can use:
```python
snapshot_ts = '2022-07-23 19:30'

# Initializing the spark session
sparkspace  = spark.SparkSession()

# Choosing a 24h window around the chosen ts
_start = str(pd.Timestamp(snapshot_ts)-pd.Timedelta(seconds = 24*3600))
_stop  = str(pd.Timestamp(snapshot_ts)+pd.Timedelta(seconds = 24*3600))

# Extracting data
var   = "HX:FILLN"
df    = sparkspace.query(var,_start,_stop)
```






## Installation:
This package is intended to be used on a acc computer. We first need to install nxcals and the working python environment. Modify the last line of `installme.sh` with your username: `... username@lxplus.cern.ch: ...` and then:
```bash
bash installme.sh 
```

Then 
```bash
source py_env/bin/activate 
```

To launch the spark builder, a `kinit` is needed:
```bash
kinit username
```

**Warning** : to ensure compatibility of xtrack with python 3.7 used in acc-py, one needs to change the 4 f-strings in `./py_env/xtrack/xtrack/loss_location_refinement` as such:
```python
# From 
f'{i_aper_1=}'
# To
f'i_aper_1={i_aper_1}'
```
This should be done automatically at the end of the `installme.sh` script.





