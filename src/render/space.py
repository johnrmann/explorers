"""
Functions for transforming between tile space and screen space.
"""

from src.math.direction import Direction

def tile_screen_transform(p, orientation: Direction):
	x, y = p
	if orientation == Direction.NORTHWEST:
		return (x - y, x + y)
	elif orientation == Direction.NORTHEAST:
		return (x + y, y - x)
	elif orientation == Direction.SOUTHEAST:
		return (y - x, -(x + y))
	elif orientation == Direction.SOUTHWEST:
		return (-(x + y), -(y - x))
	raise ArithmeticError("Unsupported orientation.")
