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