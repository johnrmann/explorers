from src.rendermath.tile import tile_z_for_width

STEPS_PER_METER = 8

def terrain_step_z_for_tile_width(tile_w):
	tile_z = tile_z_for_width(tile_w)
	return tile_z / STEPS_PER_METER
