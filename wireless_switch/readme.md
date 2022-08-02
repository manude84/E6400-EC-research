## Files
- **switch_off.txt**: Dumped while switching the wireless switch to the off position
- **switch_on.txt**: Dumped while switching the wireless switch to the on position
- **switch_off_no_wlan.txt**: Same as switch_off.txt, but with an option in the BIOS set so that WLAN is not controlled by the switch. From this the index argument was discovered.

## Results
**Command**: 0x2B

**Arguments**: Sent on indices 0x12 to 0x14
- 0x12: Which device
	- 0x00: WLAN
	- 0x01: WWAN
	- 0x02: Bluetooth
- 0x13: Must be 0x02
- 0x14:
	- 0x01: Enable device
	- 0x00: Disable device
