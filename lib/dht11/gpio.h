#ifndef __GPIO_H
#define __GPIO_H

#include <stdbool.h>

#define GPIO_HI true
#define GPIO_LO false

#define GPIO_INP true
#define GPIO_OUT false

void gpio_init();
void gpio_setup(int pin, bool inout);

bool gpio_read(int pin);
void gpio_write(int pin, bool hilo);

int gpio_expect(int pin, bool hilo, int timeout);

#endif
