"""
This module provides functions to determine the draw order vector and offset
tiles by the draw order vector based on the camera orientation.
"""

from src.math.vector2 import Vector2, vector2_rotate_point
from src.math.direction import Direction, direction_to_delta, quarter_turns_between_directions

def draw_order_next_column(
		cell_pos: Vector2,
		cam_dir: Direction
) -> Vector2:
	dx, dy = 1, -1
	if cam_dir != Direction.NORTHWEST:
		raise NotImplementedError("Only northwest is supported")
	x, y = cell_pos
	return Vector2(x + dx, y + dy)

def draw_order_next_row(
		cell_pos: Vector2,
		cam_dir: Direction,
		carry: bool,
) -> Vector2:
	dy = 1 if carry else 0
	dx = 0 if carry else 1
	if cam_dir != Direction.NORTHWEST:
		raise NotImplementedError("Only northwest is supported")
	x, y = cell_pos
	return Vector2(x + dx, y + dy)

def cells_in_draw_order(
		origin: Vector2,
		cam_dir: Direction,
		num_cols: int,
		num_rows: int,
):
	carry = True
	x, y = origin
	for _ in range(num_rows):
		next_x, next_y = draw_order_next_row((x, y), cam_dir, carry)
		for _ in range(num_cols):
			yield (x, y)
			x, y = draw_order_next_column((x, y), cam_dir)
		x, y = next_x, next_y
		carry = not carry

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
