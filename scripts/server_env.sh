#!/bin/sh

run(){
    wdir=`pwd` &&
    tmp_dir=`mktemp -d` &&
    cd "$tmp_dir" &&
    curl -s -o server_vimrc 'https://raw.githubusercontent.com/druuu/files/master/vi/server_vimrc' &&
    alias vi="vim -u ${tmp_dir}/server_vimrc" &&
    PS1='\[\e[0;15m\]\h \[\e[0;34m\]${VIRTUAL_ENV##*/} \[\e[0;33m\]\W\[\e[0m\] \[\e[0;15m\]' &&
    set -o vi &&
    export TERM=xterm-256color &&
    export EDITOR=vi &&
    export VIRTUAL_ENV_DISABLE_PROMPT=1 &&
    alias ls='ls --color' &&
    LS_COLORS=$LS_COLORS:'di=0;94' ; export LS_COLORS &&
    alias ll='ls -lash' &&

	cd "$wdir"
} &&

run
