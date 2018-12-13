* ActiveXData Objects（以下ADO）からODBCドライバを使用する方法
  * instant client, odbc driver必要。 odbc_install.exe -> registryに登録される
  
* ADOからOLE DBドライバを使用する方法
  * OLE DBには、Oracle 提供の Oracle Provider for OLE DB (OraOLEDB) と  
    * Oracle に接続するには、Oracle Client が必要です。
    * Oracle Instant Client の ODACをインストールすればよい。
      * install.bat oledb
    * "Provider=OraOLEDB.Oracle;Data Source=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=orcl)));User ID=system;Password=manager"

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
