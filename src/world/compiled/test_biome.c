#ifdef TEST_BIOME

#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>

#include "water_distance.h"
#include "biome.h"

int main() {
	printf("Running Biome Tests...\n");

	printf("Testing sizeof Biome...\n");
	assert(sizeof(Biome) == sizeof(int));
	printf("Passed!\n");

	printf("Testing get_biome_temperature...\n");
	assert(get_biome_temperature(-1) == BIOME_TPR__BARREN);
	assert(get_biome_temperature(0) == BIOME_TPR__COLD);
	assert(get_biome_temperature(46) == BIOME_TPR__TEMPERATE);
	assert(get_biome_temperature(75) == BIOME_TPR__TEMPERATE);
	assert(get_biome_temperature(76) == BIOME_TPR__HOT);
	assert(get_biome_temperature(110) == BIOME_TPR__HOT);
	assert(get_biome_temperature(1000) == BIOME_TPR__BARREN);
	printf("Passed!\n");

	printf("Testing get_biome_wetness...\n");
	WaterDistance *wd1 = make_water_distance(0, 0);
	assert(get_biome_wetness(wd1, 64) == BIOME_WET__WET);
	free_water_distance(wd1);
	WaterDistance *wd2 = make_water_distance(30, 30);
	assert(get_biome_wetness(wd2, 64) == BIOME_WET__WET);
	free_water_distance(wd2);
	WaterDistance *wd3 = make_water_distance(33, 33);
	assert(get_biome_wetness(wd3, 64) == BIOME_WET__DRY);
	free_water_distance(wd3);
	printf("Passed!\n");

	printf("Testing get_is_beach...\n");
	WaterDistance *wd4 = make_water_distance(0, 0);
	assert(get_is_beach(wd4) == true);
	free_water_distance(wd4);
	WaterDistance *wd5 = make_water_distance(3, 3);
	assert(get_is_beach(wd5) == true);
	free_water_distance(wd5);
	WaterDistance *wd6 = make_water_distance(4, 4);
	assert(get_is_beach(wd6) == false);
	free_water_distance(wd6);
	printf("Passed!\n");
}

#endif
