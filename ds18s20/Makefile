CC = gcc
CFLAGS = -O3 -std=c99 -I. -I../bcm2835/src -lbcm2835
DEPS = 
OBJ = ds18s20.o gpio.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

ds18s20: $(OBJ)
	gcc -o $@ $^ $(CFLAGS)
