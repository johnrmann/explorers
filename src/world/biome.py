"""
This module contains enumerations to define the different types of Biomes in
the game world, as well as calculating the biome type of a given tile.
"""

import math

from enum import Enum

from src.math.matrix import matrix_double_width, matrix_fold_width
from src.utility.temperature import kelvin_to_fahrenheit

# We express distance to the nearest body of water as tuple of two integers.
# The first integer is the xy distance, meaning the number of steps in the
# xy plane to reach the nearest body of water. The second integer is the z
# offset, with units of terrain steps.
#
# Use (-1, -1) to represent no water on the planet or too far away to matter.
WaterDistance = tuple[int, int]



class BiomeTemperature(Enum):
	"""Biomes can be cold, temperate, or hot. We also include a BARREN tpr
	for completely uninhabitable for humans."""

	BARREN = 0

	HOT = 1
	TEMPERATE = 2
	COLD = 3



class BiomeWetness(Enum):
	"""Biomes can be dry, temperate, or wet. We also include a BARREN wetness
	for completely uninhabitable for humans."""

	BARREN = 0

	WET = 1
	DRY = 2



class Biome(Enum):
	"""
	The various biomes we can have.
	"""

	# Completely uninhabitable for humans. Used for pre-terraforming states.
	BARREN = 0

	# For the ocean.
	OCEAN = 1

	# Special biome type for "Tutorial: Walkabout."
	OUTBACK = 2

	# Whenever we're within a certain range of water, we're in a beach biome.
	BEACH = 3

	# Biomes with a hot temperature, from most to least wet.
	TROPICAL = 4
	DESERT = 5

	# Biomes with a temperate temperature, from most to least wet.
	LUSH = 6
	SAVANNAH = 7

	# Biomes with a cold temperature, from most to least wet.
	SNOW = 8
	TUNDRA = 9



def get_biome_temperature(tpr_deg_f: float) -> BiomeTemperature:
	"""
	Maps degrees fahrenheit to a BiomeTemperature enumeration.
	"""
	if tpr_deg_f < 0:
		return BiomeTemperature.BARREN
	elif tpr_deg_f < 45:
		return BiomeTemperature.COLD
	elif tpr_deg_f < 75:
		return BiomeTemperature.TEMPERATE
	elif tpr_deg_f < 110:
		return BiomeTemperature.HOT
	else:
		return BiomeTemperature.BARREN


def get_biome_wetness(
		water_distance: WaterDistance,
		wet_cutoff: int = 64
) -> BiomeWetness:
	"""
	Maps the distance to the nearest body of water to a BiomeWetness
	enumeration.
	"""
	wd_xy, wd_z = water_distance
	wd_total = wd_xy + wd_z
	if wd_total < 0:
		return BiomeWetness.BARREN
	elif wd_total < wet_cutoff:
		return BiomeWetness.WET
	else:
		return BiomeWetness.DRY


MAX_BEACH_DISTANCE = 6
MAX_BEACH_Z_DISTANCE = 3

def get_is_beach(water_distance: WaterDistance) -> bool:
	"""
	Returns True if the given tile is a beach biome, False otherwise.
	"""
	wd_xy, wd_z = water_distance
	wd_total = wd_xy + wd_z
	if wd_xy == 0:
		return False
	if wd_total < 0:
		return False
	elif wd_z > MAX_BEACH_Z_DISTANCE:
		return False
	elif wd_total <= MAX_BEACH_DISTANCE:
		return True
	else:
		return False


def get_biome(
		tpr_deg_f: float,
		water_distance: WaterDistance,
		wet_cutoff: int = 64
) -> Biome:
	"""
	Maps a temperature and water distance to a Biome enumeration.
	"""
	tpr = get_biome_temperature(tpr_deg_f)
	wet = get_biome_wetness(water_distance, wet_cutoff=wet_cutoff)

	wd_xy, _ = water_distance
	if wd_xy == 0:
		return Biome.OCEAN

	if tpr == BiomeTemperature.BARREN or wet == BiomeWetness.BARREN:
		return Biome.BARREN

	if get_is_beach(water_distance):
		return Biome.BEACH

	if tpr == BiomeTemperature.HOT:
		if wet == BiomeWetness.WET:
			return Biome.TROPICAL
		else:
			return Biome.DESERT

	elif tpr == BiomeTemperature.TEMPERATE:
		if wet == BiomeWetness.WET:
			return Biome.LUSH
		else:
			return Biome.SAVANNAH

	else:
		# Cold.
		if wet == BiomeWetness.WET:
			return Biome.SNOW
		else:
			return Biome.TUNDRA


