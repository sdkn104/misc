## 規格
* Version: ES5 -> ES5.1 -> ECMAScript2015（ES2015）= ES6 -> ES2016, ...
* language specification
  * [ES5.1](http://www.ecma-international.org/ecma-262/5.1/index.html)
  * [ES2015](http://www.ecma-international.org/ecma-262/6.0/index.html)
* [ES6 Compatibility](https://kangax.github.io/compat-table/es6/)
* [Wikipedia](https://ja.wikipedia.org/wiki/ECMAScript)
## Doc
* Tutorial [Javascript Primer](https://jsprimer.net/)

## DOM
* reference: [MDN](https://developer.mozilla.org/ja/docs/Web/API/Document_Object_Model)
 
## Topics
### Lexical Scope (Static Scope)
```
A {
    var f;
    B {
        var y = rand();
        f = function(z) { return y + z; };
    }
    x = f(42);
}
```
関数f定義内で外側の変数yを参照している場合、fを呼び出した場合にyはどのyか。
  * staitc (lexical) scopeの場合、どこで呼び出されても常に定義場所のscopeで判断。
  * dynamic scopeの場合、呼び出された場所のscopeで判断。

### Closure
  * Javascriptの関数はクロージャである。
  * 関数が定義されたときの環境（定義時のスコープ内部にあったあらゆる変数から構成される）を保持する。
  * 環境のコピーではなく環境を保持する。複数の関数があれば、同じものを参照する。
  
### Date Time
```
let today = new Date()
let date1 = new Date(1995, 11, 17)            // 日付は 0 起点
let date1 = new Date(1995, 11, 17, 3, 24, 0)
let tm = date1.getTime() // miliseconds from 1970/1/1 0:00
date1.setTime( date1.getTime() + 24*60*60*1000 )
date1.setDate(date1.getDate() - 1)

// date: 日付オブジェクト
// format: 書式フォーマット
function formatDate (date, format) {
  format = format.replace(/yyyy/g, date.getFullYear());
  format = format.replace(/MM/g, ('0' + (date.getMonth() + 1)).slice(-2));
  format = format.replace(/dd/g, ('0' + date.getDate()).slice(-2));
  format = format.replace(/HH/g, ('0' + date.getHours()).slice(-2));
  format = format.replace(/mm/g, ('0' + date.getMinutes()).slice(-2));
  format = format.replace(/ss/g, ('0' + date.getSeconds()).slice(-2));
  format = format.replace(/SSS/g, ('00' + date.getMilliseconds()).slice(-3));
  return format;
};
```
# Promise
```
const promise1 = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve('foo');
  }, 300);
});

promise1.then((value) => {
  console.log(value);
});
```
* Promiseオブジェクトは、pending (初期状態), fulfilled (成功して完了), rejected(失敗)の３つの状態を持つ。
* Promiseオブジェクトは関数executor(resolve, reject)をコンストラクタ引数で指定して生成される。
* Promiseコンストラクタが呼ばれると、オブジェクトが生成される過程でexecutorが実行される。
* executorは、通常、その処理の中でresolve(value), reject(reason)をコールする。reasonは通常errorオブジェクト。
  通常は、executorは非同期の作業を開始して、作業が終了したときにresolve/rejectが呼ばれるようにする。
* 関数executor内でresolve(value)/reject(reason)が呼ばれると、生成されたPromiseオブジェクトはそのvalue/reasonでfulfilled/rejectedにresolveされる。
  ただし、value, reasonがPromiseオブジェクトの場合、そのpromiseにresolveされるが、fulfilledでもrejectedでもない。
  resolveされたPromoseをresolveしようとしても無効である。
* fulfilled/rejectedにresolveされされたとき、既にthen()等でハンドラonFulfilled/onRejectedが登録されていると、
　onFulfilled/onRejectedが非同期に実行(キューに登録)される。
  すでにfulfilled/rejectedにresolveされたPromiseに対してthen()等でonFulfilled/onRejectedを登録すると、
  それは非同期に実行(キューに登録)される。
* onFulfilled/onRejectedの実行が終わるとその戻り値でonFulfilled/onRejectedを登録したとき生成された
  Promise(=p1)をresolve/rejectする(p1.resolve/reject(value/reason))。
* Promiseインスタンスは、then(onFulfilled), catch(onRejected), finally(onXXX)でハンドラを登録できる。
　then/catch/finallyは、Promiseを生成して返す。
* .catch(onRejected) = .then(undefined, onRejected)
                     = .then(function(value){return value}, onRejected) ???
  .then(onFulfilled) = .then(onFulfilled, undefined) ???
--



