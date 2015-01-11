#include "gpio.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>

#define PIN 5

bool init(int pin)
{
  gpio_setup(pin, GPIO_OUT);
  gpio_write(pin, GPIO_LO);
  usleep(480);
  gpio_setup(pin, GPIO_INP);
  return gpio_expect(pin, GPIO_LO, 1000);
}

void write_1(int pin)
{
  printf("Write 1\n");
  gpio_write(pin, GPIO_LO);
  usleep(1);
  gpio_write(pin, GPIO_HI);
  usleep(60);
}

void write_0(int pin)
{
  printf("Write 0\n");
  gpio_write(pin, GPIO_LO);
  usleep(60);
}

void write_byte(int pin, unsigned char byte)
{
  gpio_setup(pin, GPIO_OUT);

  int bit = 0x1;
  for (int i = 0; i < 8; i++)
  {
    if ((byte & (bit << i)) == (bit << i))
      write_1(pin);
    else
      write_0(pin);
    usleep(1);
  }
}

bool read_bit(int pin)
{
  gpio_setup(pin, GPIO_OUT);
  gpio_write(pin, GPIO_LO);
  usleep(1);
  gpio_setup(pin, GPIO_INP);
  usleep(1);
  return gpio_read(pin);
}

unsigned char read_byte(int pin)
{
  unsigned char byte = 0;
  for (int i = 0; i < 8; i++)
  {
    byte |= read_bit(pin) ? 0x1 << i : 0;
  }
  return byte;
}
 
int main(int argc, char *argv[])
{
  bool didInit;

  init(PIN);
  write_byte(PIN, 0x33);

  for (int i = 0; i < 8; i++)
  {
    printf("%X ", read_byte(PIN));
  }

  printf("\nDone");
  return 0;
}
