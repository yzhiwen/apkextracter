#!/bin/bash

function startup() {
    find $EXTRACT_DIR -iname '*.smali' |
      xargs grep -l ".class [a-zA-Z ]* $APK_PACKAGE_REF[a-zA-Z0-9_/]*;" | 
       xargs -l awk '
            BEGIN {
                fCount = 0; # field字段数量
                fPrivateCount = 0; # private field字段数量
                fRawPrivateCount = 0; # raw private field字段数量
                mCount = 0; # method方法数量
                mPrivateCount = 0; # private method方法数量
                mRawPrivateCount = 0; # raw private method方法数量
            }

            END {
                if(exited) { } 
                else {
                    if(length(clazz) > 0) {
                        printf("%s,%s,%s,%s,%s,%s,%s\n",fRawPrivateCount, fPrivateCount, fCount, mRawPrivateCount, mPrivateCount, mCount, clazz)
                    }
                }
            }

            ### 包含interface `.class public interface`
            $1 ~ /\.class/ { 
                clazz = $NF
                if(length(clazz) == 0) {
                    exit (exited = 1)
                }
            }

            ### parse `.field private static final STATE_IDLE:I;`
            $1 ~ /\.field/ && $NF ~ /.*:.*/ { parseField($NF) }

            ### parse `.field private static final STATE_IDLE:I = 0x0`
            $1 ~ /\.field/ && $NF !~ /.*:.*/ && $(NF-2) ~ /.*:.*/ { parseField($(NF-2)) }

            function parseField(str) {
                isPrivate = $2 == "private"
                len=split(str, result, ":")
                if(len <= 1) {
                    print "error", clazz, $0
                    return;
                } else {
                    field = result[1]
                }

                fCount += 1;
                if(isPrivate) fPrivateCount += 1
                #TODO this$0情况
                if(isPrivate && !isConfusion(field)) fRawPrivateCount += 1;
            }

            ### 或 `|` -> `\|`
            $1 ~ /\.method/ && $NF !~ /<clinit>.*\|<init>.*/ {
                isPrivate = $2 == "private"
                len=split($NF, result, "(")
                if(len <= 1) {
                    print "error", clazz, $0
                    next # not return 
                } else {
                    method = result[1]
                }
                mCount += 1;
                if(isPrivate) mPrivateCount += 1;
                if(isPrivate && !isConfusion(method)) mRawPrivateCount += 1
            }

            function isConfusion(field) {
                len=length(field)
                return len > 0 && len <= 3;
            }
        '
}

function HELP() {
cat <<EOF
Usage: 
    $(basename "$0") [options] apk

Options:
    -v --viz                    confusion scan result visualization 
    -p --package [package]      specify the scan package name, '.' is all (default: apkpackage name)
EOF
}

options=$(getopt -u -o vph -l viz,package,help -- $@)
[ $? != 0 ] && echo "getopt error ..." && exit 2
set -- $options

while true; do
    case $1 in
        -v|--viz)
            VIZ=1;;
        -p|--package)
            shift
            [ -z $2 ] && echo "need package name" && exit 2
            if [ $2 == "." ]; then
                APK_PACKAGE_REF=$2
            else
                APK_PACKAGE_REF=L$(echo $2 | sed "s/\./\//g") # La/b/c
            fi
            ;;
        -h|--help)
            HELP && exit 0;;
        *)
            break;;
    esac
    shift
done
shift && [ $# == 0 ] && echo "missing file..." && exit 2

. common && apkdecode $1
[ $? != 0 ] && HELP && exit 2
[ ! -d $EXTRACT_DIR ] &&  HELP && exit 2
[ -z $APK_PACKAGE_REF ] && apkpackageref $1

start=$(date +%s)
if [ $VIZ == 1 ]; then
    startup > laboratory/viz/dist/staticfile
    echo Time taken to execute commands is $(($(date +%s) - start )) seconds. # end=$(date +%s)
    cd laboratory/viz && sh startup
    cd ../..
else
    startup
    echo Time taken to execute commands is $(($(date +%s) - start )) seconds. # end=$(date +%s)
fi