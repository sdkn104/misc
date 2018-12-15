* ActiveXData Objects（以下ADO）からODBCドライバを使用する方法
  * instant client, odbc driver必要。 odbc_install.exe -> registryに登録される
  
* ADOからOLE DBドライバを使用する方法
  * OLE DBには、Oracle 提供の Oracle Provider for OLE DB (OraOLEDB) と  
    * Oracle に接続するには、Oracle Client が必要です。
    * Oracle Instant Client の ODACをインストールすればよい。
      * https://www.oracle.com/technetwork/jp/database/windows/downloads/utilsoft-087491-ja.html
      * https://www.oracle.com/technetwork/topics/dotnet/install121024-2704210.html
        * ODAC XCopyバージョン。instant clientも同梱
        * instant clientのインストール：解凍してパスを通す。
        * install.bat oledb  -> レジストリに登録
    * 使い方　 http://skill-note.net/post-822/
      * 参照可能なライブラリファイルから「Microsoft ActiveX Data Objects X.X Library」を選択
      * "Provider=OraOLEDB.Oracle;Data Source=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=orcl)));User ID=system;Password=manager"
    * https://docs.oracle.com/cd/E62988_01/win.122/b72976/toc.htm
      * PLSQL blockも呼べそう
    * 改修方針
      * setupload() -> execute時にapiでinsertを呼ぶ。1row/1call でもよいが20rows/1callとかのほうが高速。
      * addplsql() -> execute時にapiでplsqlを実行。
      * setselect() -> execute時にapiでselect実行してrsetに取得。

  * Microsoft 提供の OLE DB Provider for Oracle の２種類があります。
    * この機能は、Windows の将来のバージョンで削除されます。 新規の開発作業ではこの機能を使用しないようにし、現在この機能を使用しているアプリケーションは修正することを検討してください。 代わりに、Oracle の OLE DB プロバイダーを使用します。
    * Oracle に接続するには、Oracle Client が必要です。

* Oracle Objectsfor OLE（以下oo4o）を使用する方法
  * Oracleクライアントの機能が必要
  * 公式サイトに行って、ODACパッケージをダウンロード。インストールはレジストリ登録する
  * Instant ClientのODACパッケージを解凍。install.bat実行のみ。
     https://srad.jp/~black-hole/journal/517310/
     インストールが完了するとinstall.batで指定したORACLE_HOME配下にODACのモジュールが展開され、ORACLE_HOMEのレジストリキーが追加されます。
  * 11g (11.2) の 32bit 版が最終。
