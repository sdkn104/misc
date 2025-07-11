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
### install Dify
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
* port mapping: wsl2 -> docker
  ```
  # check port mapping
  sudo docker compose ps -a
  ```

* (when error) 
  ```
  sudo usermod -aG docker $(whoami) 
  # to be belong to group docker
  ```

* proxy setting for Docker
  * https://qiita.com/dkoide/items/ca1f4549dc426eaf3735
  * https://zenn.dev/wsuzume/articles/f9935b47ce0b55

### Network setting

* port mapping:  host ip -> wsl2 ip

  -  https://rcmdnk.com/blog/2021/03/01/computer-windows-network/
  -  https://qiita.com/yururu_no_yu/items/1fe94eeff12bad910d58
  -  https://qiita.com/omu_kato/items/f9a6b5a02e25f5f2a487
  - https://zenn.dev/yamamoto_11709/articles/1e90bc9f7b7500
  - https://scrapbox.io/hotchpotch/WSL2_%E7%92%B0%E5%A2%83%E3%81%B8%E3%81%AE_port_forwarding
  * default port mapping: localhost -> WSL2 address
  1. get WSL2 IP address (exec on WSL2)
      ```
      ifconfig eth0 | grep 'inet ' | awk '{print $2}'
      ```
  2. set port forwarding (exec on PowerShell)
      ```
      netsh.exe interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=80   connectaddress=WSL2_ADDRESS connectport=80
      netsh.exe interface portproxy show v4tov4
      #netsh.exe interface portproxy delete v4tov4 listenport=80 listenaddress=0.0.0.0
      ```
  3. access from host PC or external PC
     * `IP_address_of_host_PC:80`

* setting firewall 
  * open port 80
  * https://support.borndigital.co.jp/hc/ja/articles/360002711593-Windows10%E3%81%A7%E7%89%B9%E5%AE%9A%E3%81%AE%E3%83%9D%E3%83%BC%E3%83%88%E3%82%92%E9%96%8B%E6%94%BE%E3%81%99%E3%82%8B

## Dify Setting

### LLM setting
- Settings —> Model Providers,  to add and configure the LLM
### Others
- Settings -> languages -> timezone

### User Account for community version
- login with mail address and password
- 


## MCP server
https://docs.dify.ai/ja-jp/plugins/best-practice/how-to-use-mcp-zapier

https://zenn.dev/upgradetech/articles/24a7d76133af4c