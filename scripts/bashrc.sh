#!/bin/bash

xdotool type --delay 0 "PS1='\[\e[1;38m\]\h \[\e[38;5;27m\]\W\[\e[0m\] \[\e[1;38m\]' export TERM=linux" &&
xdotool key 'Return'
