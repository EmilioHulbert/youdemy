# Enable core color features natively
autoload -U colors && colors
setopt PROMPT_SUBST

# ==============================================================================
# BASH HISTORY ACCELERATOR & INTEGRATION
# ==============================================================================
# Tell Zsh to use your legacy Bash data alongside new shell execution steps
HISTFILE=~/.bash_history
SAVEHIST=5000
HISTSIZE=5000

# Optimization tags to make search fast and avoid repeating commands
setopt append_history
setopt extended_history
setopt hist_expire_dups_first
setopt hist_ignore_dups
setopt hist_ignore_space
setopt share_history

# ==============================================================================
# ULTIMATE NATIVE ASYNC ZSH TICKER ENGINE (NO WRAP GLITCH / EXCITING STYLING)
# ==============================================================================
_zsh_live_clock_ticker() {
    # Check if the terminal is sitting completely idle waiting for input
    if [[ "$PENDING" -eq 0 ]]; then
        # Redraw the prompt layout cleanly without disrupting what you are typing
        zle reset-prompt
    fi
}

# Register the clock function inside Zsh's native time loop subsystem
zle -N _zsh_live_clock_ticker
TMOUT=1
trap '_zsh_live_clock_ticker' ALRM

# 100% exact translation of your layout profile swapping '%' back to the native '$'
PROMPT=$'%F{red}┌──[%F{yellow}%D{%a %b %d} %D{%L:%M:%S %p}%F{red}][%F{white}%n%F{yellow}@%F{cyan}%m%F{red}]─[%F{green}%~%F{red}]\n└──╼%F{cyan}[ZERODIUM]%F{yellow}\# %f'
# ==============================================================================

# Core Navigation Framework Aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias dir='dir --color=auto'
    alias vdir='vdir --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

alias ll='ls -lh'
alias la='ls -lha'
alias l='ls -CF'
alias em='emacs -nw'

# Security Framework Superuser Privileges
alias _='sudo'
alias _i='sudo -i'
alias fucking='sudo'
alias please='sudo'

# Custom Functions & Decoders
function hex-encode() { echo "$@" | xxd -p; }
function hex-decode() { echo "$@" | xxd -p -r; }
function rot13() { echo "$@" | tr 'A-Za-z' 'N-ZA-Mn-za-m'; }

alias venv='source /home/user/Desktop/venv/bin/activate'
alias cleanpaste="xclip -o | tr -d '\n' | xclip -selection clipboard"

# Native completion framework configuration
autoload -Uz compinit
compinit

