from src.math.vector2 import Vector2

EVENT_ID__DO_ACTION = "event.action.do"

class Action:
	"""
	Things that the player can tell characters to do.

	Actions have a unique event ID, a display label, and an expected value
	(used for AI).
	"""
	__slots__ = ["event", "display_label", "expected_value", "target", "offset"]

	def __init__(
			self,
			event=None,
			display_label=None,
			target=None,
			offset: Vector2 = None,
			expected_value=None,
		):
		self.event = event
		self.display_label = display_label
		self.expected_value = expected_value
		self.target = target
		self.offset = offset

	@property
	def position(self):
		"""
		Where the action is targeting. If an offset is set, the offset is added
		to the object's position.

		It's strongly rec'd that you use an offset because most game objects
		will mark their position as OCCUPIED.
		"""
		if not self.offset:
			return self.target.pos
		ox, oy = self.target.pos
		dx, dy = self.offset
		return Vector2(ox + dx, oy + dy)
