#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

#include "water_distance.h"
#include "biome.h"

#define HOT_MINIMUM 80.0
#define TEMPERATE_MINIMUM 50.0

BiomeMatrix *make_biome_matrix(int width, int height) {
	BiomeMatrix *matrix = malloc(sizeof(BiomeMatrix));
	matrix->width = width;
	matrix->height = height;
	matrix->matrix = malloc(sizeof(Biome *) * height);
	// Initialize all biomes to barren.
	for (int i = 0; i < width; i++) {
		matrix->matrix[i] = malloc(sizeof(Biome) * width);
	}
	return matrix;
}

void free_biome_matrix(BiomeMatrix *matrix) {
	free(matrix->matrix);
	free(matrix);
}

BiomeTemperature get_biome_temperature(float tpr_deg_f) {
	if (tpr_deg_f < 0) {
		return BIOME_TPR__BARREN;
	} else if (tpr_deg_f <= 45) {
		return BIOME_TPR__COLD;
	} else if (tpr_deg_f <= 75) {
		return BIOME_TPR__TEMPERATE;
	} else if (tpr_deg_f <= 110) {
		return BIOME_TPR__HOT;
	} else {
		return BIOME_TPR__BARREN;
	}
}

BiomeWetness get_biome_wetness(WaterDistance *water_distance, int wet_cutoff) {
	int mag = water_distance_magnitude(water_distance);
	if (mag < wet_cutoff) {
		return BIOME_WET__WET;
	} else {
		return BIOME_WET__DRY;
	}
}

#define MAX_BEACH_Z_DISTANCE 3
#define MAX_BEACH_DISTANCE 6

bool get_is_beach(WaterDistance *water_distance) {
	int mag = water_distance_magnitude(water_distance);
	bool z_in_range = water_distance->z <= MAX_BEACH_Z_DISTANCE;
	return z_in_range && mag <= MAX_BEACH_DISTANCE;
}

Biome get_biome(
	float tpr_deg_f,
	WaterDistance *water_distance,
	int wet_cutoff
) {
	BiomeTemperature tpr = get_biome_temperature(tpr_deg_f);
	BiomeWetness wet = get_biome_wetness(water_distance, wet_cutoff);
	
	if (get_is_beach(water_distance)) {
		return BIOME__BEACH;
	}
	
	return tpr | wet;
}

BiomeMatrix *calculate_biomes(
	WaterDistanceMtx *water_distances,
	float *tpr_deg_fs,
	int wet_cutoff
) {
	int width = water_distances->width;
	int height = water_distances->height;
	BiomeMatrix *biomes = make_biome_matrix(width, height);

	for (int y = 0; y < height; y++) {
		float tpr_deg_f = tpr_deg_fs[y];
		for (int x = 0; x < width; x++) {
			WaterDistance *water_distance = water_distance_matrix_get_at(
				water_distances, x, y
			);
			Biome biome = get_biome(tpr_deg_f, water_distance, wet_cutoff);
			biome_matrix_set_at(biomes, x, y, biome);
		}
	}

	return biomes;
}

void biome_matrix_set_at(BiomeMatrix *matrix, int x, int y, Biome biome) {
	Biome *row = matrix->matrix[y];
	row[x] = biome;
}
