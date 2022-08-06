
# Download acc models
git clone https://gitlab.cern.ch/acc-models/acc-models-lhc.git


# from http://bewww.cern.ch/ap/acc-py/installers/              
wget http://bewww.cern.ch/ap/acc-py/installers/acc-py-2020.11-installer.sh      
                      
bash ./acc-py-2020.11-installer.sh -p ./acc-py/base/2020.11/ -b    
           
# activate some acc-py python distribution:                 
source ./acc-py/base/2020.11/setup.sh       
                   
# create your own virtual environment in the folder "py_tn":       
acc-py venv py_env       
                    
# activate your new environment    
source ./py_env/bin/activate   
   
# and finish it with nxcals          
python -m pip install jupyterlab nxcals

# Add cpymad
pip install cpymad

# Add lhcmask and xsuite
git clone https://github.com/lhcopt/lhcmask.git py_env/lhcmask
pip install -e py_env/lhcmask

git clone https://github.com/xsuite/xobjects py_env/xobjects
pip install -e py_env/xobjects

git clone https://github.com/xsuite/xdeps py_env/xdeps
pip install -e py_env/xdeps

git clone https://github.com/xsuite/xpart py_env/xpart
pip install -e py_env/xpart

git clone https://github.com/xsuite/xtrack py_env/xtrack
pip install -e py_env/xtrack

git clone https://github.com/xsuite/xfields py_env/xfields
pip install -e py_env/xfields

# Additionnal packages
pip install jupyterlab
pip install ipywidgets
pip install PyYAML
pip install pyarrow
pip install pandas
pip install matplotlib
pip install scipy
pip install ipympl
pip install ruamel.yaml
pip install rich

# Removing the installer
rm acc-py-2020.11-installer.sh

# Adjusting the links of Backend/config_template.yaml:
sed -i "s|tracking_tools: .*|tracking_tools: $PWD\/py_env|" Backend/config_template.yaml

# Adding modules,tools,beambeam,errors:
git clone https://github.com/lhcopt/lhcmask.git py_env/modules
git clone https://github.com/lhcopt/lhctoolkit.git py_env/tools
git clone https://github.com/lhcopt/beambeam_macros.git py_env/beambeam_macros
git clone https://github.com/lhcopt/lhcerrors.git py_env/errors

# Copying relevant optics files over ssh:
rsync -rv phbelang@lxplus.cern.ch:/afs/cern.ch/eng/lhc/optics/runIII/RunIII_dev/2021_V6 :/afs/cern.ch/eng/lhc/optics/runII/2018 :/afs/cern.ch/eng/lhc/optics/runIII/RunIII_dev/IR7-Run3seqedit.madx py_env/optics


# Modifying xtrack for python 3.7.9 compatibility
sed -i "s|{i_aper_1=}, {i_aper_0=}|i_aper_1={i_aper_1}, i_aper_0={i_aper_0}|" py_env/xtrack/xtrack/loss_location_refinement/loss_location_refinement.py
sed -i "s|{presence_shifts_rotations=}|presence_shifts_rotations={presence_shifts_rotations}|" py_env/xtrack/xtrack/loss_location_refinement/loss_location_refinement.py
sed -i "s|{iteration=}|iteration={iteration}|" py_env/xtrack/xtrack/loss_location_refinement/loss_location_refinement.py


# Modifying lhc.seq to account for the missing harmonic number
sed -i "s|ACSCA : RFCAVITY, L := l.ACSCA;|ACSCA : RFCAVITY, L := l.ACSCA, HARMON := HRF400;|" acc-models-lhc/lhc.seq
sed -i "s|ACSCA : RFCAVITY, L := l.ACSCA;|ACSCA : RFCAVITY, L := l.ACSCA, HARMON := HRF400;|" acc-models-lhc/lhcb4.seq