# INSTALL
https://docs.dify.ai/ja-jp/getting-started/install-self-hosted/docker-compose

### Install WSL2
https://learn.microsoft.com/en-us/windows/wsl/install

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
    - create admin user/password for Ubuntu


### Install Docker Engine on WSL2
https://docs.docker.com/engine/install/ -> select "Ubuntu"

* Since commercial use of Docker Desktop in larger enterprises requires a paid subscription.
* so, we use Docker Engine instead.

1. install docker engine 
    - follow "Install using the apt repository" in https://docs.docker.com/engine/install/ubuntu/
      - add to curl proxy option: --proxy http://proxy.xxx.com
      - add to apt-get proxy option: -o Acquire::http::Proxy="http://proxy.xxx.com"
      - add to docker run proxy optin: -e HTTPS_PROXY=http::Proxy="http://proxy.xxx.com
      
1. install docker compose
    - follow "Install using the repository" in
      https://docs.docker.com/compose/install/linux/#install-using-the-repository
      ```bash
      sudo apt-get update
      sudo apt-get install docker-compose-plugin
      docker compose version

      sudo systemctl status docker
      #sudo systemctl restart docker
      #sudo systemctl stop docker
      ```
* proxy setting for Docker
  * https://qiita.com/dkoide/items/ca1f4549dc426eaf3735
  * https://zenn.dev/wsuzume/articles/f9935b47ce0b55

### install Dify
https://docs.dify.ai/ja-jp/getting-started/install-self-hosted/docker-compose

```bash
# install
git config --global http.proxy http://proxy.xxx.com
git config --global https.proxy http://proxy.xxx.com
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env
```    

### run Dify
```bash    
cd dify/docker
sudo docker compose up -d
# -> access with browser http://localhost
sudo docker compose ps
```    
* (when error) 
  ```bash
  sudo usermod -aG docker $(whoami) 
  # to be belong to group docker
  ```
* check if Dify running
  ```bash
  sudo docker compose ps
  ```

### Setting Network
* network configuration:
  * IP address of Host
  * IP address of WSL2 (virtual environment)
  * IP address of Docker Container (semi-virtual environment)
* port mapping: WSL2 -> docker container "nginx"
  * mapping is specified in ports section of nginx in docker-compose.yaml
  * default:  0.0.0.0:80->80, 0.0.0.0:443->443
      * Mapping port 80 of WSL2 to port 80 of docker container "nginx" 
  * check port mapping of nginx
    ```bash
    sudo docker compose ps -a
    ```
  * check listen ports in WSL2
    ```bash
    sudo lsof -i -nP
    ```

* port mapping:  Host -> WSL2
  -  https://rcmdnk.com/blog/2021/03/01/computer-windows-network/
  -  https://qiita.com/yururu_no_yu/items/1fe94eeff12bad910d58
  -  https://qiita.com/omu_kato/items/f9a6b5a02e25f5f2a487
  - https://zenn.dev/yamamoto_11709/articles/1e90bc9f7b7500
  - https://scrapbox.io/hotchpotch/WSL2_%E7%92%B0%E5%A2%83%E3%81%B8%E3%81%AE_port_forwarding
  * Default fowarding: Any TCP port you listen on inside WSL2 is automatically forwarded to the Windows host’s localhost on the same port.
  * if you want use Dify from external client, do followings
  * WLS2 IP address is changed per startup

  1. get WSL2 IP address (exec on WSL2)
      ```bash
      ifconfig eth0 | grep 'inet ' | awk '{print $2}'
        #or
      ip addr show eth0 | sed -e 's/\// /g' | awk '/inet /{print $2}'
      ```
  2. set port forwarding (exec on PowerShell)
      ```bash
      netsh.exe interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=80   connectaddress=WSL2_ADDRESS connectport=80
      netsh.exe interface portproxy show v4tov4
      #netsh.exe interface portproxy delete v4tov4 listenport=80 listenaddress=0.0.0.0
      ```

  3. setting firewall 
      * open port 80 by Windows Defender Wirewall
      * https://support.borndigital.co.jp/hc/ja/articles/360002711593-Windows10%E3%81%A7%E7%89%B9%E5%AE%9A%E3%81%AE%E3%83%9D%E3%83%BC%E3%83%88%E3%82%92%E9%96%8B%E6%94%BE%E3%81%99%E3%82%8B
      ```powershell
      # set firewall
      netsh advfirewall firewall add rule name="★Dify TCP 80" dir=in action=allow protocol=TCP localport=80 profile=private,domain
      # show firewall
      netsh advfirewall firewall show rule name="★Dify TCP 80"
      # delete firewall
      netsh advfirewall firewall delete rule name="★Dify TCP 80"
      ```

  * instead of 1 and 2:

    ~/bin/wsl_port_forwarding.sh:
    ```bash
    #!/bin/bash

    IP=$(ip addr show eth0 | sed -e 's/\// /g' | awk '/inet /{print $2}')
    LISTENPORTS=(80) 

    echo IP=$IP
    echo LISTENPORTS=$LISTENPORTS

    for port in "${LISTENPORTS[@]}"
    do
      netsh.exe interface portproxy delete v4tov4 listenport=$port
      netsh.exe interface portproxy add    v4tov4 listenport=$port connectaddress=$IP
      netsh.exe interface portproxy show   v4tov4
    done
    ```
    ```powershell
    PS> wsl -e  /home/username/bin/wsl_port_forwarding.sh
    ```
  * to delete all port forwarding: `netsh.exe interface portproxy reset`

  4. access from host PC or external PC:
      * `http://IP_address_of_host_or_hostname:80`

  * to check listen ports in Host
      ```
      netstat -ano | grep LISTEN
      ```

# Dify Setting

### LLM setting
- Settings —> Model Providers,  to add and configure the LLM
- when endpoint is local, 
  - endpoint server listen 0.0.0.0
  - specify endpoint as IP addr of host: http://IP_of_host:port/   
### Others
- Settings -> languages -> timezone

### User Account for community version
- login with mail address and password
- 

# Text Embedding Model (for RAG)

### ruri-large model
https://docs.dify.ai/en/development/models-integration/ollama#integrate-local-models-deployed-by-ollama
1. install ollama in Windows
    * -> start Ollama in background
2. change listen address:  default localhost -> 0.0.0.0
    1. click Ollama icon in task tray
    2. click Setting -> Check "Expose Ollama to the network"
3. install uri-large model
    ```powershell
    # download
    ollama pull kun432/cl-nagoya-ruri-large
    ollama list  # list pulled models
    # start running model
    curl http://localhost:11434/api/embed -Method Post -ContentType application/json -Body '{
      "model": "kun432/cl-nagoya-ruri-large",
      "input": "文章: 日本のAI技術の進展について教えてください。"
    }'
    # check models running
    ollama ps
    # stop model
    ollama stop kun432/cl-nagoya-ruri-large
    ```
5. Setting Firewall
      ```powershell
      # set firewall
      netsh advfirewall firewall add rule name="★Ollama TCP 11434" dir=in action=allow protocol=TCP localport=11434 profile=private,domain
      # show firewall
      netsh advfirewall firewall show rule name="★Ollama TCP 11434"
      # delete firewall
      netsh advfirewall firewall delete rule name="★Ollama TCP 11434"
      ```
6. Ollama starts an API service at:
    * default: `http://localhost:11434`
    * setting OLLAMA_HOST: `http://$OLLAMA_HOST:11434`

# MCP server
https://docs.dify.ai/ja-jp/plugins/best-practice/how-to-use-mcp-zapier
https://zenn.dev/upgradetech/articles/24a7d76133af4c
