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

double x_looped_distance2(Vector2 *p, Vector2 *q, int w) {
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

int find_closest(Vector2 *p, Vector2 *qs, int num_points) {
	int closest_index = 0;
	double closest_distance = distance2(&qs[0], p);
	
	for (int i = 1; i < num_points; i++) {
		double distance = distance2(&qs[i], p);
		if (distance < closest_distance) {
			closest_distance = distance;
			closest_index = i;
		}
	}
	
	return closest_index;
}

int x_looped_find_closest(Vector2 *p, Vector2 *qs, int num_points, int w) {
	int closest_index = 0;
	double closest_distance = x_looped_distance2(&qs[0], p, w);
	
	for (int i = 1; i < num_points; i++) {
		double distance = x_looped_distance2(&qs[i], p, w);
		if (distance < closest_distance) {
			closest_distance = distance;
			closest_index = i;
		}
	}
	
	return closest_index;
}
