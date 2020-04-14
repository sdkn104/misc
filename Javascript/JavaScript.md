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
* Lexical Scope (Static Scope)
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

* Closure
  Javascriptの関数はクロージャである。
  関数が定義されたときの環境（定義時のスコープ内部にあったあらゆる変数から構成される）を保持する。
  環境のコピーではなく環境を保持する。複数の関数があれば、同じものを参照する。
  
  
  
