## init
```
nvm use 22
mkdir projname
vd projname
npm init -y
npm install modules...
```
```
npm install  // install all for ./packatge.json
  or,
npm ci // install for package-lock.json
```
## NVM
https://github.com/coreybutler/nvm-windows

1. install NVM by installer nvm_setup.exe
2. 
```
nvm list available
nvm 22.17.0
nvm list
nvm use 22.17.0
node -v

echo 22.17.0 >> .nvmrc
nvm use
```

## webpack
create webpack.config.js

add to package.json
```
"scripts": {
  "build": "webpack"
}
```

```
npm run build
```