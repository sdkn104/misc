## DESCRIPTION
* This program check the status of current PC user in Seat System D/B, and warning toast notification if status is not set.
* This program assumes to be called by Windows Task Scheduler periodically, while a user is logged on and network is connected.

## HOW TO UPDATE and DEPLOY
1. install python (3.12, etc)
1. do the followings:
```
pip install -r requirements.txt
```
1. modify source file: checkSeat.py
1. do the followings:
```
pyinstaller --onefile checkSeat.py  
# -> created ./dist/checkSeat.exe
```
