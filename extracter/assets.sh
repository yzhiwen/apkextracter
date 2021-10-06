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
Usage: $(basename "$0") [options] apk
EOF
}

# the dir need apk/assets and smali, now decode by apktool
. common && apkdecode $1
[ $? != 0 ] && HELP && exit 2
[ ! -d $EXTRACT_DIR ] &&  HELP && exit 2
echo "extract assetless file ..." && uselessAssetFile