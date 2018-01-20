#compdef sshch
#
# ZSH Completion for SSHCH
# Usage:
#  1) Place File in a Directory where ZSH can find it
#     -> Search Path is Stored in $fpath
#     -> echo $fpath
#  2) Rename File to '_sshch'
#
_arguments '::aliasname:->getAlias' \
	   '-e[Edit Alias]:aliasname:->getAlias' '--edit[Edit Alias]:aliasname:->getAlias' \
	   '-p[Set Password]:aliasname:->getAlias' '--password[Set Password]:aliasname:->getAlias' \
	   '-r[Remove Alias]:aliasname:->getAlias' '--remove[Remove Alias]:aliasname:->getAlias' \
	   '-k[Keep Connection]:aliasname:->getAlias' '--keep[Keep Connection]:aliasname:->getAlias' \
           '-a[Add Alias]'     '--add[Add Alias]'\
           '-c[Add Command for Executing Alias]'     '--command[Add Command for Executing Alias]'\
           '-h[Show Help Message]'     '--help[Show Help Message]'\
           '-l[List Existing Alias]' '--list[List Existing Alias]'\
           '-f[List Existing Alias with Connection String]' '--fulllist[List Existing Alias with Connection String]'\
           '--version[Show Program Version]'
case "$state" in
    getAlias)
        local -a alias_list
        alias_list=($(sshch -l))
	_values -s ' '  'Aliases' $alias_list
        ;;
esac
