#ifndef HELPERS_H
#define HELPERS_H

#include <kipr/botball.h>
#include <stdio.h>

/**
 * The Arduino map function.
 */
long map(long x, long in_min, long in_max, long out_min, long out_max);

/**
 * The Arduino map function for doubles.
 */
double map(double x, double in_min, double in_max, double out_min, double out_max);

void print_botball_logo();

#endif