#ifdef TEST_WATER_DISTANCE

#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>

#include "water_distance.h"

int main() {
	printf("Running Water Distance Tests...\n");

	// Test make, set, get water distance matrix
	printf("Testing make, get, and set...\n");
	WaterDistanceMtx *wdm = make_water_distance_matrix(3, 3);
	water_distance_matrix_set_at(wdm, 0, 0, 4, 8);
	water_distance_matrix_set_at(wdm, 1, 1, 15, 16);
	water_distance_matrix_set_at(wdm, 2, 2, 23, 42);
	WaterDistance *wd1 = water_distance_matrix_get_at(wdm, 0, 0);
	assert(wd1->xy == 4);
	assert(wd1->z == 8);
	WaterDistance *wd2 = water_distance_matrix_get_at(wdm, 1, 1);
	assert(wd2->xy == 15);
	assert(wd2->z == 16);
	WaterDistance *wd3 = water_distance_matrix_get_at(wdm, 2, 2);
	assert(wd3->xy == 23);
	assert(wd3->z == 42);
	printf("Passed!\n");

	// Test water distance magnitude
	printf("Testing water distance magnitude...\n");
	assert(water_distance_magnitude(wd1) == 12);
	assert(water_distance_magnitude(wd2) == 31);
	assert(water_distance_magnitude(wd3) == 65);
	printf("Passed!\n");

	// Clean up.
	free_water_distance_matrix(wdm);
}

#endif
