"""
This module provides functions to determine the draw order vector and offset
tiles by the draw order vector based on the camera orientation.
"""

from src.math.vector2 import Vector2
from src.math.direction import Direction, direction_to_delta

def draw_order_vector(camera_orientation: Direction) -> Vector2:
	"""
	The draw order vector is the vector along which we draw rows of
	tiles.

	For example, if the camera is pointing to the northwest, we want to
	draw the northwest tiles first, and the southeast tiles last. Therefore,
	the draw order vector is southeast.
	"""
	dx, dy = direction_to_delta(camera_orientation)
	return Vector2(-dx, -dy)

def offset_tile_by_draw_order_vector(
		p: Vector2,
		camera_orientation: Direction,
		k: int,
) -> tuple[Vector2, Vector2]:
	"""
	The idea is that if the camera orientation is pointed to the northwest,
	the order draw vector goes from the northwest to the southeast, so
	incrementing by k means we return k tiles to the southeast.

	If the offset is odd, it will return two tiles.
	"""
	if k == 0:
		return p, p
	offset_vector = draw_order_vector(camera_orientation)
	ox, oy = offset_vector
	even_offset = k // 2
	is_odd = k % 2
	offset = (offset_vector * even_offset)
	q = p + offset
	if is_odd:
		return (q + Vector2(ox, 0), q + Vector2(0, oy))
	else:
		return q, q
