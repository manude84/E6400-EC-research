## Results
**Command**: 0x19

**Arguments**: Sent on index 0x12
- 0x02: "Fn Key Only" option selected. Embedded num pad functions the same as a normal num-pad only if the Fn key is held. Num lock status behavior is as one would expect.
	+ Fn + Num Lock on: Operates as a numpad with num lock on
	+ Fn + Num Lock off: Operates as a numpad with num lock off
	+ No Fn: Operates on the normal keyboard layer
- 0x03: "By Num Lock" option selected.
	+ Fn + Num Lock on: Operates on the normal keyboard layer
	+ Fn + Num Lock off: Operates as a numpad with num lock off
	+ No Fn + Num Lock on: Operates as a numpad with num lock on
	+ No Fn + Num Lock off: Operates on the normal keyboard layer
