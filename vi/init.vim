"syntax on
"colorscheme druuu

filetype on
filetype plugin on
filetype plugin indent on

set laststatus=0
set backspace=indent,eol,start
set expandtab           " enter spaces when tab is pressed
set tabstop=4           " use 4 spaces to represent tab
set softtabstop=4
set shiftwidth=4        " number of spaces to use for auto indent
set autoindent          " copy indent from current line when starting a new line
set pastetoggle=<F10>
set ignorecase      " ignore case when searching
set ruler
set mouse=
set ttyfast
set clipboard=unnamedplus
set hidden
set foldenable
set foldmethod=indent

au FileType python setl sw=4 sts=4 et
:inoremap <BS> <Nop>

"highlight MyGroup cterm=bold
"match MyGroup /./
hi clear texItalStyle
"imap <j> <left>
"imap <k> <left>
"imap <j> <left>
"imap <j> <left>
syntax off set nohlsearch set t_C
highlight Search ctermbg=gray

