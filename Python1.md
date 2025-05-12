## dev / setup / install
```
pip install <packageName>
pip freeze > requirements.txt
pip install [--upgrade] -r requirements.txt

pip list -o

# optimize/init module versions
pip freeze > requirement.txt
pip uninstall -r requirement.txt
python -m pip install -U pip
pip install pip-tools
mv requirement.txt requirement.in
pip-compile requirements.in  # created requirement.txt
pip install -r requirements.txt

pip list -o
```

## venv
```
cd C:\Users\Username
mkdir my_project
cd my_project

py -3.12 -m venv myenv

# start venv
.\myenv\Scripts\activate
python -V
# 
pip install <package-name>
python xxxx.py

code .
```
