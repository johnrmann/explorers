#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#include "distance.h"
#include "vector2.h"
#include "voronoi.h"

int find_closest_point(Vector2 *qs, int num_points, Vector2 *p, int w, int h) {
	int closest_index = 0;
	double closest_distance = x_looped_distance2(&qs[0], p, w, h);
	
	for (int i = 1; i < num_points; i++) {
		double distance = x_looped_distance2(&qs[i], p, w, h);
		if (distance < closest_distance) {
			closest_distance = distance;
			closest_index = i;
		}
	}
	
	return closest_index;
}

Vector2 *make_points(int num_points) {
	Vector2 *points = (Vector2 *)malloc(num_points * sizeof(Vector2));
	return points;
}

void fill_voronoi(int **matrix, int w, int h, Vector2 *points, int num_points) {
	generate_random_points(points, num_points, w, h);

	Vector2 p;
	for (int y = 0; y < h; y++) {
		for (int x = 0; x < w; x++) {
			p.x = x;
			p.y = y;
			matrix[y][x] = find_closest_point(points, num_points, &p, w, h);
		}
	}
}

int **make_voronoi(int w, int h, int density) {
	int **matrix = (int **)malloc(h * sizeof(int *));
	for (int i = 0; i < h; i++) {
		matrix[i] = (int *)malloc(w * sizeof(int));
	}
	srand(time(NULL));
	int num_points = (w * h) / density;
	Vector2 *points = make_points(num_points);
	fill_voronoi(matrix, w, h, points, num_points);
	free(points);
	return matrix;
}

void free_voronoi(int **matrix, int height) {
	for (int i = 0; i < height; i++) {
		free(matrix[i]);
	}
	free(matrix);
}
