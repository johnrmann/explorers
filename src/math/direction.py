"""
Enums and functions useful for translation in space.
"""

from enum import Enum

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
	NORTHEAST = 4
	SOUTHEAST = 5
	SOUTHWEST = 6
	NORTHWEST = 7

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

DEFAULT_CAMERA_ORIENTATION = Direction.NORTHWEST

def direction_opposite(direction: Direction):
	"""
	Return the opposite of a given direction.
	"""
	return OPPOSITES.get(direction)

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
	if orientation == Direction.NORTHWEST:
		return Direction.SOUTH
	pass

def right_wall_direction(orientation: Direction):
	"""
	Read the docs for left_wall_direction.
	"""
	if orientation == Direction.NORTHWEST:
		return Direction.EAST
	pass

def left_ridge_direction(orientation: Direction):
	return direction_opposite(right_wall_direction(orientation))

def right_ridge_direction(orientation: Direction):
	return direction_opposite(left_wall_direction(orientation))
