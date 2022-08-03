
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
git clone https://github.com/pbelange/lhcmask.git py_env/lhcmask
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

# Removing the installer
rm acc-py-2020.11-installer.sh