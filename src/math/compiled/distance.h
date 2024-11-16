#ifndef DISTANCE_H
#define DISTANCE_H

#include "vector2.h"

/**
 * The square of the distance is faster for many operations than just the
 * distance.
 */
double distance2(Vector2 *p, Vector2 *q);

/**
 * Planets are looped on the x-axis. The shortest line can be over the
 * international dateline.
 */
double x_looped_distance2(Vector2 *p, Vector2 *q, int w, int h);

#endif
