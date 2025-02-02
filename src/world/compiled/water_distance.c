#include <stdlib.h>
#include <stdbool.h>

#include "../../math/compiled/matrix.h"

#include "water_distance.h"

#define min(a, b) ((a) < (b) ? (a) : (b))

WaterDistance *make_water_distance(int xy, int z) {
	WaterDistance *water_distance = malloc(sizeof(WaterDistance));
	water_distance->xy = xy;
	water_distance->z = z;
	return water_distance;
}

void copy_water_distance(WaterDistance *src, WaterDistance *dest) {
	dest->xy = src->xy;
	dest->z = src->z;
}

void free_water_distance(WaterDistance *water_distance) {
	free(water_distance);
}

int water_distance_magnitude(WaterDistance *water_distance) {
	return water_distance->xy + water_distance->z;
}

void water_distance_copymin(
	WaterDistance *src1,
	WaterDistance *src2,
	WaterDistance *dest
) {
	int mag1 = water_distance_magnitude(src1);
	int mag2 = water_distance_magnitude(src2);
	if (mag1 < mag2) {
		copy_water_distance(src1, dest);
	} else {
		copy_water_distance(src2, dest);
	}
}

WaterDistanceMtx *make_water_distance_matrix(int width, int height) {
	WaterDistanceMtx *matrix = malloc(sizeof(WaterDistanceMtx));
	matrix->width = width;
	matrix->height = height;
	matrix->matrix = malloc(sizeof(WaterDistance *) * height);
	for (int i = 0; i < width; i++) {
		matrix->matrix[i] = malloc(sizeof(WaterDistance) * width);
	}
	return matrix;
}

WaterDistance *water_distance_matrix_get_at(
	WaterDistanceMtx *wdm,
	int x,
	int y
) {
	WaterDistance *row = wdm->matrix[y];
	return &row[x];
}

WaterDistanceMtx *water_distance_matrix_minfold(WaterDistanceMtx *matrix) {
	int width = matrix->width / 2;
	int height = matrix->height;
	WaterDistanceMtx *new_mat = make_water_distance_matrix(width, height);
	for (int y = 0; y < height; y++) {
		for (int x = 0; x < width; x++) {
			int x2 = x + width;
			WaterDistance *src1 = water_distance_matrix_get_at(matrix, x, y);
			WaterDistance *src2 = water_distance_matrix_get_at(matrix, x2, y);
			WaterDistance *dest = water_distance_matrix_get_at(new_mat, x, y);
			water_distance_copymin(src1, src2, dest);
		}
	}
	return new_mat;
}

void free_water_distance_matrix(WaterDistanceMtx *matrix) {
	for (int i = 0; i < matrix->height; i++) {
		free(matrix->matrix[i]);
	}
	free(matrix->matrix);
	free(matrix);
}

void water_distance_matrix_set_at(
	WaterDistanceMtx *matrix,
	int x,
	int y,
	int wd_xy,
	int wd_z
) {
	WaterDistance *wd = water_distance_matrix_get_at(matrix, x, y);
	wd->xy = wd_xy;
	wd->z = wd_z;
}

WaterDistanceMtx *calculate_water_distance_matrix(
	IntMatrix *land_heights,
	IntMatrix *water_heights
) {
	int wd_infinity = land_heights->width + land_heights->height + 1;

	IntMatrix *total_heights = int_matrix_add(land_heights, water_heights);

	WaterDistanceMtx *wd_matrix = make_water_distance_matrix(
		land_heights->width,
		land_heights->height
	);

	for (int y = 0; y < land_heights->height; y++) {
		for (int x = 0; x < land_heights->width; x++) {
			int water_height = int_matrix_get_at(water_heights, y, x);
			if (water_height > 0) {
				water_distance_matrix_set_at(wd_matrix, x, y, 0, 0);
			} else {
				water_distance_matrix_set_at(
					wd_matrix, x, y, wd_infinity, wd_infinity
				);
			}
		}
	}

	struct WaterDistance my_wd;
	for (int y = 0; y < land_heights->height; y++) {
		for (int x = 0; x < land_heights->width; x++) {
			copy_water_distance(
				water_distance_matrix_get_at(wd_matrix, x, y),
				&my_wd
			);

			int land_height = int_matrix_get_at(land_heights, y, x);
			int water_height = int_matrix_get_at(water_heights, y, x);
			int total_height = land_height + water_height;

			int look_north_xy = wd_infinity;
			int look_north_z = wd_infinity;

			if (y > 0) {
				look_north_xy = water_distance_matrix_get_at(
					wd_matrix, x, y - 1
				)->xy;
				int north_height = int_matrix_get_at(total_heights, y - 1, x);
				int dz = abs(total_height - north_height);
				look_north_z = water_distance_matrix_get_at(
					wd_matrix, x, y - 1
				)->z + dz;
			}

			int look_west_xy = wd_infinity;
			int look_west_z = wd_infinity;

			if (x > 0) {
				look_west_xy = water_distance_matrix_get_at(
					wd_matrix, x - 1, y
				)->xy;
				int west_height = int_matrix_get_at(total_heights, y, x - 1);
				int dz = abs(total_height - west_height);
				look_west_z = water_distance_matrix_get_at(
					wd_matrix, x - 1, y
				)->z + dz;
			}

			int xy = min(look_north_xy, look_west_xy);
			xy = min(xy, my_wd.xy);

			int z = min(look_north_z, look_west_z);
			z = min(z, my_wd.z);

			water_distance_matrix_set_at(wd_matrix, x, y, xy, z);
		}
	}

	for (int y = land_heights->height - 1; y >= 0; y--) {
		for (int x = land_heights->width - 1; x >= 0; x--) {
			copy_water_distance(
				water_distance_matrix_get_at(wd_matrix, x, y),
				&my_wd
			);

			int land_height = int_matrix_get_at(land_heights, y, x);
			int water_height = int_matrix_get_at(water_heights, y, x);
			int total_height = land_height + water_height;

			int look_south_xy = wd_infinity;
			int look_south_z = wd_infinity;

			if (y < land_heights->height - 1) {
				look_south_xy = water_distance_matrix_get_at(
					wd_matrix, x, y + 1
				)->xy;
				int south_height = int_matrix_get_at(total_heights, y + 1, x);
				int dz = abs(total_height - south_height);
				look_south_z = water_distance_matrix_get_at(
					wd_matrix, x, y + 1
				)->z + dz;
			}

			int look_east_xy = wd_infinity;
			int look_east_z = wd_infinity;

			if (x < land_heights->width - 1) {
				look_east_xy = water_distance_matrix_get_at(
					wd_matrix, x + 1, y
				)->xy;
				int east_height = int_matrix_get_at(total_heights, y, x + 1);
				int dz = abs(total_height - east_height);
				look_east_z = water_distance_matrix_get_at(
					wd_matrix, x + 1, y
				)->z + dz;
			}

			int xy = min(look_south_xy, look_east_xy);
			xy = min(xy, my_wd.xy);

			int z = min(look_south_z, look_east_z);
			z = min(z, my_wd.z);

			water_distance_matrix_set_at(wd_matrix, x, y, xy, z);
		}
	}

	free_int_matrix(total_heights);

	return wd_matrix;
}
