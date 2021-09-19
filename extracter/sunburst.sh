#!/bin/bash

function parse() {
    zipinfo -l alitrip_android_600000.apk | awk -f ss.awk
}