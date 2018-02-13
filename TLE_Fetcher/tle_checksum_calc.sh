#!/bin/bash

function calculate_checksum {
    TLE=$(sed -e 's/-/1/g' -e 's/[^[:digit:]]//g' -e 's/./&+/g' <<< "${1:0:68}")
    checksum=$(( ${TLE}0 ))
    echo "${checksum: -1}"
}
