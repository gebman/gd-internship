#!/usr/local/bin/bash
# Write script with following functionality:
# If -v tag is passed, replaces lowercase characters with uppercase and vise versa
# If -s is passed, script substitutes <A_WORD> with <B_WORD> in text (case sensitive)
# If -r is passed, script reverses text lines
# If -l is passed, script converts all the text to lower case
# If -u is passed, script converts all the text to upper case
# Script should work with -i <input file> -o <output file> tags

while getopts "i:o:vs:rlu" args; do
    case ${args} in

    i)
        infile=$OPTARG;;
    o)
        outfile=$OPTARG;;
    v)
        v_flag=1;;
    s)
        s_flag=1
        s_string=($OPTARG);;
    l)
        l_flag=1
        if [[ -n $v_flag ]] || [[ -n $u_flag ]]; then
            echo "Error: conflicting flags (-v -l -u)"
            exit 1
        fi;;
    r)
        r_flag=1;;
    u)
        u_flag=1
        if [[ -n $v_flag ]] || [[ -n $l_flag ]]; then
            echo "Error: conflicting flags (-v -l -u)"
            exit 1
        fi;;
    esac
done
rm -f $outfile
touch $outfile
while read -r line; do

    if [[ -n $s_flag ]]; then
        line="${line/${s_string[0]}/${s_string[1]}}"
    fi
    if [[ -n $v_flag ]]; then
        line="${line~~}"
    fi
    if [[ -n $l_flag ]]; then
        line="${line,,}"
    fi
    if [[ -n $u_flag ]]; then
        line="${line^^}"
    fi
    if [[ -n $r_flag ]]; then
        line=`echo $line | rev`
    fi
    echo $line >> $outfile

done <$infile