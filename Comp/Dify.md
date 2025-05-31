## INSTALL
https://docs.dify.ai/ja-jp/getting-started/install-self-hosted/docker-compose

### Install WSL2
https://docs.docker.com/desktop/setup/install/windows-install/#wsl-2-backend

```powershell
wsl --list --online
wsl --install Ubuntu
```

### Install Docker Engine on WSL2
https://docs.docker.com/desktop/setup/install/linux/

1. install docker engine  (Docker Desktop is not free)
    - install using the apt repository
      https://docs.docker.com/engine/install/ubuntu/
1. install docker compose
    - follow installation instruction for linux
      https://docs.docker.com/compose/install/linux/#install-using-the-repository
      ```
      sudo apt-get update
      sudo apt-get install docker-compose-plugin
      ```
### install dify
https://docs.dify.ai/ja-jp/getting-started/install-self-hosted/docker-compose

```
# install
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env
# invoke dify
docker compose up -d
# -> open with browser http://localhost
```    

* (for error) 
  ```
  sudo usermod -aG docker $(whoami) 
  # to be belong to group docker
  ```

