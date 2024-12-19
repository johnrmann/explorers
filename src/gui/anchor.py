from enum import Enum

class Anchor(Enum):
	"""
	Represents the different anchor points for a GUI element.
	"""
	TOP_LEFT = 0 # default
	TOP_RIGHT = 1
	BOTTOM_LEFT = 2
	BOTTOM_RIGHT = 3
	CENTER = 4
	TOP_CENTER = 5
	BOTTOM_CENTER = 6
	LEFT_CENTER = 7
	RIGHT_CENTER = 8

def is_top_anchor(anchor):
	"""
	Returns True if the anchor is at the top of the screen.
	"""
	return anchor in (Anchor.TOP_LEFT, Anchor.TOP_RIGHT, Anchor.TOP_CENTER)

def is_bottom_anchor(anchor):
	"""
	Returns True if the anchor is at the bottom of the screen.
	"""
	return anchor in (
		Anchor.BOTTOM_LEFT, Anchor.BOTTOM_RIGHT, Anchor.BOTTOM_CENTER
	)

def is_left_anchor(anchor):
	"""
	Returns True if the anchor is at the left of the screen.
	"""
	return anchor in (Anchor.TOP_LEFT, Anchor.BOTTOM_LEFT, Anchor.LEFT_CENTER)

def is_right_anchor(anchor):
	"""
	Returns True if the anchor is at the right of the screen.
	"""
	return anchor in (
		Anchor.TOP_RIGHT, Anchor.BOTTOM_RIGHT, Anchor.RIGHT_CENTER
	)

def is_center_x_anchor(anchor):
	"""
	Returns True if the anchor is at the center of the x-axis.
	"""
	return anchor in (Anchor.CENTER, Anchor.TOP_CENTER, Anchor.BOTTOM_CENTER)

def is_center_y_anchor(anchor):
	"""
	Returns True if the anchor is at the center of the y-axis.
	"""
	return anchor in (Anchor.CENTER, Anchor.LEFT_CENTER, Anchor.RIGHT_CENTER)

def _origin_via_anchor_center(
		origin,
		dims,
		parent_dims,
		parent_origin=None,
):
	ox, oy = origin
	dx, dy = dims
	px, py = parent_origin
	pw, ph = parent_dims
	cx = (px + pw - dx) // 2
	cy = (py + ph - dy) // 2
	return cx + ox, cy + oy

def origin_via_anchor(
		origin,
		dims,
		parent_dims,
		anchor=Anchor.TOP_LEFT,
		parent_origin=None,
):
	"""
	Calcualtes the absolute origin relative to its parent and the anchor.
	"""

	if parent_origin is None:
		parent_origin = (0, 0)
	if parent_dims is None:
		raise ValueError("parent_dims must be provided")

	px, py = parent_origin
	ox, oy = origin
	pw, ph = parent_dims
	dx, dy = dims
	cx, cy = _origin_via_anchor_center(origin, dims, parent_dims, parent_origin)
	if anchor == Anchor.CENTER:
		return cx, cy

	x = px + ox
	if is_right_anchor(anchor):
		x = (px + pw - dx) - ox
	elif is_center_x_anchor(anchor):
		x = cx

	y = py + oy
	if is_bottom_anchor(anchor):
		y = (py + ph - dy) - oy
	elif is_center_y_anchor(anchor):
		y = cy

	return x, y
