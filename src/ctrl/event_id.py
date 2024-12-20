"""
Defines constants for types of control events.
"""

from src.mgmt.event import Event
from src.math.direction import Direction

class CameraMoveEvent(Event):
	"""
	An event to tell the camera to move in a direction.
	"""

	direction: Direction

	def __init__(self, direction: Direction):
		self.direction = direction

	def __eq__(self, other):
		return (
			isinstance(other, self.__class__) and
			other.direction == self.direction
		)

class CameraZoomEvent(Event):
	"""
	An event to tell the camera to zoom in or out.
	"""

	delta: int

	def __init__(self, delta: int):
		self.delta = delta

	def __eq__(self, other):
		return (
			isinstance(other, self.__class__) and
			other.delta == self.delta
		)

class CameraRotateEvent(Event):
	"""
	An event to tell the camera to turn 90deg (counter-)clockwise.
	"""

	delta: int

	def __init__(self, delta: int):
		self.delta = delta

	def __eq__(self, other):
		return (
			isinstance(other, self.__class__) and
			other.delta == self.delta
		)
