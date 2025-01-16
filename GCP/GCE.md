# RDP to GCE of linux (xfce)

## install xfce
https://cloud.google.com/architecture/chrome-desktop-remote-on-compute-engine?hl=ja

sudo DEBIAN_FRONTEND=noninteractive \
    apt install --assume-yes xfce4 desktop-base dbus-x11 xscreensaver

#sudo systemctl disable lightdm.service

## install Chrome
curl -L -o google-chrome-stable_current_amd64.deb \
https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install --assume-yes --fix-broken ./google-chrome-stable_current_amd64.deb

# install XRDP
https://qiita.com/shkik/items/54ac74072f66645dc1d2

$sudo apt install -y xrdp
$sudo sed -e 's/^new_cursors=true/new_cursors=false/g' -i /etc/xrdp/xrdp.ini

