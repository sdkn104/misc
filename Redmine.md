Redmine MEMO
============

* CORS

  * setting server: [https://qiita.com/8amjp/items/db1f5f71475d00395863]
  * use JSONP: [https://community.bitnami.com/t/redmine-rest-api-origin-not-allowed-crossdomain-problem/11970/2]
  
 
* Reminder mail
  * [http://redmine.jp/faq/issue/send_reminders/]
 
* Apache
  * redmine-3.4.6-2\apache2\htdocs\xxx.htm  --> http://localhost/xxx.htm
  
* View customization
  * [http://d.hatena.ne.jp/suer/20100119/redmine_view_ext]

* Auth
  * auto login by API key
     * ex. http://localhost/redmine/issues?key=a0988524fb7e4949d013d6cd8437ba6f0db97b88
     * ex. http://localhost/redmine/issues?key=d629355c6f9c3b8047a8c4321e0e77e9d13ff002

* Othres
  * MySql
    * [http://a1-style.net/redmine/mysql-setting/]
    * [https://sawara.me/mysql/1428/]
    
Setup History
-------------

* install bitami redmine
* service start/stop by bitami console
* change conf file for CORS:  [https://qiita.com/8amjp/items/db1f5f71475d00395863]
* create redmine.htm in redmine-3.4.6-2\apache2\htdocs\
* modify css redmine-3.4.6-2\apps\redmine\htdocs\public\stylesheets\application.css
   * label[for=issue_fixed_version_id] {font-weight:bold;  text-decoration : underline; color:#FF0000}
* modify view  "redmine-3.4.6-2\apps\redmine\htdocs\app\views\issues\new.html.erb"
* 必須項目の設定   by 設定->ワークフロー
