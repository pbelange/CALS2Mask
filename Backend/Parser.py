#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu July 28 11:50:29 2022
i
@author: phbelang
"""

import numpy as np
import pandas as pd

import Backend.Constants as cst


#==========================================
# OPTICS CROSS REFERENCE
#==========================================

# /afs/cern.ch/eng/lhc/optics/runIII/RunIII_dev/2021_V6/PROTON/README
OPTICS_CROSSREF = { 'R2022a_A60cmC60cmA10mL200cm' : 'opticsfile.23',
                    'R2022a_A56cmC56cmA10mL200cm' : 'opticsfile.24',
                    'R2022a_A52cmC52cmA10mL200cm' : 'opticsfile.25',
                    'R2022a_A48cmC48cmA10mL200cm' : 'opticsfile.26',
                    'R2022a_A45cmC45cmA10mL200cm' : 'opticsfile.27',
                    'R2022a_A41cmC41cmA10mL200cm' : 'opticsfile.28',
                    'R2022a_A38cmC38cmA10mL200cm' : 'opticsfile.29',
                    'R2022a_A35cmC35cmA10mL200cm' : 'opticsfile.30',
                    'R2022a_A32cmC32cmA10mL200cm' : 'opticsfile.31',
                    'R2022a_A30cmC30cmA10mL200cm' : 'opticsfile.32'}


#==========================================
# PARSER CLASS
#==========================================
class Parser():
    def __init__(self,data_df = pd.DataFrame({})):
        
        # Main attributes
        self.data  = data_df
        self.ts    = None
        self.beam  = None
        self.bunch = None

        # NXCALS variable list used for each property
        self.varlist  = {'optics_file'     : 'BFC.LHC:OpticsActive:opticsName',
                        'beam_norm_emit_x' : {'B1':'LHC.BSRT.5R4.B1:AVERAGE_EMITTANCE_H',
                                              'B2':'LHC.BSRT.5L4.B2:AVERAGE_EMITTANCE_H'},
                        'beam_norm_emit_y' : {'B1':'LHC.BSRT.5R4.B1:AVERAGE_EMITTANCE_V',
                                              'B2':'LHC.BSRT.5L4.B2:AVERAGE_EMITTANCE_V'},
                        'beam_sigt'        : {'B1':'LHC.BQM.B1:BUNCH_LENGTH_MEAN',
                                              'B2':'LHC.BQM.B2:BUNCH_LENGTH_MEAN'},
                        'beam_npart'       : {'B1':'LHC.BCTDC.A6R4.B1:BEAM_INTENSITY',
                                              'B2':'LHC.BCTDC.A6R4.B2:BEAM_INTENSITY'},
                        'beam_energy_tot'  : {'B1':'LHC.BCCM.B1.A:BEAM_ENERGY',
                                              'B2':'LHC.BCCM.B2.A:BEAM_ENERGY'},
                        'oct_current'      : {'B1':'RPMBB.UJ33.ROD.A23B1:I_MEAS',
                                              'B2':'RPMBB.UJ33.ROD.A23B2:I_MEAS'},
                        'lumi_ip1'         : 'ATLAS:LUMI_TOT_INST',
                        'lumi_ip2'         : 'ALICE:LUMI_TOT_INST',
                        'lumi_ip5'         : 'CMS:LUMI_TOT_INST',
                        'lumi_ip8'         : 'LHCB:LUMI_TOT_INST',
                        'nco_IP1'          : 'LHC.STATS:NUMBER_COLLISIONS_IP1_5',
                        'nco_IP5'          : 'LHC.STATS:NUMBER_COLLISIONS_IP1_5',
                        'nco_IP2'          : 'LHC.STATS:NUMBER_COLLISIONS_IP2',
                        'nco_IP8'          : 'LHC.STATS:NUMBER_COLLISIONS_IP8',
                        'on_x1'            : 'LHC.RUNCONFIG:IP1-XING-V-MURAD',
                        'on_x2v'           : 'LHC.RUNCONFIG:IP2-XING-V-MURAD',
                        'on_x5'            : 'LHC.RUNCONFIG:IP5-XING-H-MURAD',
                        'on_x8h'           : 'LHC.RUNCONFIG:IP8-XING-H-MURAD'}
        
        # Location in the config file (including nested properties)
        self.configloc = {  'mode'             : '/',
                            'optics_file'      : '/',
                            'beam_norm_emit_x' : '/',
                            'beam_norm_emit_y' : '/',
                            'beam_sigt'        : '/',
                            'beam_npart'       : '/',
                            'beam_energy_tot'  : '/',
                            'oct_current'      : '/', 
                            'lumi_ip1'         : '/', 
                            'lumi_ip2'         : '/', 
                            'lumi_ip5'         : '/', 
                            'lumi_ip8'         : '/', 
                            'nco_IP1'          : '/',
                            'nco_IP5'          : '/',
                            'nco_IP2'          : '/',
                            'nco_IP8'          : '/',
                            'on_x1'            : 'knob_settings/',
                            'on_x2v'           : 'knob_settings/',
                            'on_x5'            : 'knob_settings/',
                            'on_x8h'           : 'knob_settings/'}


    #---------------------------------
    # ALL PROPERTIES USED FOR CONFIG
    #----------------------------------
    #---------------------
    @property
    def mode(self,):
        return {'B1':'b1_with_bb','B2':'b4_from_b2_with_bb'}[self.beam]
    #---------------------
    @property
    def optics_file(self,):
        _var  = self.varlist['optics_file']
        fname = self.get_previous(_var)
        
        optfile = OPTICS_CROSSREF[fname]
        #return f'acc-models-lhc/operation/optics/{fname}.madx'
        return f'optics_repository/{optfile}'
    #---------------------
    @property
    def beam_norm_emit_x(self,):
        # return in [um]
        #_var = f'LHC.BSRT.{_loc}:BUNCH_EMITTANCE_H'
        
        _var  = self.varlist['beam_norm_emit_x'][self.beam]
        value = self.get_previous(_var)
        
        return value
    #---------------------
    @property
    def beam_norm_emit_y(self,):
        # return in [um]
        
        _var  = self.varlist['beam_norm_emit_y'][self.beam]
        value = self.get_previous(_var)
        
        return value
    #---------------------
    @property   
    def beam_sigt(self,):
        #return in [m]
        #_var = f'LHC.BQM.{self.beam}:BUNCH_LENGTHS'
        
        _var  = self.varlist['beam_sigt'][self.beam]
        value = self.get_previous(_var)
        
        # return in [m]
        return value*cst.c
    #---------------------
    @property   
    def beam_npart(self,):
        #_var = f'LHC.BCTFR.A6R4.{self.beam}:BUNCH_INTENSITY'
        
        _var  = self.varlist['beam_npart'][self.beam]
        value = self.get_previous(_var)
        
        return int(value)
    #---------------------
    @property
    def beam_energy_tot(self,):         
        # return in [GeV]
        _var  = self.varlist['beam_energy_tot'][self.beam]
        value = self.get_previous(_var)
        
        return value
    #---------------------
    @property
    def oct_current(self,):
        _var  = self.varlist['oct_current'][self.beam]
        value = self.get_previous(_var)
        
        return value
    #---------------------
    @property
    def lumi_ip1(self,):
        _var  = self.varlist['lumi_ip1']
        value = self.get_previous(_var)
        
        # from Hz/ub to Hz/cm2
        return float(f'{value/(1e-30):.4e}')
    #---------------------
    @property
    def lumi_ip2(self,):
        _var  = self.varlist['lumi_ip2']
        value = self.get_previous(_var)
        
        # from Hz/ub to Hz/cm2
        return float(f'{value/(1e-30):.4e}')
    #---------------------
    @property
    def lumi_ip5(self,):
        _var  = self.varlist['lumi_ip5']
        value = self.get_previous(_var)
        
        # from Hz/ub to Hz/cm2
        return float(f'{value/(1e-30):.4e}')
    #---------------------
    @property
    def lumi_ip8(self,):
        _var  = self.varlist['lumi_ip8']
        value = self.get_previous(_var)
        
        # from Hz/ub to Hz/cm2
        return float(f'{value/(1e-30):.4e}')
    #---------------------   
    @property
    def nco_IP1(self,):
        _var  = self.varlist['nco_IP1']
        value = self.get_previous(_var)
        
        return value
    #---------------------
    @property
    def nco_IP5(self,):
        _var  = self.varlist['nco_IP5']
        value = self.get_previous(_var)
        
        return value
    #---------------------
    @property
    def nco_IP2(self,):
        _var  = self.varlist['nco_IP2']
        value = self.get_previous(_var)
        
        return value
    #---------------------
    @property
    def nco_IP8(self,):
        _var  = self.varlist['nco_IP8']
        value = self.get_previous(_var)
        
        return value
    #---------------------
    @property
    def on_x1(self,):
        _var  = self.varlist['on_x1']
        value = self.get_previous(_var)
        
        return value
    #---------------------
    @property
    def on_x2v(self,):
        _var  = self.varlist['on_x2v']
        value = self.get_previous(_var)
        
        return value
    #---------------------
    @property
    def on_x5(self,):
        _var  = self.varlist['on_x5']
        value = self.get_previous(_var)
        
        return value
    #---------------------
    @property
    def on_x8h(self,):
        _var  = self.varlist['on_x8h']
        value = self.get_previous(_var)
        
        return value

    
    #---------------------------------
    # METHODS TO QUERRY DATA
    #----------------------------------
    def obs_timestamp(self,ts):
        # Ensuring consistent ts format
        if pd.Timestamp(ts).tzinfo is None:
            ts = pd.Timestamp(ts).tz_localize('UTC')
        self.ts = ts

    def obs_beam(self,beam):
        self.beam = beam.upper()

    def obs_bunch(self,bunchNum):
        self.bunch = bunchNum

    def get_previous(self,_var,returnTS = False):
        subset = self.data[_var].dropna()
        _ts    = subset.index[subset.index.get_loc(self.ts, method='pad')]
        if returnTS:
            return _ts,self.data.loc[_ts,_var]
        else:
            return self.data.loc[_ts,_var]

    def get_next(self,_var,returnTS = False):
        subset = self.data[_var].dropna()
        _ts    = subset.index[subset.index.get_loc(self.ts, method='backfill')]
        if returnTS:
            return _ts,self.data.loc[_ts,_var]
        else:
            return self.data.loc[_ts,_var]

    def get_nearest(self,_var,returnTS = False):
        subset = self.data[_var].dropna()
        _ts    = subset.index[subset.index.get_loc(self.ts, method='nearest')]
        if returnTS:
            return _ts,self.data.loc[_ts,_var]
        else:
            return self.data.loc[_ts,_var]

    def __getitem__(self, item):
        return getattr(self, item)

    def get_varList(self):
        allvars = []
        for key,item in self.varlist.items():
            if type(self.varlist[key]) is dict:
                allvars += list(self.varlist[key].values())
            else:
                allvars.append(item)
        return allvars
    
    def update_config(self,config):
        
        # Copying to new config
        newConf = config.copy()
        for key,loc in self.configloc.items():
            
            # Access value, including nested ones
            gettr = newConf
            for sub in loc.split('/')[:-1]:
                if sub == '':
                    continue
                gettr = gettr[sub]
            
            # Replace value with current one
            if isinstance(self[key],np.floating):
                gettr[key] = float(self[key])
            else:
                gettr[key] = self[key]
        
        return newConf
            
    
    

#===================================
# BACKUPS
#===================================

 # https://lhc-commissioning.web.cern.ch/systems/data-exchange/published-topics/beam-modes.htm
BACKUP_BeamMode = 'HX:BMODE'
BACKUP_BeamMode_continuous = {'LHC.CISA.CCR:BEAM_MODE':{ 1  : 'NOMODE',
                                            2  : 'SETUP',
                                            3  : 'INJPILOT',
                                            4  : 'INJINTR',
                                            5  : 'INJNOMN',
                                            6  : 'PRERAMP',
                                            7  : 'RAMP',
                                            8  : 'FLATTOP',
                                            9  : 'SQUEEZE',
                                            10 : 'ADJUST',
                                            11 : 'STABLE',
                                            12 : 'UNSTABLE',
                                            13 : 'BEAMDUMP',
                                            14 : 'RAMPDOWN',
                                            15 : 'RECOVERY',
                                            16 : 'INJDUMP',
                                            17 : 'CIRCDUMP',
                                            18 : 'ABORT',
                                            19 : 'CYCLING',
                                            20 : 'WBDUMP',
                                            21 : 'NOBEAM'}}

