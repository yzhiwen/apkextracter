#!/bin/bash

# status graph:
# old.apk       new.apk    status  
#   []      ->  [file]      add
#   [file]  ->  []          del
#   [file]  ->  [file]      modify(modify same filename)

function HELP() {
cat <<EOF
Usage: 
    $(basename "$0") [options] file

file:
    apk/dir

options:
    -v
    -u --useless            print unused asset directory file in code directly 
EOF
}


[ -e _TEMPFILE ] && rm _TEMPFILE
touch _TEMPFILE
zipinfo -l $1 >> _TEMPFILE
zipinfo -l $2 >> _TEMPFILE

awk '
    BEGIN {
        print ARGV[2]
    }

    $0 ~ /Archive:/ {
        if(archive == "old") archive = "new"
        else archive = "old"
    }

    archive ~ "old" && NF == 10 {
        file = $10
        size = $4
        old[file] = size
    }

    archive ~ "new" && NF == 10 {
        file = $10
        size = $4
        if(!old[file]) add[file] = size
        else {
            modify[file] = size - old[file]
            delete old[file]
        }
    }

    END {
        for(file in old) 
            printf("")
        print file
        printf("add: %s, delete: %s, modify: %s\n", length(old), length(add), length(modify))
    }
' _TEMPFILE $aaa

rm _TEMPFILE