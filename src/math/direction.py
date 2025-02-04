"""
Enums and functions useful for translation in space.
"""

from enum import Enum
from functools import cache

from src.math.vector2 import Vector2

class Direction(Enum):
	"""
	Represents a direction that we can move. The cardinal directions are
	grouped together for convenience since there are cases where we use
	them and do not use diagonals.
	"""
	# Cardinals
	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3
	# Diagonals
	NORTHWEST = 4
	NORTHEAST = 5
	SOUTHEAST = 6
	SOUTHWEST = 7

OPPOSITES = {
	Direction.NORTH: Direction.SOUTH,
	Direction.SOUTH: Direction.NORTH,
	Direction.EAST: Direction.WEST,
	Direction.WEST: Direction.EAST,
	Direction.NORTHEAST: Direction.SOUTHWEST,
	Direction.SOUTHEAST: Direction.NORTHWEST,
	Direction.SOUTHWEST: Direction.NORTHEAST,
	Direction.NORTHWEST: Direction.SOUTHEAST,
}

CARDINAL_DIRECTIONS = set([
	Direction.NORTH,
	Direction.EAST,
	Direction.SOUTH,
	Direction.WEST
])

DIAGONAL_DIRECTIONS = set([
	Direction.NORTHWEST,
	Direction.NORTHEAST,
	Direction.SOUTHEAST,
	Direction.SOUTHWEST
])

DIRECTIONS_CLOCKWISE_ORDER = [
	Direction.NORTH,
	Direction.NORTHEAST,
	Direction.EAST,
	Direction.SOUTHEAST,
	Direction.SOUTH,
	Direction.SOUTHWEST,
	Direction.WEST,
	Direction.NORTHWEST
]

DEFAULT_CAMERA_ORIENTATION = Direction.NORTHWEST

def direction_opposite(direction: Direction):
	"""
	Return the opposite of a given direction.
	"""
	return OPPOSITES.get(direction)

def quarter_turns_between_directions(d1: Direction, d2: Direction):
	"""
	Returns the number of clockwise quarter turns between directions.
	"""
	diff = 0
	if is_direction_diagonal(d1) and is_direction_diagonal(d2):
		diff = d2.value - d1.value
	elif not is_direction_diagonal(d1) and not is_direction_diagonal(d2):
		diff = d2.value - d1.value
	else:
		raise ValueError("Cannot have quarter turns btwn these directions")
	return diff % 4

def direction_rotate_90(direction: Direction, quarter_turns = 1):
	"""
	Rotates direction clockwise.

	North --> East
	West --> North
	Northeast --> Southeast
	"""
	if quarter_turns == 0:
		return direction
	base = 0 if not is_direction_diagonal(direction) else 4
	new_val = (((direction.value - base) + quarter_turns) % 4) + base
	return Direction(new_val)

def direction_rotate_45(direction: Direction, eighth_turns = 1):
	"""
	Rotates direction clockwise.
	
	North --> Northeast
	Northwest --> North
	"""
	current = DIRECTIONS_CLOCKWISE_ORDER.index(direction)
	new_idx = (current + eighth_turns) % len(DIRECTIONS_CLOCKWISE_ORDER)
	return DIRECTIONS_CLOCKWISE_ORDER[new_idx]

def direction_to_delta(direction: Direction):
	"""
	Converts direction enumeration to (dx,dy).
	"""
	if direction == Direction.NORTH:
		return (0, -1)
	elif direction == Direction.NORTHEAST:
		return (1, -1)
	elif direction == Direction.EAST:
		return (1, 0)
	elif direction == Direction.SOUTHEAST:
		return (1, 1)
	elif direction == Direction.SOUTH:
		return (0, 1)
	elif direction == Direction.SOUTHWEST:
		return (-1, 1)
	elif direction == Direction.WEST:
		return (-1, 0)
	elif direction == Direction.NORTHWEST:
		return (-1, -1)
	raise AttributeError("Unknown direction")

def delta_to_direction(v: Vector2) -> Direction:
	"""
	Takes in a (dx, dy) vector and returns the compass direction it's
	pointing in. If no direction exists in the enumeration, an error is thrown.
	"""
	vx, vy = v
	if vx == 0 and vy < 0:
		return Direction.NORTH
	elif vx > 0 and vy == 0:
		return Direction.EAST
	elif vx == 0 and vy > 0:
		return Direction.SOUTH
	elif vx < 0 and vy == 0:
		return Direction.WEST
	elif vx < 0 and vy < 0 and abs(vx) == abs(vy):
		return Direction.NORTHWEST
	elif vx > 0 and vy < 0 and abs(vx) == abs(vy):
		return Direction.NORTHEAST
	elif vx > 0 and vy > 0 and abs(vx) == abs(vy):
		return Direction.SOUTHEAST
	elif vx < 0 and vy > 0 and abs(vx) == abs(vy):
		return Direction.SOUTHWEST
	raise ValueError("Unknown direction")

@cache
def is_direction_diagonal(direction: Direction):
	"""
	Returns true if the direction is not a cardinal direction.
	"""
	return not Direction.NORTH.value <= direction.value <= Direction.WEST.value

def left_wall_direction(orientation: Direction):
	"""
	Which direciton is the left wall (as in screen left) for an isometric cell?

	For example, the default case where the camera is facing NW, the bottom edge
	of the cell is SE. The left wall is therefore facing south and the right
	wall is facing east.
	"""
	return direction_rotate_45(orientation, eighth_turns=5)

def right_wall_direction(orientation: Direction):
	"""
	Read the docs for left_wall_direction.
	"""
	return direction_rotate_45(orientation, eighth_turns=3)

def left_ridge_direction(orientation: Direction):
	"""
	We call lines drawn between tiles of different height to make the height
	diff apparent "ridges."

	If the camera is facing Northwest, the left ridge should be opposite of
	the right wall.
	"""
	return direction_opposite(right_wall_direction(orientation))

def right_ridge_direction(orientation: Direction):
	"""
	Read the docs for right_ridge_direction.
	"""
	return direction_opposite(left_wall_direction(orientation))
