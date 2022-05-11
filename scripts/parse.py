#!/bin/python
"""
    Parses the raw LPC cycle hex dumps and produces human readable
    descriptions of each cycle. Also adds blank lines to separate
    groups of similar port addresses
"""
import sys
import re

subs = {
    r"(.*?02(.{4})([\dA-F])([\dA-F]).*)": r"\1\tWrite 0x\4\3 port 0x\2",
    r"(.*?00(.{4}).*?0([\dA-F])([\dA-F]).*)": r"\1\tRead 0x\4\3 port 0x\2"
}
ports = {
    0x002E: {"group": 0},
    0x002F: {"group": 0},
    0x0060: {"group": 1},
    0x0064: {"group": 1},
    0x0080: {"group": 2},
    0x0084: {"group": 2},
    0x0086: {"group": 2},
    0x008C: {"group": 2},
    0x02FA: {"group": 3},
    0x02FC: {"group": 3},
    0x037A: {"group": 4},
    0x0910: {"group": 5},
    0x0911: {"group": 5},
    0x0920: {"group": 6},
    0x0921: {"group": 6},
    0x0924: {"group": 6},
    0x0925: {"group": 6},
    0x0928: {"group": 6},
    0x094E: {"group": 7},
    0x094F: {"group": 7},
}
last_group = -1

for line in sys.stdin:
    for pattern in subs.keys():
        re_match = re.match(pattern, line)
        if re_match is not None:
            if int(re_match.group(2), 16) not in ports.keys():
                print("\n", end='')
                group = -1
            else:
                group = ports[int(re_match.group(2), 16)]["group"]
                if last_group != group:
                    print("\n", end='')
            print(re.sub(pattern, subs[pattern], line), end='')
            last_group = group
            break
