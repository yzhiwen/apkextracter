#!/bin/bash

awk '
    $0 ~ /^[ ]*[A-Z0-9_]*\(/ {
        num = split($0, fs, "\"")
        op = num >= 2 ? fs[2] : ""

        num = split($0, fs, ",")
        for(item in fs) {
            start = index(fs[item], "Format.")   # `Format.Format3rmi`
            if(start == 0) continue

            len = length(fs[item])
            if(index(fs[item], ")")) len -= 1 # `RETURN(0x0f, "return", ReferenceType.NONE, Format.Format11x),`
            format = substr(fs[item], start + 7, len - 8)
            break
        }

        if(op != "" && format != "") {
            # print op, format
            # printf("Opcode(\"%s\", %s()),\n", op, format) # as list
            printf("\"%s\": Opcode(\"%s\", %s()),\n", op, op, format) # as map
        }
    }
' ../laboratory/smali/dexlib2/src/main/java/org/jf/dexlib2/Opcode.java
# https://github.com/JesusFreke/smali/raw/master/dexlib2/src/main/java/org/jf/dexlib2/Opcode.java