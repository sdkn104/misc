* Oracle Objectsfor OLE（以下oo4o）を使用する方法
  * Oracleクライアントの機能が必要
  * 公式サイトに行って、ODACパッケージをダウンロード。インストールはレジストリ登録する
  * Instant ClientのODACパッケージを解凍。install.bat実行のみ。
     https://srad.jp/~black-hole/journal/517310/
     インストールが完了するとinstall.batで指定したORACLE_HOME配下にODACのモジュールが展開され、ORACLE_HOMEのレジストリキーが追加されます。
  * __11g (11.2) の 32bit 版が最終。__

* ActiveXData Objects（以下ADO）からODBCドライバを使用する方法
  * ADO -(OLEDB)-> Microsoft OLE DB Provider for ODBC -(ODBC)-> Oracle ODBC Driver -> Oracle Client (OCI) -> DB
  * PLSQLはできそう。
  * インストール：instant client, odbc driver必要。 odbc_install.exe -> registryに登録される
    * https://www.oracle.com/technetwork/jp/database/database-technologies/instant-client/overview/index.html
    1. install instant client basic
    1. odbc_install.exe JA
         * Oracle Instant Client directory (present directory) name will be part of the driver name in registry.
         * 登録確認：ODBCデータソースアドミニストレータ:「コントロールパネル」から［管理ツール］－［データソース(ODBC)］の順に選択します。
           * -> Driverのタブに、Oracle in OraDb11g_home1が表示される。OraDb11g_home1はインストールフォルダ。
           * -> システムDSNの追加登録すれば、上記ドライバのDSNを登録できるみたい。driver名で呼び出すならたぶん不要。
    1. PATH, TNS_ADMIN を設定する
  * 使い方
    * Oracle ODBC Driver: https://docs.oracle.com/cd/E57425_01/121/ADFNS/adfns_odbc.htm#BABGJEHF
    * 参照可能なライブラリファイルから「Microsoft ActiveX Data Objects X.X Library」を選択
    * ADO Connection OpenのconnectStringに、DRIVER={Oracle in OraDb11g_home1} のようにフォルダ名指定。__バージョン共存できそう__
       * https://excelwork.info/excel/databaseoracleodbc/
       * https://docs.oracle.com/cd/E57425_01/121/ADFNS/adfns_odbc.htm#BABIJAGI
       * installdir/ODBC_IC_Readme_Win.html
  * coding
      * Microsoft OLE DB Provider for ODBC: https://msdn.microsoft.com/ja-jp/library/cc426827.aspx
      * ADO ref: https://msdn.microsoft.com/ja-jp/library/cc408215.aspx
        * transaction: cn.BeginTrans, cn.CommitTrans, ..
      * Oracle SQL ref: https://docs.oracle.com/cd/E82638_01/sqlrf/index.html
        * 上記リンクにANSI SQL準拠状況の記載あり
      * PL/SQL: https://docs.oracle.com/cd/E57425_01/121/LNPLS/title.htm
        * ANSI SQL/PSM: PL/SQLと似たもの。俗に「ストアドプロシージャ」と呼ばれる。
      * Embedded SQL: https://ja.wikipedia.org/wiki/%E5%9F%8B%E3%82%81%E8%BE%BC%E3%81%BFSQL
        * これを「埋め込みSQL」(Embedded SQL/ESQL) と呼び、後にANSIにより仕様が標準化された。
        * Oracle Embedded SQL: https://docs.oracle.com/cd/E57425_01/121/LNPCC/toc.htm
      * CLI: ANSI SQL/CLI = ODBCとほぼ同じ。https://ja.wikipedia.org/wiki/Call_Level_Interface
      * Dynamic SQL: https://ja.wikipedia.org/wiki/SQL
      　* ANSI SQLで規定。
  * 改修方針
      * setupload(arr, table, opt) -> execute時にapiでinsertを呼ぶ。1row/1call でもよいが20rows/1callとかのほうが高速。
      * addplsql(plsql) -> execute時にapiでplsqlを実行。
      * setselect(sql) -> execute時にapiでselect実行してrsetに取得。
  * 改修方針(http)
      * http post で csv, table, opt, plsql, sqlを送信。
       
* ADOからOLE DBドライバを使用する方法
  * Microsoft 提供の OLE DB Provider for Oracle を使う方法
    * __この機能は、Windows の将来のバージョンで削除されます。__ 新規の開発作業ではこの機能を使用しないようにし、現在この機能を使用しているアプリケーションは修正することを検討してください。 代わりに、Oracle の OLE DB プロバイダーを使用します。
    * Oracle に接続するには、Oracle Client が必要です。

  * Oracle 提供の Oracle Provider for OLE DB (OraOLEDB) を使う方法
    * Oracle に接続するには、Oracle Client が必要です。
    * Oracle Instant Client の ODACをインストールすればよい。
      * https://www.oracle.com/technetwork/jp/database/windows/downloads/utilsoft-087491-ja.html
      * https://www.oracle.com/technetwork/topics/dotnet/install121024-2704210.html
        * ODAC XCopyバージョン。instant clientも同梱
        * instant clientのインストール：解凍してパスを通す。
        * install.bat oledb  -> レジストリに登録。レジストリ登録名がOraOLEDB.Oracle。__なのでバージョン共存はできなさそう。__
    * 使い方　 http://skill-note.net/post-822/
      * 参照可能なライブラリファイルから「Microsoft ActiveX Data Objects X.X Library」を選択
      * "Provider=OraOLEDB.Oracle;Data Source=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=orcl)));User ID=system;Password=manager"
      * PLSQL blockも呼べそう
    * coding
      * OraOLEDB ref: https://docs.oracle.com/cd/E62988_01/win.122/b72976/toc.htm
      

