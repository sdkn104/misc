# INSTALL

- python 3.13, etc
```powershell
pip install -r requerements.txt
python app.py
```
- exe
```powershell
# modify app.py -> uvicorn.run(...., reload=False, log_config=None)
pip install pyinstaller
pyinstaller app.py --onefile --noconsole
```
