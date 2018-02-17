CC=vc
CFLAGS=-c99 -g -sc -O2

all: hdr uaetool

hdr:
	$(MAKE) -C uae_lib

uaetool: uaetool.c
	$(CC) $(CFLAGS) -Iuae_lib/include -o $@ $< -lamiga
