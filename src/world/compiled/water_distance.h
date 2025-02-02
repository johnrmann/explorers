#ifndef WATER_DISTANCE_H
#define WATER_DISTANCE_H

#include "../../math/compiled/matrix.h"

typedef struct WaterDistance {
	int xy;
	int z;
} WaterDistance;

typedef struct WaterDistanceMtx {
	WaterDistance **matrix;
	int width;
	int height;
} WaterDistanceMtx;

/**
 * Create a malloc'd WaterDistance struct.
 */
WaterDistance *make_water_distance(int xy, int z);

/**
 * Free a malloc'd WaterDistance struct.
 */
void free_water_distance(WaterDistance *water_distance);

/**
 * Copy the values from src to dest.
 */
void copy_water_distance(WaterDistance *src, WaterDistance *dest);

/**
 * Get the magnitude of the water distance.
 */
int water_distance_magnitude(WaterDistance *water_distance);

/**
 * Make an empty water distance matrix with the given dimensions.
 */
WaterDistanceMtx *make_water_distance_matrix(int width, int height);

/**
 * Fold a water matrix in half, using the minimum of the two values.
 */
WaterDistanceMtx *water_distance_matrix_minfold(WaterDistanceMtx *matrix);

/**
 * Get the WaterDistance at the given x, y coordinates.
 */
WaterDistance *water_distance_matrix_get_at(
	WaterDistanceMtx *matrix,
	int x,
	int y
);

/**
 * Set the WaterDistance at the given x, y coordinates.
 */
void water_distance_matrix_set_at(
	WaterDistanceMtx *matrix,
	int x,
	int y,
	int wd_xy,
	int wd_z
);

/**
 * Free a water distance matrix.
 */
void free_water_distance_matrix(WaterDistanceMtx *matrix);

/**
 * Calculate a water distance matrix from a land and water height map.
 */
WaterDistanceMtx *calculate_water_distance_matrix(
	IntMatrix *land_heights,
	IntMatrix *water_heights
);


#endif
