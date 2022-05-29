#!/bin/python
"""
    Takes in a parsed lpc dump and removes the hex dump
"""
import sys

hide = False
for line in sys.stdin:
    if (line.isspace()):
        print(line, end='')
        hide = False
    elif line[0] == "#":
        print(line, end='')
        hide = True
    elif not hide:
        print(line, end='')
