#!/bin/sh

timedatectl set-timezone Asia/Kolkata &&
ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime &&

pacman -S base-devel openssh gksu xorg-server xf86-input-synaptics neovim xorg-xinit xf86-video-ati compton xautolock xdotool xbindkeys git firefox feh cron vim libxft xorg-xfd mpv alsa-utils redshift python-virtualenv python2-virtualenv ranger nload zip unzip tk &&
pacman -Rdd noto-fonts &&

git clone 'https://github.com/druuu/files.git' &&
cd files && 
rm /usr/share/fonts/* -r &&
cp fonts/druuu.ttf /usr/share/fonts/ &&
cp fonts/DaxRegular.ttf /home/dinesh/.fonts/ &&

cp x/70-synaptics.conf /etc/X11/xorg.conf.d/ &&

mkdir /root/.config/nvim &&
cp vi/init.vim /root/.config/nvim/ &&
cp vi/vimrc /root/.vimrc &&
cp vi/colors /root/.config/nvim/ -r &&
cp vi/xmodmap_vi.sh /root/.config/ &&

cp scripts/tnt /root/.config/tnt -r &&
#TODO install scron from aur
cp scripts/crontab /etc/ &&

cp scripts/xmodmap /root/.config/ &&
cp scripts/xmodmap1 /root/.config/ &&
cp scripts/ram.py /root/.config/ &&

cd suckless/st && make clean install &&
cd ../dwm && make clean install &&
cd ../slock-1.2 && make clean install &&
cd ../../ &&
cp shell/bashrc /root/.bashrc &&
cp x/xinitrc /root/.xinitrc &&
ls /root/.config || mkdir /root/.config
cp x/compton.conf /root/.config/ &&

#TODO better way to install packer
yaourt_conf='[archlinuxfr]
SigLevel = Never
Server = http://repo.archlinux.fr/$arch' &&
echo "$yaourt_conf" >> /etc/pacman.conf
pacman -Syu &&
pacman -S yaourt &&
echo 'remove yaourt from pacman conf' &&
useradd dinesh && passwd dinesh &&
usermod -aG wheel dinesh
