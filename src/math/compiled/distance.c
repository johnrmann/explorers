#include <stdlib.h>
#include <time.h>
#include <math.h>

#include "distance.h"
#include "vector2.h"

double distance2(Vector2 *p, Vector2 *q) {
	int dy = p->y - q->y;
	int dx = p->x - q->x;
	return pow(dx, 2) + pow(dy, 2);
}

double x_looped_distance2(Vector2 *p, Vector2 *q, int w, int h) {
	int temp_x = p->x;
	double normal = distance2(p, q);
	p->x = temp_x + w;
	double beyond = distance2(p, q);
	p->x = temp_x - w;
	double behind = distance2(p, q);
	p->x = temp_x;
	if (normal < beyond && normal < behind) {
		return normal;
	} else if (beyond < normal && beyond < behind) {
		return beyond;
	} else {
		return behind;
	}
}
