CC = gcc
CFLAGS = -O3 -std=gnu99 -I. -I../lib -I../bcm2835/src -lbcm2835 -lrt
DEPS = 
OBJ = analog.o ../lib/gpio.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

analog: $(OBJ)
	gcc -o $@ $^ $(CFLAGS)

clean:
	@rm *.o
