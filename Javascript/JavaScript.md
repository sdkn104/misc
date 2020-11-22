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
### Basic
```
const promise1 = new Promise(executor);
const executor = (resolve, reject) => {
  setTimeout(() => {
    resolve('foo');
  }, 300);
};

let promise2 = promise1.then(onFulfilled, onRejected)
const onFulfilled = (value) => {
  return value2;
});
const onRejected = (reason) => {
 return reason2;
};
```
* Promiseオブジェクトは、pending (初期状態), fulfilled (成功して完了), rejected(失敗)の３つの状態を持つ。
* Promiseのコンストラクタ
  * Promiseオブジェクトは関数executor(resolve, reject)をコンストラクタ引数で指定して生成される。
  * Promiseコンストラクタが呼ばれると、オブジェクトが生成される過程でexecutorが実行される。
  * executorは、通常、その処理の中でresolve(value), reject(reason)をコールする。reasonは通常errorオブジェクト。
    通常は、executorは非同期の作業を開始して、作業が終了したときにresolve/rejectが呼ばれるようにする。
  * executorは同期的に実行されるか？(executorが終了してからオブジェクトが返るか？)
* executor -> promise1のresolve
  * 関数executor内でresolve(value)/reject(reason)が呼ばれると、
    生成されたPromiseオブジェクトpromise1はvalue/reasonでresolveされfulfilled/rejectedとなる。
    ただし、value/reasonが別のPromiseオブジェクトpの場合、Promise pにresolveされるが、状態はpと同じになる。
    (pがvalue/reasonでfulfilled/rejectedされていれば同じ値でfulfilled/rejectedされた状態となり、
    　penndingであればpが将来fulfilled/rejectedされたとき同じ値でfulfilled/rejectedされる)
    resolveされたPromoseをresolveしようとしても無効である。
  * executor内で発生した例外はトラップされない(???)。try catchなどでハンドリングすべき。
* fulfill/reject -> ハンドラ起動
  * fulfilled/rejectedとなったとき、既にthen()等でハンドラonFulfilled/onRejectedが登録されていると、
   onFulfilled(value)/onRejected(reason)が非同期に実行(キューに登録)される。
    すでにfulfilled/rejectedであるPromiseに対してthen()等でonFulfilled/onRejectedを登録すると、
    onFulfilled(value)/onRejected(reason)は非同期に実行(キューに登録)される。
* ハンドラ終了 -> promise2のresolve
  * ハンドラonFulfilled/onRejectedの実行が終わると、ハンドラを登録したとき生成された
    Promise(=promise2)を、その戻り値でresolveしてfulfilledとする。
    ただし、戻り値が別のPromise pのとき、pにresolveするが状態はpと同じになる（上記promse1のresolveと同じ）。
  * ハンドラ内で例外が発生したとき、そのerror値でpromise2をrejectする。
* ハンドラ登録とproise2の生成
  * Promiseインスタンスは、then(onFulfilled, onRejected), catch(onRejected), finally(onXXX)でハンドラを登録できる。
   then/catch/finallyは、Promiseを生成して返す。
  * .catch(onRejected) = .then(undefined, onRejected)
                       = .then(function(value){return value}, onRejected) ???
  * .then(onFulfilled) = .then(onFulfiled, undefined) ???
  * onFulfilledに関数以外を登録したとき、idendity(function(v){return v})が登録される。
  * onRejectedに関数以外を登録したとき、thrower(function(v){throw v})が登録される。
* thenのないPromiseは永久にイベントキューに残るのか？　デストラクトするとどうなるか？

### パタン
* ハンドラの連鎖
```
   // onRejectedをもたないthen複数下位のあと、一つのcatch、そのと一つのfunally
   paromiseFunc()
   .then((value) => {
     return value2;
   })
   .then(...)
   .catch(...)
   .funally(...);     
```
* 非同期関数をPromiseでwrapする
* Promise関数をハンドラ内で使う
* ハンドラ内のエラーを外部にthrowする

### async/await

--



