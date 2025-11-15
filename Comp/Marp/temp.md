
- Azure (Megcloud)
    - OpenAI API
    - Webコンソール

- オンプレミス
    - PC（クラウド使用者）
    - サーバ（仮想サーバ）
        - 中継サーバ

    - サーバ（仮想サーバ）
        - Dify
    
    - PC（エンドユーザ）
        - エクセル（VBA）
        - Cline
        - 他

```mermaid
flowchart LR

  subgraph Azure_Megcloud[Azure（Megcloud）]
    Azure_Megcloud_OpenAI["Azure OpenAI API"]
    Azure_Megcloud_WebConsole["Webコンソール"]
  end

  subgraph OnPremise["オンプレミス"]
    OnPremise_PC["PC（クラウド管理担当）"]
    subgraph OnPremise_Server1["サーバ（仮想サーバ）A"]
      OnPremise_Server_Chukei["中継サーバ"]
      OnPremise_Server_log["(Log)"]
    end
    subgraph OnPremise_Server2["サーバ（仮想サーバ）B"]
      OnPremise_Server_Dify["Dify"]
    end
    subgraph OnPremise_PC_EndUser["PC（エンドユーザ）"]
      OnPremise_PC_EndUser_Excel["エクセル（VBA）"]
      OnPremise_PC_EndUser_Cline["Cline"]
      OnPremise_PC_EndUser_Other["他"]
      OnPremise_PC_EndUser_Edge["Edgeブラウザ"]
    end
  end

  %% 適当に末端ノード間の矢印も追加
OnPremise_Server_Chukei --Azure API Key--> Azure_Megcloud_OpenAI
OnPremise_PC -- 管理ID/PW --> Azure_Megcloud_WebConsole
OnPremise_Server_Chukei -.-> OnPremise_Server_log
OnPremise_Server_Dify --Key--> OnPremise_Server_Chukei
OnPremise_PC_EndUser_Excel --Key--> OnPremise_Server_Chukei
OnPremise_PC_EndUser_Other --Key--> OnPremise_Server_Chukei
OnPremise_PC_EndUser_Cline --Key--> OnPremise_Server_Chukei
OnPremise_PC_EndUser_Edge --ID/PW--> OnPremise_Server_Dify
```
