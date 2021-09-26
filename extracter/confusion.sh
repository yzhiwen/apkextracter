#!/bin/bash

function startup() {
    find $EXTRACT_DIR -iname '*.smali' ! -iname 'R.smali' ! -iname 'R$*.smali' | \
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
                printf("%s,%s,%s,%s,%s,%s,%s\n",fRawPrivateCount, fPrivateCount, fCount, mRawPrivateCount, mPrivateCount, mCount, clazz)
            }

            ### 包含interface `.class public interface`
            $1 ~ /\.class/ { clazz = $NF }

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
    $(basename "$0") [options] file

file:
    apk/dir

options:
    --viz            print viz 
EOF
}

options=$(getopt -u -o h -l viz,help -- $@)
if [ $? != 0 ]; then
    exit 2;
fi
set -- $options

while true; do
    case $1 in
        --viz)
            VIZ=1;;
        -h|--help)
            HELP && exit 0;;
        *)
            break;;
    esac
    shift
done

shift && [ $# == 0 ] && echo "missing file..." && exit 2
EXTRACT_FILE=`realpath $1`
EXTRACT_DIR=""
if [[ -f $EXTRACT_FILE ]]; then
    EXTRACT_DIR="__`basename $EXTRACT_FILE`"
    rm -rf $EXTRACT_DIR
    bin/apk/apktool d -o $EXTRACT_DIR $EXTRACT_FILE
elif [ -d $EXTRACT_DIR ]; then
    EXTRACT_DIR=$1
else
    echo "input file invalid $1"
    exit 2
fi

start=$(date +%s)
if [[ $VIZ -eq 1 ]]; then
    echo "[TODO]"
else
    startup
fi
echo Time taken to execute commands is $(($(date +%s) - start )) seconds. # end=$(date +%s)