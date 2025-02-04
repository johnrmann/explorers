#include <stdlib.h>

#include "matrix.h"

IntMatrix* make_int_matrix(int w, int h) {
	IntMatrix *m = (IntMatrix *)malloc(sizeof(IntMatrix));
	m->data = (int *)malloc(w * h * sizeof(int));
	m->width = w;
	m->height = h;
	return m;
}

void free_int_matrix(IntMatrix *m) {
	free(m->data);
	free(m);
}

IntMatrix *int_matrix_add(IntMatrix *m1, IntMatrix *m2) {
	int width = m1->width;
	int height = m1->height;
	IntMatrix *result = make_int_matrix(width, height);
	for (int r = 0; r < height; r++) {
		for (int c = 0; c < width; c++) {
			int v1 = int_matrix_get_at(m1, r, c);
			int v2 = int_matrix_get_at(m2, r, c);
			int_matrix_set_at(result, r, c, v1 + v2);
		}
	}
	return result;
}

int int_matrix_idx(IntMatrix *m, int r, int c) {
	return r * m->width + c;
}

int int_matrix_get_at(IntMatrix *m, int r, int c) {
	int idx = int_matrix_idx(m, r, c);
	return m->data[idx];
}

void int_matrix_set_at(IntMatrix *m, int r, int c, int value) {
	int idx = int_matrix_idx(m, r, c);
	m->data[idx] = value;
}

void int_matrix_delta_at(IntMatrix *m, int r, int c, int delta) {
	int idx = int_matrix_idx(m, r, c);
	m->data[idx] += delta;
}

int **int_matrix_values(IntMatrix *m) {
	int **values = (int **)malloc(m->height * sizeof(int *));
	for (int i = 0; i < m->height; i++) {
		values[i] = (int *)malloc(m->width * sizeof(int));
		for (int j = 0; j < m->width; j++) {
			values[i][j] = int_matrix_get_at(m, i, j);
		}
	}
	return values;
}
