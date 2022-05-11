#!/bin/bash

# sed command is to break up lpc cycle aborts, indicated using exclamation marks,
# onto individual lines
sed -E "s/!/\n/g" $1 | ./parse.py | ./remove-raw.py | ./patterns.py | uniq > $(basename -s .txt $1)-parsed.txt
cat $(basename -s .txt $1)-parsed.txt | sed -n "/#/p" > $(basename -s .txt $1)-summary.txt
