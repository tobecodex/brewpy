#include <string.h>
#include <stdlib.h>

#include "gpio.h"

#include "dht11.h"
#include <stdio.h>
#include <stdbool.h>

int main(int argc, char **argv)
{
  gpio_init();
  int celsius, rh;

  bool done = false;
  while (!done) {  
    if (readDHT11(4, &celsius, &rh)) {
      printf("T:%d RH:%d\n", celsius, rh);
      done = true;
    } else {
      sleep(2);
    }
  }
  return 0;
}

bool readDHT11(int pin, int *celsius, int *rh) {

  const int MAX_WAITS = 1000;

  gpio_setup(pin, GPIO_OUT);
  gpio_write(pin, GPIO_HI);
  usleep(500000);
  gpio_write(pin, GPIO_LO);
  usleep(20000);
 
  gpio_setup(pin, GPIO_INP);
  if (!gpio_expect(pin, GPIO_LO, MAX_WAITS) || 
      !gpio_expect(pin, GPIO_HI, MAX_WAITS) || 
      !gpio_expect(pin, GPIO_LO, MAX_WAITS)) {
    return false;
  } 

  int waits;
  int bits[40];
  int sum_waits = 0;
  for (int i = 0; i < 40; i++) {
    if (!gpio_expect(pin, GPIO_HI, MAX_WAITS))
      return false;
    if (!(bits[i] = gpio_expect(pin, GPIO_LO, MAX_WAITS)))
      return false;
    sum_waits += bits[i];
  }

  char bytes[5];
  memset(bytes, 0, sizeof(bytes));
  const int avg_waits = sum_waits / 40;

  for (int i = 0; i < 40; i++) {
    bytes[i / 8] |= ((bits[i] > avg_waits ? 1 : 0) << (7 - (i % 8)));
  }

  char check = 0;
  for (int i = 0; i < 4; i++) {
    check += bytes[i];
  }
  
  if ((check & 0xFF) == bytes[4]) {
    *celsius = bytes[2]; *rh = bytes[0];
    return true;
  }

  return false;
}
