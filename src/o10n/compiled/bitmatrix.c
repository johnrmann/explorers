#include <stdlib.h>
#include <string.h>

#include "bitmatrix.h"

bitmatrix* make_bitmatrix(int w, int h) {
	bitmatrix *bm = (bitmatrix*)malloc(sizeof(bitmatrix));
	if (!bm) return NULL;
	bm->width = w;
	bm->height = h;
	bm->data = (uint8_t*)calloc(w * h, sizeof(uint8_t));
	if (!bm->data) {
		free(bm);
		return NULL;
	}
	return bm;
}

int bitmatrix_size(int w, int h) {
	return w * h;
}

void bitmatrix_set_bit_at(bitmatrix *bm, int r, int c, char value) {
	if (r >= 0 && r < bm->height && c >= 0 && c < bm->width) {
		if (value)
			bm->data[r * bm->width + c] = 1;
		else
			bm->data[r * bm->width + c] = 0;
	}
}

char bitmatrix_get_bit_at(bitmatrix *bm, int r, int c) {
	if (r >= 0 && r < bm->height && c >= 0 && c < bm->width) {
		return bm->data[r * bm->width + c];
	}
	return 0;
}

void bitmatrix_clear(bitmatrix *bm) {
	if (bm && bm->data) {
		memset(bm->data, 0, bm->width * bm->height);
	}
}

void free_bitmatrix(bitmatrix *bm) {
	if (bm) {
		if (bm->data) {
			free(bm->data);
		}
		free(bm);
	}
}
