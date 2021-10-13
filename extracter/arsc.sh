#!/bin/bash

which aapt2 || exit 2
# which apktool || exit 2

function parseResInArsc() {
    awk '$0 ~ /^    resource/ { print $2 }' arsc/arscdump
}

function parseResFieldInCode() {
    # 生成 R$ class ref 到 R$ file path 映射文件 <LxxxR$xxx, file>

    # 抽取R文件filed。Lcom/example/feedback_impl/R$drawable;->im_e76:I 0x7f021643
    find $EXTRACT_DIR -iname 'R$*.smali' | xargs -l \
        awk '$1 ~ /^\.class$/ { ref = $4; } $0 ~ /^\.field public static final .*:I = 0x7f.*/ { printf("%s->%s %s\n", ref, $5, $7) }' | \
            sort -u > arsc/_rinxml

    # 从代码中找到存在R$文件的引用，再根据rfields映射文件转换成对应十六进制值
    find $EXTRACT_DIR ! -iname 'R$*.smali' -iname '*.smali' | xargs \
        grep -h -o "L.*R$.*;->.*:I" |  # 性能：其中xargs -l grep 一个一个file传入grep会变得很慢
            # uniq | # sort -u 有点慢，是等到所有数据读完才处理估计，而且目前并不需要排序，因此使用uniq
                xargs -I {} grep {} arsc/_rinxml |
                    cut -d " " -f2

    rm arsc/_rinxml
}

function parseResValueInCode() {
    find $EXTRACT_DIR ! -iname 'R$*.smali' -iname '*.smali' | 
        xargs grep -h -o "0x7f.\{6\}$" |
            uniq
}

function parseResFieldInXml() {
    find $EXTRACT_DIR -name '*.xml' | xargs \
        grep -h -o '@[a-zA-Z0-9_:]*/[a-zA-Z0-9_]*' | 
            sort -u | cut -b2- | sort -u > arsc/_rinxml
    
    grep "resource 0x" arsc/arscdump | 
        grep -w -f arsc/_rinxml | 
            awk '{ print $2 }' 
            # | sort -u > out/resInXml
    
    rm arsc/_rinxml
}

function uselessr() {
    aapt2 dump resources $EXTRACT_FILE > arsc/arscdump # arsc/arscdump also for the next step
    parseResInArsc | sort -u > arsc/resInArsc

    parseResFieldInCode > arsc/resFieldValueInCode
    parseResValueInCode > arsc/resValueInCode
    parseResFieldInXml > arsc/resFieldInXml
    cat arsc/resFieldValueInCode arsc/resValueInCode arsc/resFieldInXml | sort -u > arsc/resInUsed

    comm -23 arsc/resInArsc arsc/resInUsed > arsc/ruseless

    # parseUnusedRes2Name
    grep "resource 0x" arsc/arscdump | grep -f arsc/ruseless | awk '{ print $3,$2 }'
}

function groupUnusedRes() {
    # 未使用资源类型分类
    uselessr > arsc/__ && \
        cat arsc/__ | cut -d "/" -f1 | uniq -c
    rm arsc/__
}

function HELP() {
cat <<EOF
Usage: $(basename "$0") [options] apk
EOF
}

. common && apkdecode $1
[ ! -f $EXTRACT_FILE ] && HELP && exit 2
[ ! -d $EXTRACT_DIR ] && HELP && exit 2

[ ! -d arsc ] && mkdir arsc

# print useless R field in code and xml
echo "extract resource less value ..." && uselessr