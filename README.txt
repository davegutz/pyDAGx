Dave Gutz's Python tools

10/1/2010

Python is meant to be installed as one giant package at the computer admin level.   Then you should be able to add packages locally using setup.py stuff, otherwise known as "setuptools" sometimes known as "easy_install"  (Windows).

For windows, you need to install the "easy_install" program to complete the top level administrative stuff.   Download and install "easy_install.exe" using other email.


Installing packages:

mac OS X:
sudo python setup.py install --install-scripts=/usr/local/bin

Windows:
pip install --index-url https://test.pypi.org/simple/ pyDAG3
or
pip install pyDAG3-3.4-py2-none-any.whl
#python setup.py install
in .bashrc
alias my_replace='python -m pyReplace.py'

Linux:
sudo python setup.py install
in .bashrc
alias replace='python pyReplace.py'

UNIX: 
python setup.py install --home=~ --install-scripts=~/bin 
in .bashrc
alias replace='python pyReplace.py'


Building packages:

For some reason this is hard.  I am doing this on my netbook mac OS X at present in ~/source/python.  Take for example pyDAG3.   It has a top level that resides in ~/source/python.   Inside that is another pyDAG3 with all the stuff in it.   This is so the top level can be built and named with versions for installation while keeping the package name pyDAG3 when used.

cd ~/source/python/pyDAG3


To build the MANIFEST file:
-  populate MANIFEST.in
- run following to update the MANIFEST file.   It looks in setup.py for "packages".   It counts on the __init.py__ files to point down into packages.


To construct a scratch build folder:
python setup.py build

To build a tar.gz distribution.  The tar.gz file will be in dist folder:
python setup.py sdist bdist bdist_wheel
or
Run the "dist" process in PyCharm.  Be sure to up the version in setup.py

Upload for trial ****use Windows CMD for this**********
cd Documents\GitHub\pyDAGx
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
uname=davegutz, pwd=Stevie18g

Test
pip install --index-url https://test.pypi.org/simple/ pyDAG3
or for available local whl copy
pip install pyDAG3-3.5.5-py3-none-any.whl


Uninstall  ******use Window CMD for this********
pip uninstall pyDAG3
or
python -m pip uninstall pyDAG3-3.5.5-py3-none-any.whl


Version number goes into setup.py

python setup.py sdist --manifest-only

Running scripts:
Add PY to PATHEXT
dos prompt   > pyReplace
cygwin prompt$ python "`cygpath -w /cygdrive/c/Users/Dave/AppData/Local/Programs/Python/Python37/Scripts/pyReplace.py`"

Running python in cygwin.  In windows, python is an attached process and uses pipes hence -i
python -i
or
cygstart python

