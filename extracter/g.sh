#!/bin/bash

function parsePng() {
    for png in $*; do
        bin/png/pngcheck -vt $png | awk '
            $0 ~ /File:/ { file = substr($2, 0); size = substr($3, 2) }
            $0 ~ /chunk/ { chunk = $2; }
            { if(chunk ~ /IHDR/) { width = $1; height = $3; colorspace = sprintf("%s-%s",$5, substr($6,0, length($6)-1)); } }
            END { printf("%s %s %s %s %s %s\n", width, height, "png", colorspace, size, file) }'
    done
}

function parseJpeg() {
    for jpeg in $*; do
        jpeginfo $jpeg | awk '{ print $2, $4, "jpeg", $5"RGB", $8, $1 }'
    done
}

function parseWebp() {
    for webp in $*; do
        _webpinfo=$(webpinfo -summary $webp | awk '
            # https://developers.google.com/speed/webp/docs/riff_container
            # Chunk type  :  VP8 VP8L VP8X ALPH ANIM ANMF(VP8 /VP8L/ALPH) ICCP EXIF  XMP
            $0 ~ /File:/ { file = $2 }
            $0 ~ /File size/ { size = $3 }

            $0 ~ /Canvas size/ {
                if($3 > width) width = $3;
                if($5 > height) height = $5;
            }

            $0 ~ /Width:/ {
                if($2 > width) width = $2;
            }

            $0 ~ /Height:/ {
                if($2 > height) height = $2;
            }

            $0 ~ /^Chunk counts:/ {
                if($5 > 0 && $7 > 0) {
                    type = "animated-webp"; # VP8X：扩展格式，有ANIM则为动态，否则为静态\
                    if($9 > 0 && $10 > 0) colorspace = "mux";
                    else if($9 > 0) colorspace = "yuv";
                    else if($10 > 0) colorspace = "rgba";
                    else colorspace = "-";
                } else if($3 > 0) {
                    type = "Lossy-webp"; # VP8
                    colorspace = "yuv"; # yuv420
                } else if($4 > 0) {
                    type = "lossess-webp"; # VP8L
                    colorspace = "rgba"; # maybe color index
                } else {
                    type = "-";
                    colorspace = "-";
                }
            }

            END {
                if(width && height && type) {
                    print width, height, type, colorspace, size, file
                }
            }
        ')
        if [ "$_webpinfo" ]; then
            echo "$_webpinfo"
        else
            # echo "error parse $file"
            echo ""
        fi
    done
}

################################## png optimizable ##################################

# 查找png文本chunk跟辅助chunk数量
# outputformat: textualChunk ancillaryChunk file
# ref: http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html
function extractPngChunk() {
    for png in $*; do
        bin/png/pngcheck -cvt $png | awk '
            BEGIN { ancillaryChunk = 0; textualChunk = 0; textualSize = 0;  }
            $0  ~ /File:/ { file = $2 }
            $0 ~ /^[ ]*chunk/ && $0 !~ /IHDR|PLTE|IDAT|IEND/ { ancillaryChunk++ }
            $0  ~ /tEXt|zTXt|iTXt/ { textualChunk++; textualSize+=$7 }
            END { printf("%s (textsize:%s) %s (ancillary) %s\n", textualChunk, textualSize, ancillaryChunk, file) }
        '
    done
}

function extractLossLessPng() {
    sum=0
    for png in $*; do
        output="_`basename $png`"
        optipng -nx -o7 -backup -quiet $png -out $output
        if [ $? ]; then
            inputSize=`du $png | cut -f1`
            outputSize=`du $output | cut -f1`
            reduceSize=`echo "$inputSize-$outputSize" | bc`
            sum=`echo $sum+$reduceSize | bc`
            echo "$reduceSize $inputSize $outputSize $png"
        else
            echo 'optipng error with $png'
        fi

        rm -f $output
    done
    echo "lossless png maybe space: $sum"
}

######################################### arguments #########################################

function HELP() {
cat <<EOF

Usage: 
    $(basename "$0") [options] file

file:
    apk/zip/dir

png options:
    -p --png                extract png file
    --pngchunk              parse png ancillary chunk info
    --pngll                 search png lossless space (eg. slow)
    --png2webp              [todo] lossy options...

webp options:
    -w --webp               extract webp file
    --webploss              compress webp loss space
    --png2png8              [todo]

jpeg options:
    -j --jpeg               extract jpeg file
    --jpeg2webp             [todo]

other options:
    -s --size               fliter file size, the find command -size (eg. +10k is >=10kb)
    -q --quality <int>      lossy options, default 95
    -b --benifit <int>      lossy options, default 15 (eg. benifit with 15%)
EOF
}

# -u Do not quote the output. 其他的参数不会被单引号包裹
options=$(getopt -u -o pwjhs:q:b: -l png,pngchunk,pngll,png2webp,webp,webploss,webp2png8,jpeg,jpeg2webp,size:,quality:,benifit:,help -- $@)
if [ $? != 0 ]; then
    exit 2;
fi
set -- $options

while true; do
    case $1 in
        -p|--png)
            PNG="true"
            ;;
        --pngchunk)
            PNGCHUNK="true" # "" or !""
            ;;
        --pngll)
            PNGLOSSLESS="true"
            ;;
        --png2webp)
            PNG2WEBP="true"
            ;;
        -w|--webp)
            WEBP="true"
            ;;
        --webp2png8)
            WEBP2PNG8="true"
            ;;
        --webploss)
            WEBPLOSS="true";;
        -j|--jpeg)
            JPEG="true"
            ;;
        --jpeg2webp)
            JPEG2WEBP="true"
            ;;
        -s|--size)
            FLITER_SIZE=$2
            shift
            ;;
        -q|--quality)
            (( $2 >= 100 || $2 <= 0)) && echo "the -q|--quality must be in (0, 100)" && exit 2
            FLITER_QUQLITY=$2
            shift
            ;;
        -b|--benifit)
            (( $2 >= 100 || $2 <= 0)) && echo "the -b|--benifit must be in (0, 100)" && exit 2
            FLITER_BENIFIT=$2
            shift
            ;;
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

# which jpeginfo
[ -z $FLITER_SIZE ] && FLITER_SIZE="+0"

if [ $PNG ]; then
    pngs=`find $EXTRACT_DIR -name '*.png'`
    parsePng $pngs
elif [ $PNGCHUNK ]; then
    pngs=`find $EXTRACT_DIR -name '*.png'`
    extractPngChunk $pngs
elif [ $PNGLOSSLESS ]; then
    pngs=`find $EXTRACT_DIR -name '*.png'`
    extractLossLessPng $pngs
elif [ $PNG2WEBP ]; then
    echo "[todo]png2webp maybe need wait"
fi

if [ $JPEG ]; then
    jpegs=`find $EXTRACT_DIR -regex '.*\(jpeg\|jpg\)'`
    parseJpeg $jpegs
elif [ $JPEG2WEBP ]; then
    echo "[todo]jpeg2webp maybe need wait"
fi

[ $WEBP ] && parseWebp `find $EXTRACT_DIR -name '*.webp' -size $FLITER_SIZE`
[ $WEBP2PNG8 ] && echo "[todo]webp2png8 maybe need wait"

# Animated WebP file is not supported.
if [ $WEBPLOSS ]; then
    webps=`find $EXTRACT_DIR -name '*.webp' -size $FLITER_SIZE`
    for webp in $webps; do
        result=`python3 ssim.py -v $webp`
        if [[ $result == "True" ]]; then
            echo "ture in $webp"
        else
            echo "false in $webp"
        fi
    done
fi