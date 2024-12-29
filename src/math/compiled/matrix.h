#ifndef MATRIX_H
#define MATRIX_H

typedef struct {
	int *data;
	int width;
	int height;
} IntMatrix;

/**
 * Allocates memory for an integer matrix of the given width and height.
 */
IntMatrix* make_int_matrix(int w, int h);

/**
 * Frees the memory allocated for an integer matrix.
 */
void free_int_matrix(IntMatrix *m);

/**
 * Returns the index of the element at the given row and column.
 */
int int_matrix_get_at(IntMatrix *m, int r, int c);

/**
 * Sets the value of the element at the given row and column.
 */
void int_matrix_set_at(IntMatrix *m, int r, int c, int value);

/**
 * Increments the value of the element at the given row and column by the given
 * delta.
 */
void int_matrix_delta_at(IntMatrix *m, int r, int c, int delta);

/**
 * Returns a 2D array of the values in the matrix. Note that responsibility
 * for freeing this 2D array is the caller of this function's.
 */
int **int_matrix_values(IntMatrix *m);

#endif