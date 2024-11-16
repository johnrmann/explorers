#ifdef RUN_VORONOI

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#include "voronoi.h"

int main(int argc, char *argv[]) {
	if (argc != 4) {
		fprintf(stderr, "Usage: %s <width> <height> <density>\n", argv[0]);
		return 1;
	}

	int width = atoi(argv[1]);
	int height = atoi(argv[2]);
	int density = atoi(argv[3]);

	int **voronoi_matrix = make_voronoi(width, height, density);

	for (int y = 0; y < height; y++) {
		for (int x = 0; x < width; x++) {
			printf("%d ", voronoi_matrix[y][x]);
		}
		printf("\n");
	}

	free_voronoi(voronoi_matrix, height);
	return 0;
}

#endif
