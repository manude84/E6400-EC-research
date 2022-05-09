import sys
import re

# r"(.*?02(.{4})([\dA-F])([\dA-F]).*)": r"\1\tWrite 0x\4\3 port 0x\2",
# r"(.*?00(.{4}).*?0([\dA-F])([\dA-F]).*)": r"\1\tRead 0x\4\3 port 0x\2",
subs = {
    r"^# Wait EC$": r"",
    r"^# Read EC index (0x[\dA-F]{2}):.*$": r"read_ec(\1);",
    r"^# Write EC index (0x[\dA-F]{2}): (0x[\dA-F]{2})$": r"write_ec(\1, \2);",
    r"^# Read EC index (0x[\dA-F]{2})-(0x[\dA-F]{2}):.*$": r"read_ec_regs(\1, \2, buf);",
    r"^# Write EC index 0x[\dA-F]{2}-0x[\dA-F]{2}: .*$": r"",
    r"^Write (0x[\dA-F]{2}) port 0x0{0,3}([\dA-F]*)$": r"outb(\1, 0x\2);",
    r"^Read 0x[\dA-F]{2} port 0x0{0,3}([\dA-F]*)$": r"inb(0x\1);"
}
skip_line = False
for line in sys.stdin:
    if line == ("\n"):
        skip_line = False
    if skip_line:
        continue
    for i, pattern in enumerate(subs.keys()):
        re_match = re.match(pattern, line)
        if re_match is not None:
            print(re.sub(pattern, subs[pattern], line), end="")
            if i < 4:
                skip_line = True
            break
