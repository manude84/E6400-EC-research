#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Missing filename"
	exit
fi
if [[ ! -f $1 ]]; then
	echo "$1: no such file or directory"
	exit
fi

script=$(dirname $0)

# sed command is to break up lpc cycle aborts, indicated using exclamation marks,
# onto individual lines
sed -E "s/!/\n/g" $1 | $script/parse.py | $script/remove-raw.py | $script/patterns.py | uniq > $(basename -s .txt $1)-parsed.txt
cat $(basename -s .txt $1)-parsed.txt | sed -n "/#/p" > $(basename -s .txt $1)-summary.txt
