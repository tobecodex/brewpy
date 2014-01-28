#include "gpio.h"

#include <time.h>
#include <stdio.h>
#include <unistd.h>

double readAnalog(int pin);

int main(int argc, char **argv)
{
  gpio_init();

  bool done = false;
  while (!done) {
    printf("%d\n", (int)readAnalog(23));
    sleep(2);
  }
  return 0;
}

double readAnalog(int pin) {

  gpio_setup(pin, GPIO_OUT);
  gpio_write(pin, GPIO_LO);
  sleep(1);

  struct timespec begin, end;

  // Measure time to charge 
  clock_gettime(CLOCK_REALTIME, &begin);
  gpio_setup(pin, GPIO_INP);
  gpio_expect(pin, GPIO_HI, 0); 
  clock_gettime(CLOCK_REALTIME, &end);

  // t in seconds
  double t = ((end.tv_sec * 1e9) + end.tv_nsec) - 
    ((begin.tv_sec * 1e9) + (begin.tv_nsec));
  t = t / 1e9;

  // C in Farads
  double C = 0.000001;
  
  // t = RC/2 (1.3v threshold, 3.3v limit, 40% = RC/2)
  double R = (2 * t) / C;

  return R;
}
