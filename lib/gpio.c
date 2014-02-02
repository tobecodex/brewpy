#include "gpio.h"

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/fcntl.h>

volatile unsigned *gpio;

#define BCM2708_PERI_BASE    0x20000000
#define GPIO_BASE            (BCM2708_PERI_BASE + 0x200000) 

#define SET_GPIO_ALT(g,a) *(gpio+(((g)/10))) |= (((a)<=3?(a)+4:(a)==4?3:2)<<(((g)%10)*3))

void gpio_setup(int pin, bool inout)
{
  #define INP_GPIO(g) *(gpio+((g)/10)) &= ~(7<<(((g)%10)*3))
  #define OUT_GPIO(g) *(gpio+((g)/10)) |=  (1<<(((g)%10)*3))

  INP_GPIO(pin);
  if (inout == GPIO_OUT)
    OUT_GPIO(pin);
}

void gpio_write(int pin, bool hilo)
{
  #define GPIO_SET *(gpio + 7)
  #define GPIO_CLR *(gpio + 10)

  hilo ? (GPIO_SET = (1 << pin)) : (GPIO_CLR = (1 << pin));
}

bool gpio_read(int pin)
{
  #define GPIO_READ(g)  *(gpio + 13) &= (1 << (g))
  return GPIO_READ(pin);
}

int gpio_expect(int pin, bool hilo, int max_waits)
{
  int waits = 0;
  while (gpio_read(pin) != hilo) {
    if (++waits > max_waits && max_waits != 0)
      return 0;
  }
  return waits;
}

//

void gpio_init()
{
  int mem_fd;
  const int BLOCK_SIZE = 1024;

  /* open /dev/mem */
  if ((mem_fd = open("/dev/mem", O_RDWR | O_SYNC) ) < 0) {
    printf("can't open /dev/mem \n");
    exit(-1);
  } 

  /* mmap GPIO */
  void *gpio_map = mmap(
    NULL,             // Any adddress in our space will do
    BLOCK_SIZE,       // Map length
    PROT_READ | PROT_WRITE, // Enable reading & writting to mapped memory
    MAP_SHARED,       // Shared with other processes
    mem_fd,           // File to map
    GPIO_BASE         // Offset to GPIO peripheral
  );

  close(mem_fd); // No need to keep mem_fd open after mmap

  if (gpio_map == MAP_FAILED) {
    printf("mmap error %d\n", (int)gpio_map); // errno also set!
    exit(-1);
  }

  // Always use volatile pointer!
  gpio = (volatile unsigned *)gpio_map;
}
