#!/bin/sh

#datetime
timedatectl set-timezone Asia/Kolkata &&
ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime &&


pacman -S base-devel openssh gksu xorg-server xf86-input-synaptics neovim xorg-xinit xf86-video-ati compton xautolock xdotool xbindkeys git firefox feh cron vim libxft xorg-xfd mpv alsa-utils redshift python-virtualenv python2-virtualenv ranger nload zip unzip tk xorg-xmodmap webkitgtk2 dmenu xorg-xprop &&
pacman -Rdd noto-fonts &&

git clone 'https://github.com/druuu/files.git' &&
cd files && 

#silent boot
echo 'kernel.printk = 3 3 3 3' > /etc/sysctl.d/20-quiet-printk.conf &&
echo '[[ $(fgconsole 2>/dev/null) == 1 ]] && exec startx -- vt1 &> /dev/null' > /root/.bash_profile &&
cmp orig/mkinitcpio.conf /etc/mkinitcpio.conf &&
cmp orig/systemd-fsck-root.service /usr/lib/systemd/system/systemd-fsck-root.service &&
cmp 'orig/systemd-fsck@.service' '/usr/lib/systemd/system/systemd-fsck@.service' &&
cp mod/mkinitcpio.conf /etc/ &&
mkinitcpio -p linux &&
cp mod/systemd-fsck-root.service /etc/systemd/system/ &&
cp 'mod/systemd-fsck@.service' /etc/systemd/system/ &&
cp -r 'mod/getty@tty1.service.d' /etc/systemd/system/ &&
touch ~/.hushlogin


#fonts
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
cp scripts/reset_xmodmap /root/.config/ &&
cp scripts/ram.py /root/.config/ &&

cd suckless/surf-0.7 && make clean install &&
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
