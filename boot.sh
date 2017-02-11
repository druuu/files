#!/bin/sh

boot_dev='/dev/sda1' &&
swap_dev='/dev/sda2' &&
root_dev='/dev/sda3' &&
home_dev='/dev/sda4' &&

mkfs.vfat -F32 "$boot_dev" &&
mkswap "$swap_dev" &&
swapon "$swap_dev" &&
mkfs.ext4 "$root_dev" &&

mount "$root_dev" /mnt &&
mkdir /mnt/boot &&
mount "$boot_dev" /mnt/boot &&

pacstrap -i /mnt base &&
genfstab -U -p /mnt >> /mnt/etc/fstab &&
cat /mnt/etc/fstab &&
arch-chroot /mnt /bin/bash
