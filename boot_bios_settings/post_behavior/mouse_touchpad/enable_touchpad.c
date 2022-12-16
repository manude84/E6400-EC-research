#include <stdio.h>
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

int main()
{
	if (ioperm(0x910, 2, 1) < 0) {
		perror("ioperm");
		return -1;
	}
	outb(0x12, EC_CTRL);
	outb(0x02, EC_DATA);
	send_command(0x1A);
	return 0;
}
