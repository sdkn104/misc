# RDP to GCE of linux (xfce)

## install xfce
https://cloud.google.com/architecture/chrome-desktop-remote-on-compute-engine?hl=ja

sudo DEBIAN_FRONTEND=noninteractive apt install --assume-yes xfce4 desktop-base dbus-x11 xscreensaver

#sudo systemctl disable lightdm.service

ファイアウォールの設定 必要に応じて、ファイアウォールで3389ポートを開放します。
sudo ufw allow 3389/tcp

再起動 設定を反映させるために、システムを再起動します。
sudo reboot

## install Chrome
curl -L -o google-chrome-stable_current_amd64.deb \
https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install --assume-yes --fix-broken ./google-chrome-stable_current_amd64.deb

# install XRDP
https://qiita.com/shkik/items/54ac74072f66645dc1d2

sudo apt install xrdp

xrdpサービスの開始と有効化 インストールが完了したら、xrdpサービスを開始し、自動起動を有効にします。
sudo systemctl start xrdp
sudo systemctl enable xrdp

ファイアウォールの設定 必要に応じて、ファイアウォールで3389ポートを開放します。
sudo ufw allow 3389/tcp

xrdpの設定 xrdpがxfceを使用するように設定します。以下のコマンドを実行して、xrdpの設定ファイルを編集します。
echo "startxfce4" > ~/.xsession

再起動 設定を反映させるために、システムを再起動します。
sudo reboot

リモートデスクトップ接続 Windowsのリモートデスクトップ接続（RDPクライアント）を使用して、UbuntuマシンのIPアドレスを指定して接続します。ユーザー名とパスワードを入力すると、リモートデスクトップが表示されます。
