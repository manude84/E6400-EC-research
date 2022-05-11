#!/bin/python
"""
    Takes in a parsed dump of LPC cycles and groups them according
    to hard coded patterns found through observation
"""
import sys
import re
from enum import Enum


class State(Enum):
    NA = 0
    RW = 1
    READ = 2
    WRITE = 3
    WAIT = 4


line_buffer = list()
data = list()
state = State.NA
last_index = 256

WRITE_INDEX = r"^.*Write 0x([0-9A-F]{2}) port 0x0910"
READ_DATA = r"^.*Read 0x([0-9A-F]{2}) port 0x0911"
WRITE_DATA = r"^.*Write 0x([0-9A-F]{2}) port 0x0911"


def print_section(state):
    global line_buffer, data, last_index
    start = last_index - len(data) + 1
    end = last_index
    data_string = "".join([c if c.isprintable() and c.isascii() else "."
                           for c in [chr(int(n, 16)) for n in data]])
    if state == State.READ:
        if len(data) == 1:
            print(f"\n# Read EC index 0x{start:02X}: 0x{data[0]}")
        else:
            print(f"\n# Read EC index 0x{start:02X}-0x{end:02X}: ", end='')
            print(" ".join(data) + "  " + data_string)
    elif state == State.WRITE:
        if len(data) == 1:
            print(f"\n# Write EC index 0x{start:02X}: 0x{data[0]}")
        else:
            print(f"\n# Write EC index 0x{start:02X}-0x{end:02X}: ", end='')
            print(" ".join(data) + "  " + data_string)
    elif state == State.WAIT:
        print("\n# Wait EC")

    print("".join(line_buffer))
    line_buffer = list()
    data = list()
    last_index = 256


for line in sys.stdin:
    if line.isspace():
        print(line, end='')
        continue

    if state == State.NA:
        match = re.match(WRITE_INDEX, line)
        if match is not None:
            line_buffer.append(line)
            last_index = int(match.group(1), 16)
            state = State.RW
            continue
        else:
            print(line, end='')
            continue

    if state == State.RW:
        # match = re.match(r"^.*?Write (0x[0-9A-F]{2}) port 0x0911", line)
        match = re.match(WRITE_DATA, line)
        if match is not None:
            line_buffer.append(line)
            data.append(match.group(1))
            state = State.WRITE
            continue
        # match = re.match(r"^.*?Read (0x[0-9A-F]{2}) port 0x0911", line)
        match = re.match(READ_DATA, line)
        if match is not None:
            if last_index == 0:
                state = State.WAIT
            else:
                state = State.READ
                data.append(match.group(1))
            line_buffer.append(line)
            continue

    if state == State.WRITE:
        # match = re.match(r"^.*?Write (0x[0-9A-F]{2}) port 0x0910", line)
        match = re.match(WRITE_INDEX, line)
        if match is not None:
            if int(match.group(1), 16) == last_index + 1:
                line_buffer.append(line)
                last_index += 1
            else:
                print_section(state)
                line_buffer.append(line)
                last_index = int(match.group(1), 16)
                state = State.RW
            continue
        # match = re.match(r"^.*?Write (0x[0-9A-F]{2}) port 0x0911", line)
        match = re.match(WRITE_DATA, line)
        if match is not None:
            line_buffer.append(line)
            data.append(match.group(1))
            continue
        # match = re.match(r"^.*?Read (0x[0-9A-F]{2}) port 0x0911", line)
        match = re.match(READ_DATA, line)
        if match is not None:
            print_section(state)
            line_buffer.append(line)
            state = State.WAIT
            continue
        print_section(state)
        state = State.NA
        print(line, end='')
        continue

    if state == State.READ:
        # match = re.match(r"^.*?Write (0x[0-9A-F]{2}) port 0x0910", line)
        match = re.match(WRITE_INDEX, line)
        if match is not None:
            if int(match.group(1), 16) == last_index + 1:
                last_index += 1
            else:
                print_section(state)
                last_index = int(match.group(1), 16)
                state = State.RW
            line_buffer.append(line)
            continue
        # match = re.match(r"^.*?Read (0x[0-9A-F]{2}) port 0x0911", line)
        match = re.match(READ_DATA, line)
        if match is not None:
            line_buffer.append(line)
            data.append(match.group(1))
            continue
        match = re.match(WRITE_DATA, line)
        # Catch a late transition to the WRITE state on index 0. Since a write
        # to index 0 on the command/index port could be either another wait
        # state or the beginning of a new write to index 0, the correct
        # transition is missed until the access to the data port
        if match is not None:
            tmp = line_buffer.pop()
            last_index -= 1
            print_section(state)
            line_buffer.append(tmp)
            last_index = int(re.match(WRITE_INDEX, tmp).group(1), 16)
            data.append(match.group(1))
            line_buffer.append(line)
            state = State.WRITE
        else:
            print_section(state)
            state = State.NA
            print(line, end='')
        continue

    if state == State.WAIT:
        # match = re.match(r"^.*?Read (0x[0-9A-F]{2}) port 0x0911", line)
        match = re.match(READ_DATA, line)
        if match is not None:
            line_buffer.append(line)
            continue
        # match = re.match(r"^.*?Write (0x[0-9A-F]{2}) port 0x0910", line)
        match = re.match(WRITE_INDEX, line)
        if match is not None:
            if match.group(1) == "0x00":
                line_buffer.append(line)
            else:
                print_section(state)
                last_index = int(match.group(1), 16)
                line_buffer.append(line)
                state = State.RW
            continue
        match = re.match(WRITE_DATA, line)
        # Catch a late transition to the WRITE state on index 0. Since a write
        # to index 0 on the command/index port could be either another wait
        # state or the beginning of a new write to index 0, the correct
        # transition is missed until the access to the data port
        if match is not None:
            tmp = line_buffer.pop()
            print_section(state)
            line_buffer.append(tmp)
            last_index = int(re.match(WRITE_INDEX, tmp).group(1), 16)
            data.append(match.group(1))
            line_buffer.append(line)
            state = State.WRITE
        else:
            print_section(state)
            state = State.NA
            print(line, end='')
        continue
