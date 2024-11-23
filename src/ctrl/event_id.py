"""
Defines constants for types of control events.
"""

from src.mgmt.event import Event
from src.math.direction import Direction

EVENT_CAMERA_MOVE = 'camera.move'
EVENT_CAMERA_ZOOM = 'camera.zoom'
EVENT_CAMERA_ROTATE = 'camera.rotate'

EVENT_MOUSE_CLICK_WORLD = 'mouse.click.world'
EVENT_MOUSE_CLICK_OBJECT = 'mouse.click.object'

EVENT_MOUSE_CLICK_GUI = 'mouse.click.gui'

class CameraMoveEvent(Event):
	"""
	An event to tell the camera to move in a direction.
	"""

	direction: Direction

	def __init__(self, direction: Direction):
		super().__init__(event_type=EVENT_CAMERA_MOVE)
		self.direction = direction

	def __eq__(self, other):
		return (
			other.event_type == self.event_type and
			other.direction == self.direction
		)

class CameraZoomEvent(Event):
	"""
	An event to tell the camera to zoom in or out.
	"""

	delta: int

	def __init__(self, delta: int):
		super().__init__(event_type=EVENT_CAMERA_ZOOM)
		self.delta = delta

	def __eq__(self, other):
		return (
			other.event_type == self.event_type and
			other.delta == self.delta
		)

class CameraRotateEvent(Event):
	"""
	An event to tell the camera to turn 90deg (counter-)clockwise.
	"""

	delta: int

	def __init__(self, delta: int):
		super().__init__(event_type=EVENT_CAMERA_ROTATE)
		self.delta = delta

	def __eq__(self, other):
		return (
			other.event_type == self.event_type and
			other.delta == self.delta
		)
