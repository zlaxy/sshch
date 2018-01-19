_sshch_complete()
{
        local cur_word alias_list
        cur_word="${COMP_WORDS[COMP_CWORD]}"
        alias_list=`sshch -l`
        COMPREPLY=($(compgen -W "$alias_list" -- $cur_word))
        return 0
}

complete -F _sshch_complete sshch

