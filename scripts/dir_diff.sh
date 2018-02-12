#!/bin/bash

usage() {
    echo -e "Usage: $0 <path> <path>\n" \
            "Compare files by sha1sum in two directories\n"
    exit 0
}

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    usage
fi

diff <(pushd $1 > /dev/null && \
       find ./ -type f -print0 | xargs -0 sha1sum && \
       popd > /dev/null) \
     <(pushd $2 > /dev/null && \
       find ./ -type f -print0 | xargs -0 sha1sum && \
       popd > /dev/null)

exit 0
