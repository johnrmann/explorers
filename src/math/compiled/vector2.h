#ifndef VECTOR2_H
#define VECTOR2_H

typedef struct {
	int x;
	int y;
} Vector2;

/**
 * Given an array of points (*points) with length num_points, generate random
 * positions in the dimensions (w, h).
 */
void generate_random_points(Vector2 *points, int num_points, int w, int h);

#endif
