#include <stdlib.h>
#include <time.h>
#include <math.h>

#include "vector2.h"

void generate_random_points(Vector2 *points, int num_points, int w, int h) {
	for (int i = 0; i < num_points; i++) {
		points[i].x = rand() % w;
		points[i].y = rand() % h;
	}
}
