## dev / setup / install
```
# install modules
pip install <packageName>
pip freeze > requirements.txt
pip install [--upgrade] -r requirements.txt
python -V > python.ver.txt

# list modules
pip list -o

# optimize/init module versions
pip freeze > requirements.txt
pip uninstall -y -r requirements.txt
python -m pip install -U pip
pip install pip-tools
cat requirements.txt | foreach { $_ -replace '==.*', ''} | set-content "requirements.in"
#mv requirements.txt requirements.in
pip-compile requirements.in  # created requirements.txt optimizing versions
pip install -r requirements.txt

pip index versions ライブラリ名
pipdeptree

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
