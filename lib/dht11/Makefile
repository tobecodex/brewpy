CC = gcc
CFLAGS = -O3 -std=c99 -I. -I../bcm2835/src -lbcm2835
DEPS = 
OBJ = dht11.o gpio.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

dht-11: $(OBJ)
	gcc -o $@ $^ $(CFLAGS)
