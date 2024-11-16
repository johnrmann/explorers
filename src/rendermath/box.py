"""
Functions for computing the isometric draw order of cubes.
"""

from src.math.direction import Direction, quarter_turns_between_directions
from src.math.vector3 import vector3_rotate_points

from src.rendermath.multicell import multicell_polygon_on_global_screen
from src.rendermath.tile import tile_z_for_width
from src.rendermath.geometry import is_point_in_hexagon

class Box:
	"""
	A box is a rectangular prism. The origin (p) and anti-origin are points,
	not cells, meaning that a 1x1x1 point at 0,0,0 has an anti-origin
	1,1,1.
	"""

	p = (0, 0, 0)
	q = (0, 0, 0)
	size = (0, 0, 0)

	def __init__(self, p=None, q=None, size=None):
		if p is None:
			raise ValueError("Origin must be defined.")
		self.p = p
		px, py, pz = p
		neither = q is None and size is None
		both = q is not None and size is not None
		if neither or both:
			raise ValueError("Either an antiorigin xor size must be defined.")
		if size is not None:
			sx, sy, sz = size
			self.size = size
			self.q = (px + sx, py + sy, pz + sz)
		if q is not None:
			qx, qy, qz = q
			self.size = (qx - py, qy - py, qz - pz)
			self.q = q

	def multicell(self):
		"""
		Returns the bottom multicell of the box. Notice that here we are
		dealing with cells, not points. A 1x1x1 box at 0,0,0 will touch points
		between 0,0,0 and 1,1,1 but will have a multicell of (0,0), (0,0).
		"""
		px, py, _ = self.p
		sx, sy, _ = self.size
		return ((px, py), (px + sx - 1, py + sy -1))

def box_to_global_screen_projection(cube: Box, cam_dir, tile_dims):
	"""
	Given a cube = (position, size), returns the two points that bind the cube.
	"""
	tile_width, _ = tile_dims
	bottom_multicell = cube.multicell()
	_, _, sz = cube.size
	bottom_proj = multicell_polygon_on_global_screen(
		bottom_multicell,
		cam_dir,
		tile_dims
	)
	dz_pixels = tile_z_for_width(tile_width) * sz
	top_proj = [
		(x, y - dz_pixels) for x, y in bottom_proj
	]
	_, bot_right, bot_bot, bot_left = bottom_proj
	top_top, top_right, _, top_left = top_proj
	return (
		top_top, top_right, bot_right, bot_bot, bot_left, top_left
	)

def are_boxes_overlapping(box1: Box, box2: Box, cam_dir, tile_dims):
	"""
	Two boxes overlap if their hex projections overlap.
	"""
	proj1 = box_to_global_screen_projection(box1, cam_dir, tile_dims)
	proj2 = box_to_global_screen_projection(box2, cam_dir, tile_dims)
	for p in proj1:
		if is_point_in_hexagon(p, proj2):
			return True
	return False

def _transform_box_coords(box: Box, cam_dir=Direction.NORTHWEST):
	dir_diff = quarter_turns_between_directions(Direction.NORTHWEST, cam_dir)
	return vector3_rotate_points([box.p, box.q], quarter_turns=dir_diff)

def compare_boxes(
		box1: Box,
		box2: Box,
		cam_dir=Direction.NORTHWEST,
		tile_dims=None
):
	"""
	Return 1 if box1 should be drawn before box2, and -1 if box2 should be
	drawn before box1. Return 0 if they can be drawn in any order.
	"""
	if tile_dims is None:
		tile_dims = (48, 24)
	if not are_boxes_overlapping(box1, box2, cam_dir, tile_dims):
		return 0
	min1, max1 = _transform_box_coords(box1, cam_dir=cam_dir)
	min2, max2 = _transform_box_coords(box2, cam_dir=cam_dir)
	if min2.x >= max1.x:
		return 1
	if max2.x <= min1.x:
		return -1
	if min2.y >= max1.y:
		return 1
	if max2.y <= min1.y:
		return -1
	if min1.z >= max2.z:
		return -1
	if min2.z >= max1.z:
		return 1
	return 0
