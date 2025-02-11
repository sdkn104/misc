```
sudo apt update
sudo apt upgrade

# node
sudo apt install nodejs npm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
nvm install 14.16.0              
nvm use 14.16.0
```
```
# git
sudo apt install git
#start store credential
git config --global credential.helper store

git push origin main
cat ~/.git-credentials
```
