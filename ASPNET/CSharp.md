## 公式Ref
* [Language](https://docs.microsoft.com/en-us/dotnet/csharp/)
* [.NET API](https://docs.microsoft.com/ja-jp/dotnet/api/)

## Collections
* IEnumerable<T> : foreachが使えるインタフェース
* ICollection<T> : 上に加え、Countが使えるインタフェース。順序を持たない。
* IList<T> : 上に加え、順序を持ち、Item(i), Add, Removeなどができるインタフェース。
* List<T> : IList<T>インタフェースを実装したクラス。Sort, BinarySearchなどができる。

```
List<string> dinosaurs = new List<string>();
dinosaurs.Add("Tyrannosaurus");
```
* ArrayListは使わないほうが良い。
* 基本はList<T>を使う？

* IQueriable ?? LINQ

  
