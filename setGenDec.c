/* SPDX-License-Identifier: MIT */

#include <sys/io.h>

#include <err.h>
#include <errno.h>
#include <stdio.h>

#define PCI_CFG_ADDR 0xCF8
#define PCI_CFG_DATA 0xCFC

int
main(int argc, char *argv[])
{
	(void)argc;
	(void)argv;

	if (ioperm(PCI_CFG_ADDR, 8, 1) == -1)
		err(errno, "ioperm");

	// LPC Controller 00:1f.0 GEN2_DEC register
	outl(0x80000000 | (0 << 16) | (0x1f << 11) | (0 << 8) | 0x88, PCI_CFG_ADDR);
	// Forward IO ports 0x900 to 0x97f over LPC
	outl(0x007c0901, PCI_CFG_DATA);
	return errno;
}
