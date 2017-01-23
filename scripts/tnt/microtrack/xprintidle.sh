#!/bin/bash

pid_dir='/opt/microtrack/pid_dir'

while true
do 
    if [[ $(xprintidle) -gt 180000 ]]
    then
        echo 'quit' > mt_fifo
    else
        sleep 1
    fi
done
