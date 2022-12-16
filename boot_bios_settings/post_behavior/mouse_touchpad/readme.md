## Files
- **serial_mouse.txt**
- **ps2_mouse.txt**
- **touchpad_ps2.txt**

All three of these files were dumped during boot after selecting the BIOS setting of the same name.

## Results
**Command**: 0x1A

**Arguments**: Sent on index 0x12
- 0x00: "Serial Mouse" option selected. Disables the internal touchpad and forces use of a serial mouse, according to BIOS help text
- 0x01: "PS/2 Mouse" option selected. Disables touchpad when an external PS/2 mouse is connected, according to BIOS help text
- 0x02: "Touchpad-PS/2" option selected. Leaves touchpad enabled when an external PS/2 mouse is connected, according to BIOS help text

If this command is not sent, the touchpad/trackpoint will not function. Either 0x01 or 0x02 must be used as the argument.

The utility `enable_touchpad` can be used to test these. To compile:
```
gcc -O2 -o enable_touchpad enable_touchpad.c
```
