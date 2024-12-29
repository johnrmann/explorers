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
double x_looped_distance2(Vector2 *p, Vector2 *q, int w);

/**
 * Given a point `p` and a list of points `qs` of length `num_points`, find the
 * index of the point in `qs` that is closest to `p` 
 */
int find_closest(Vector2 *p, Vector2 *qs, int num_points);

/**
 * Given a point `p` and a list of points `qs` of length `num_points`, find the
 * index of the point in `qs` that is closest to `p` given a looped x-dimension
 * of width `w`.
 */
int x_looped_find_closest(Vector2 *p, Vector2 *qs, int num_points, int w);

#endif
