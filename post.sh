#!/bin/sh

pacman -S base-devel openssh gksu xorg-server xf86-input-synaptics neovim xorg-xinit xf86-video-ati compton xautolock xdotool xbindkeys git firefox feh cron vim libxft xorg-xfd mpv alsa-utils &&
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

cd suckless/st && make clean install &&
cd ../dwm && make clean install &&
cd ../slock-1.2 && make clean install &&
cd ../../ &&
cp shell/bashrc /root/.bashrc &&
cp x/xinitrc /root/.xinitrc &&
ls /root/.config || mkdir /root/.config
cp x/compton.conf /root/.config/ &&

yaourt_conf='[archlinuxfr]
SigLevel = Never
Server = http://repo.archlinux.fr/$arch' &&
echo "$yaourt_conf" >> /etc/pacman.conf
pacman -Syu &&
pacman -S yaourt &&
echo 'remove yaourt from pacman conf' &&
useradd dinesh && passwd dinesh &&
usermod -aG wheel dinesh
