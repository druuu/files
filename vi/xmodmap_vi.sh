#/bin/bash

xmodmap -e "keycode 9 = Caps_Lock" > /dev/null 2>&1 &
xmodmap -e 'clear Lock' -e 'keycode 0x42 = Escape' > /dev/null 2>&1 &
