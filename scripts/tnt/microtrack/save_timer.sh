#!/bin/bash

app_dir='/opt/microtrack' &&
activity_file='/root/.microtrack/activity.txt' &&

#cat /opt/microtrack/timer_fifo | stdbuf -o0 -e0 -i0 sed -n "s/\(.*\)/\1 $1/p" >> $activity_file

while true
do
    read action </opt/microtrack/timer_fifo;
    if [ "$action" == "show_main" ]; then
        xwid="$(xdotool search -name mt_8ca0681d11ae4e0c9e9fd6d2ba038104)"
        xdotool windowmap $xwid
    else
        echo $action | stdbuf -o0 -e0 -i0 sed -n "s/\(.*\)/\1 $1/p" >> $activity_file
    fi
done
