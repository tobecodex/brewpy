#include "gpio.h"

#include <time.h>
#include <stdio.h>
#include <unistd.h>

/*
  Measure analog Ω, C or V on a single digital pin by charging an RC
  network. Pin goes high at 1.3v.
*/

static int PIN = 23;
static double CAP_VALUE = 1e-6;

double readAnalog(int pin);

int main(int argc, char **argv)
{
  gpio_init();
  printf("%d\n", (int)readAnalog(PIN));
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

  // t = RC/2 (since V is 3.3v, 40% = RC/2)
  double R = (2 * t) / CAP_VALUE;

  return R;
}
