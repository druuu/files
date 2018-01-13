#!/bin/bash

capacity=`cat /sys/class/power_supply/BAT0/capacity`
status=`cat /sys/class/power_supply/BAT0/status`
notification="Capacity: ${capacity}%"
#acpi_time=`acpi | sed -n 's/\(.*%, \(.*\) until .*\)\|\(.*%, \(.*\) .*\)/\2\4/p'`

if [ $status == 'Discharging' ]
then
    if [ $capacity -le 7 ]
    then
        echo mem > /sys/power/state
    fi
    if [ $capacity -le 35 ]
    then
        /usr/local/bin/stn -i -g 25x1+1187 -e /root/.config/stn_bat.sh " bat discharging: $capacity%" &
    fi
elif [ $capacity -ge 85 ]
then
    /usr/local/bin/stn -i -g 25x1+1187 -e /root/.config/stn_bat.sh " bat charging: $capacity%" &
fi
