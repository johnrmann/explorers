#ifndef BITMATRIX_H
#define BITMATRIX_H

#include <stdint.h>

typedef struct {
	uint8_t *data;
	int width;
	int height;
} bitmatrix;

/**
 * Allocates memory for a bitmatrix of the given width and height.
 */
bitmatrix* make_bitmatrix(int w, int h);

/**
 * Frees the memory allocated for a bitmatrix.
 */
void free_bitmatrix(bitmatrix *bm);

/**
 * Returns the number of bytes needed to store a bitmatrix of the given width
 * and height.
 */
int bitmatrix_size(int w, int h);

/**
 * Sets the value of the bit at the given row and column.
 */
void bitmatrix_set_bit_at(bitmatrix *bm, int r, int c, char value);

/**
 * Returns the value of the bit at the given row and column.
 */
char bitmatrix_get_bit_at(bitmatrix *bm, int r, int c);

/**
 * Resets all bits in a bitmatrix to zero.
 */
void bitmatrix_clear(bitmatrix *bm);

#endif