def _water_distances(
		land_height: list[list[int]],
		water_level: list[list[int]],
):
	width = len(land_height[0])
	height = len(land_height)

	total_heights = [
		[land_height[y][x] + water_level[y][x] for x in range(width)]
		for y in range(height)
	]

	water_dist_xys = [
		[0 if water_level[y][x] > 0 else math.inf for x in range(width)]
		for y in range(height)
	]

	water_dist_zs = [
		[0 if water_level[y][x] > 0 else math.inf for x in range(width)]
		for y in range(height)
	]

	for y in range(height):
		for x in range(width):
			my_xy = water_dist_xys[y][x]
			my_z = water_dist_zs[y][x]
			my_height = total_heights[y][x]
			look_north_xy = math.inf
			look_north_z = math.inf
			look_west_xy = math.inf
			look_west_z = math.inf
			if y > 0:
				look_north_xy = water_dist_xys[y - 1][x]
				north_height = total_heights[y - 1][x]
				dz = abs(my_height - north_height)
				look_north_z = water_dist_zs[y - 1][x] + dz
			if x > 0:
				look_west_xy = water_dist_xys[y][x - 1]
				west_height = total_heights[y][x - 1]
				dz = abs(my_height - west_height)
				look_west_z = water_dist_zs[y][x - 1] + dz
			water_dist_xys[y][x] = min(
				look_north_xy + 1,
				look_west_xy + 1,
				my_xy
			)
			water_dist_zs[y][x] = min(
				look_north_z,
				look_west_z,
				my_z
			)

	for y in range(height -1, -1, -1):
		for x in range(width - 1, -1, -1):
			my_xy = water_dist_xys[y][x]
			my_z = water_dist_zs[y][x]
			my_height = total_heights[y][x]
			look_south_xy = math.inf
			look_south_z = math.inf
			look_east_xy = math.inf
			look_east_z = math.inf
			if y < height - 1:
				look_south_xy = water_dist_xys[y + 1][x]
				south_height = total_heights[y + 1][x]
				dz = abs(my_height - south_height)
				look_south_z = water_dist_zs[y + 1][x] + dz
			if x < width - 1:
				look_east_xy = water_dist_xys[y][x + 1]
				east_height = total_heights[y][x + 1]
				dz = abs(my_height - east_height)
				look_east_z = water_dist_zs[y][x + 1] + dz
			water_dist_xys[y][x] = min(
				look_south_xy + 1,
				look_east_xy + 1,
				my_xy
			)
			water_dist_zs[y][x] = min(
				look_south_z,
				look_east_z,
				my_z
			)
	
	return [
		[(water_dist_xys[y][x], water_dist_zs[y][x]) for x in range(width)]
		for y in range(height)
	]


def _min_water_dist(pair1, pair2):
	"""
	Given two water distance pairs, returns the one that's smaller.
	"""
	sum1 = sum(pair1)
	sum2 = sum(pair2)
	if sum1 < sum2:
		return pair1
	else:
		return pair2


def calculate_biomes(
		land_height: list[list[int]] = None,
		water_height: list[list[int]] = None,
		tpr_deg_fs: dict[int, float] = None,
		tpr_kelvins: dict[int, float] = None,
		wet_cutoff: int = 64,
		loop_x = True,
):
	"""
	Calculate the biomes for a terrain map given the land heightmap, water
	heightmap, and temperature function (mapping latitude to tpr).

	Optional wetness cutoff to determine where we transition from wet climates
	to dry climates.

	Optional loop_x parameter to determine if the map wraps around like a
	spherical planet.
	"""

	# First, ensure that required params are passed.
	if land_height is None:
		raise ValueError("Land height must be provided.")
	if water_height is None:
		raise ValueError("Water level must be provided.")
	if tpr_deg_fs is None and tpr_kelvins is None:
		raise ValueError("Temperatures must be provided.")

	# Convert tprs to fahrenheit
	if tpr_deg_fs is None:
		if isinstance(tpr_kelvins, dict):
			tpr_deg_fs = {
				idx: kelvin_to_fahrenheit(tpr)
				for idx, tpr in tpr_kelvins.items()
			}
		else:
			tpr_deg_fs = {
				idx: kelvin_to_fahrenheit(tpr)
				for idx, tpr in enumerate(tpr_kelvins)
			}

	width = len(land_height[0])
	height = len(land_height)

	biomes = [
		[Biome.BARREN for _ in range(width)]
		for _ in range(height)
	]

	# Calculate the water distance matrix.
	water_distances = [[]]
	if not loop_x:
		water_distances = _water_distances(
			land_height, water_height
		)
	else:
		doubled_land = matrix_double_width(land_height)
		doubled_water = matrix_double_width(water_height)
		unfolded = _water_distances(doubled_land, doubled_water)
		water_distances = matrix_fold_width(unfolded, _min_water_dist)

	for y in range(height):
		water_dist_row = water_distances[y]
		tpr = tpr_deg_fs[y]
		for x in range(width):
			wd = water_dist_row[x]
			biomes[y][x] = get_biome(tpr, wd, wet_cutoff=wet_cutoff)
	
	return biomes
