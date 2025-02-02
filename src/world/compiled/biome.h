#ifndef BIOME_H
#define BIOME_H

#include "water_distance.h"

typedef enum BiomeTemperature {
	BIOME_TPR__BARREN = 0x00,

	BIOME_TPR__HOT = 0x01,
	BIOME_TPR__TEMPERATE = 0x02,
	BIOME_TPR__COLD = 0x03
} BiomeTemperature;

typedef enum BiomeWetness {
	BIOME_WET__BARREN = 0x00,

	BIOME_WET__WET = 0x10,
	BIOME_WET__DRY = 0x20
} BiomeWetness;

typedef enum Biome {
	BIOME__BARREN = BIOME_TPR__BARREN | BIOME_WET__BARREN,
	BIOME__OUTBACK = 0x200,
	BIOME__BEACH = 0x300,

	// Hot temperature.
	BIOME__TROPICAL = BIOME_TPR__HOT | BIOME_WET__WET,
	BIOME__DESERT = BIOME_TPR__HOT | BIOME_WET__DRY,

	// Temperate temperature.
	BIOME__LUSH = BIOME_TPR__TEMPERATE | BIOME_WET__WET,
	BIOME__SAVANNAH = BIOME_TPR__TEMPERATE | BIOME_WET__DRY,

	// Cold temperature.
	BIOME__SNOW = BIOME_TPR__COLD | BIOME_WET__WET,
	BIOME__TUNDRA = BIOME_TPR__COLD | BIOME_WET__DRY
} Biome;

typedef struct BiomeMatrix {
	Biome **matrix;
	int width;
	int height;
} BiomeMatrix;

/**
 * Get the temperature of the given temperature in degrees Fahrenheit.
 */
BiomeTemperature get_biome_temperature(float tpr_deg_f);

/**
 * Get the wetness of the given water distance.
 */
BiomeWetness get_biome_wetness(WaterDistance *water_distance, int wet_cutoff);

/**
 * Check if the given water distance is a beach.
 */
bool get_is_beach(WaterDistance *water_distance);

/**
 * Get the biome for the given temperature and water distance.
 */
Biome get_biome(float tpr_deg_f, WaterDistance *water_distance, int wet_cutoff);

/**
 * Create a malloc'd BiomeMatrix struct.
 */
BiomeMatrix *make_biome_matrix(int width, int height);

/**
 * Free a malloc'd BiomeMatrix struct.
 */
void free_biome_matrix(BiomeMatrix *matrix);

/**
 * Calculate the biomes for the given water distances and temperatures.
 */
BiomeMatrix *calculate_biomes(
	WaterDistanceMtx *water_distances,
	float *tpr_deg_fs,
	int wet_cutoff
);

/**
 * Get the biome at the given x, y coordinates.
 */
void biome_matrix_set_at(BiomeMatrix *matrix, int x, int y, Biome biome);

#endif
