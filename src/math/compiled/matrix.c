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
