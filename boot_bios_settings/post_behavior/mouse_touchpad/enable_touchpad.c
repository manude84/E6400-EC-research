#include <stdio.h>
#include <stdlib.h>
#include <sys/io.h>

static const unsigned short EC_CTRL = 0x910;
static const unsigned short EC_DATA = 0x911;

static void wait_ec(void)
{
	unsigned char v;
	do {
		outb(0, EC_CTRL);
		v = inb(EC_DATA);
	} while (v != 0);
}

static void send_command(unsigned char cmd) {
	outb(0, EC_CTRL);
	outb(cmd, EC_DATA);
	wait_ec();
}

int main(int argc, char *argv[])
{
	if (ioperm(0x910, 2, 1) < 0) {
		perror("ioperm");
		return -1;
	}
	if (argc < 2) {
		printf("missing argument.\n");
		printf("Usage: enable_touchpad 0|1|2\n");
		printf("0: Disable touchpad, use a serial mouse\n");
		printf("1: Disable touchpad when PS/2 mouse connected\n");
		printf("2: Touchpad always enabled\n");
		return -1;
	}
	int option = strtol(argv[1], NULL, 10);
	if (option < 0 || option > 2) {
		printf("Argument out of range\n");
		return -1;
	}
	outb(0x12, EC_CTRL);
	outb(option, EC_DATA);
	send_command(0x1A);
	return 0;
}
