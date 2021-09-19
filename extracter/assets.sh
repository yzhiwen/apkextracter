#!/bin/bash

function allconststring() {
    # ref：https://source.android.com/devices/tech/dalvik/dalvik-bytecode
    # const-string vAA, string@BBBB	参数：A: 目标寄存器（8 位）B: 字符串索引。说明：将通过给定索引指定的字符串的引用移到指定的寄存器中。
    find $EXTRACT_DIR -iname '*.smali' | \
        xargs grep 'const-string' | cut -d "," -f2 | cut -d "\"" -f2
}

function uselessAssetFile() {
    curdir=`pwd`
    assetsdir="$EXTRACT_DIR/assets"
    [ ! -e $assetsdir ] && echo "!-e" && exit 2
   
    touch _allconststring && _allstring=`realpath _allconststring`
    touch _allasset && _asset=`realpath _allasset`
    touch _allusedasset && _used=`realpath _allusedasset`

    # step 1.
    cd $assetsdir && find -type f | cut -d "/" -f2- | sort -u > $_asset && cd $curdir
    # step 2.
    allconststring | sort -u > $_allstring
    # step 3.
    cat $_asset | xargs -I {} grep -w {} $_allstring | sort -u > $_used
    # step 4.
    grep -v -f _allusedasset _allasset
    # grep -v -f _allusedasset _allasset > $_unused 
    # comm -23 $_asset $_used > $_unused

    rm _allconststring
    rm _allasset
    rm _allusedasset
}

function HELP() {
cat <<EOF
Usage: 
    $(basename "$0") [options] file

file:
    apk/dir

options:
    -u --useless            print unused asset directory file in code directly 
EOF
}

options=$(getopt -u -o uh -l useless,help -- $@)
if [ $? != 0 ]; then
    exit 2;
fi
set -- $options

while true; do
    case $1 in
        -u|--useless)
            USELESS="true";;
        -h|--help)
            HELP && exit 0;;
        *)
            break;;
    esac
    shift
done

shift && [ $# == 0 ] && echo "missing file..." && exit 2
EXTRACT_DIR=`realpath $1`
if [[ -f $EXTRACT_DIR ]]; then
    tempdir="__`basename $EXTRACT_FILE`"
    rm -rf $tempdir
    unzip $EXTRACT_FILE -d $tempdir
    EXTRACT_DIR=$tempdir
elif [ -d $EXTRACT_DIR ]; then
    EXTRACT_DIR=$1
else
    echo "input file invalid $1"
    exit 2
fi

[ $USELESS ] && uselessAssetFile