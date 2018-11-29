#ifndef HELPERS_H
#define HELPERS_H

#include <kipr/botball.h>
#include <stdio.h>

namespace ths_helpers {
    /**
     * The Arduino map function.
     */
    long map(long x, long in_min, long in_max, long out_min, long out_max);
}

#endif