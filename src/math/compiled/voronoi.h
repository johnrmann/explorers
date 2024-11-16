#ifndef VORONOI_H
#define VORONOI_H

/**
 * Create a voronoi matrix with dimensions (w * h) and a total of (w * h) /
 * density points.
 */
int **make_voronoi(int w, int h, int density);

/**
 * Free the matrix.
 */
void free_voronoi(int **matrix, int h);

#endif
