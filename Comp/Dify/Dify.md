## INSTALL
https://docs.dify.ai/ja-jp/getting-started/install-self-hosted/docker-compose

### Install WSL2
https://docs.docker.com/desktop/setup/install/windows-install/#wsl-2-backend

1. install
    ```powershell
    #if error occur in installation:
    #dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
    #dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
    #shutdown /r /t 0

    # install wsl
    wsl --install Ubuntu
    #wsl --list --online

    # check wsl version (1 or 2)
    wsl -l -v
    #wsl --set-version Ubuntu 2
    ```
2. setting
    - user: meiden/Nagoya1234  (administrator)


### Install Docker Engine on WSL2
https://docs.docker.com/desktop/setup/install/linux/

1. install docker engine  (Docker Desktop is not free)
    - install using the apt repository
      https://docs.docker.com/engine/install/ubuntu/
      - add to curl proxy option: --proxy http://proxy.mei.melco.co.jp:9515
      - add to apt-get proxy option: -o Acquire::http::Proxy="http://proxy.mei.melco.co.jp:9515"
      - add to docker run proxy optin: -e HTTPS_PROXY=http::Proxy="http://proxy.mei.melco.co.jp:9515
      
1. install docker compose
    - follow installation instruction for linux
      https://docs.docker.com/compose/install/linux/#install-using-the-repository
      ```
      sudo apt-get update
      sudo apt-get install docker-compose-plugin

      sudo systemctl status docker
      sudo systemctl restart docker
      sudo systemctl stop docker

      ```
### install dify
https://docs.dify.ai/ja-jp/getting-started/install-self-hosted/docker-compose

```
# install
git config --global http.proxy http://proxy.mei.melco.co.jp:9515
git config --global https.proxy http://proxy.mei.melco.co.jp:9515
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env

# invoke dify
cd dify/docker
sudo docker compose up -d
# -> open with browser http://localhost
```    

* (for error) 
  ```
  sudo usermod -aG docker $(whoami) 
  # to be belong to group docker
  ```

* proxy setting for Docker
  * https://qiita.com/dkoide/items/ca1f4549dc426eaf3735
  * https://zenn.dev/wsuzume/articles/f9935b47ce0b55

* network setting (host ip -> wsl2 ip -> docker ip)
https://rcmdnk.com/blog/2021/03/01/computer-windows-network/
https://qiita.com/yururu_no_yu/items/1fe94eeff12bad910d58
https://qiita.com/omu_kato/items/f9a6b5a02e25f5f2a487


## Setting

### LLM setting
- Settings —> Model Providers,  to add and configure the LLM
### Others
- Settings -> languages -> timezone

### User Account for community version
- login with mail address and password
- 

### IP address


## MCP server
https://docs.dify.ai/ja-jp/plugins/best-practice/how-to-use-mcp-zapier

https://zenn.dev/upgradetech/articles/24a7d76133af4c