#!/bin/bash

# status graph:
# old.apk       new.apk    status  
#   []      ->  [file]      add
#   [file]  ->  []          del
#   [file]  ->  [file]      modify(modify same filename)

function HELP() {
cat <<EOF
Usage: $(basename "$0") [options] oldapk newapk
EOF
}

[ -e _TEMPFILE ] && rm _TEMPFILE
touch _TEMPFILE

[[ ! -f $1 ]] && HELP && exit 2
[[ ! -f $2 ]] && HELP && exit 2
zipinfo -l $1 >> _TEMPFILE
zipinfo -l $2 >> _TEMPFILE

awk '
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
        if(file in old) {
            if(size != old[file]) modify[file] = size - old[file]
            delete old[file]
        } else {
            add[file] = size
        }
    }

    END {
        for(item in add) print "\033[32m [A]", item, add[item]
        for(item in old) print "\033[31m [D]", item, old[item]
        for(item in modify) printf "\033[33m [M] %s %s\n", item, modify[item]
        printf("\033[32m add: %s, \033[31m delete: %s, \033[33m modify: %s\n", length(add), length(old), length(modify))
    }
' _TEMPFILE

rm _TEMPFILE