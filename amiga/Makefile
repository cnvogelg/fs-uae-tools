CC=vc
CFLAGS=-c99 -g -sc -O2

all: hdr uaetool

clean:
	@rm -f uaetool
	@$(MAKE) -C uae_lib clean

hdr:
	@$(MAKE) -C uae_lib

uaetool: uaetool.c
	$(CC) $(CFLAGS) -Iuae_lib/include -o $@ $< -lamiga
