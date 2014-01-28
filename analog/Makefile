CC = gcc
CFLAGS = -O3 -std=gnu99 -I. -I../bcm2835/src -lbcm2835 -lrt
DEPS = 
OBJ = analog.o gpio.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

analog: $(OBJ)
	gcc -o $@ $^ $(CFLAGS)
