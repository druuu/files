#!/bin/bash

capacity=`cat /sys/class/power_supply/BAT1/capacity`
status=`cat /sys/class/power_supply/BAT1/status`
notification="Capacity: ${capacity}%"
#acpi_time=`acpi | sed -n 's/\(.*%, \(.*\) until .*\)\|\(.*%, \(.*\) .*\)/\2\4/p'`

if [ $status == 'Discharging' ]
then
    if [ $capacity -le 7 ]
    then
        echo mem > /sys/power/state
    fi
    if [ $capacity -le 40 ]
    then
        st -i -g 20x1+1225 -e ~/.config/stn.sh "bat discharging: $capacity" &
    fi
elif [ $capacity -ge 80 ]
then
    st -i -g 20x1+1225 -e ~/.config/stn.sh "bat charging: $capacity" &
fi
