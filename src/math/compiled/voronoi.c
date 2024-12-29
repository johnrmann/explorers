#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#include "../../o10n/compiled/bitmatrix.h"

#include "distance.h"
#include "vector2.h"
#include "voronoi.h"
#include "matrix.h"

char FANOUT_DIRECTION_SOURCE = 0;
char FANOUT_DIRECTION_NORTH = 1;
char FANOUT_DIRECTION_EAST = 2;
char FANOUT_DIRECTION_SOUTH = 3;
char FANOUT_DIRECTION_WEST = 4;

Vector2 *make_points(int num_points) {
	Vector2 *points = (Vector2 *)malloc(num_points * sizeof(Vector2));
	return points;
}

void voronoi_visit(
	IntMatrix *matrix,
	Vector2 *position,
	Vector2 *voronois,
	int label, bitmatrix *visited,
	char fanout_direction
) {
	int x = position->x;
	int y = position->y;
	int w = matrix->width;
	int h = matrix->height;

	if (bitmatrix_get_bit_at(visited, y, x) == 1) {
		return;
	}
	bitmatrix_set_bit_at(visited, y, x, 1);
	int set_value = x_looped_find_closest(position, voronois, label, w) + 1;
	int_matrix_set_at(matrix, y, x, set_value);
	if (set_value != label) {
		return;
	}

	// Visit north.
	if (fanout_direction != FANOUT_DIRECTION_SOUTH && y > 0) {
		position->y = y - 1;
		voronoi_visit(
			matrix, position, voronois, label, visited, FANOUT_DIRECTION_NORTH
		);
	}

	// Visit south.
	if (fanout_direction != FANOUT_DIRECTION_NORTH && y < h - 1) {
		position->y = y + 1;
		voronoi_visit(
			matrix, position, voronois, label, visited, FANOUT_DIRECTION_NORTH
		);
	}

	// Visit east.
	if (fanout_direction != FANOUT_DIRECTION_WEST) {
		position->x = (x + 1) % w;
		voronoi_visit(
			matrix, position, voronois, label, visited, FANOUT_DIRECTION_EAST
		);
	}

	// Visit west.
	if (fanout_direction != FANOUT_DIRECTION_EAST) {
		position->x = (x - 1 + w) % w;
		voronoi_visit(
			matrix, position, voronois, label, visited, FANOUT_DIRECTION_WEST
		);
	}

	// Reset the point back to original value.
	position->x = x;
	position->y = y;
}

void fill_voronoi(IntMatrix *matrix, int num_points) {
	Vector2 *points = make_points(num_points);
	generate_random_points(points, num_points, matrix->width, matrix->height);

	bitmatrix *visited = make_bitmatrix(matrix->width, matrix->height);

	for (int y = 0; y < matrix->height; y++) {
		for (int x = 0; x < matrix->width; x++) {
			int_matrix_set_at(matrix, y, x, 1);
		}
	}

	Vector2 p;
	for (int i = 1; i < num_points; i++) {
		p = points[i];
		voronoi_visit(
			matrix,
			&p, points,
			i + 1, visited,
			FANOUT_DIRECTION_SOURCE
		);
		bitmatrix_clear(visited);
	}

	free(points);
	free_bitmatrix(visited);
}

void norm_voronoi(IntMatrix *matrix) {
	int w = matrix->width;
	int h = matrix->height;
	for (int y = 0; y < h; y++) {
		for (int x = 0; x < w; x++) {
			int_matrix_delta_at(matrix, y, x, -1);
		}
	}
}

int **make_voronoi(int w, int h, int density) {
	IntMatrix *matrix = make_int_matrix(w, h);

	srand(time(NULL));
	int num_points = (w * h) / density;
	fill_voronoi(matrix, num_points);
	norm_voronoi(matrix);

	int **values = int_matrix_values(matrix);
	free_int_matrix(matrix);
	return values;
}

void free_voronoi(int **matrix, int height) {
	for (int i = 0; i < height; i++) {
		free(matrix[i]);
	}
	free(matrix);
}
