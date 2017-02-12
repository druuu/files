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
        python /home/random/code/tnt/notify.py $notification
    fi
elif [ $capacity -ge 80 ]
then
    python /home/random/code/tnt/notify.py $notification
fi
