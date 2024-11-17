class Action:
	"""
	Things that the player can tell characters to do.

	Actions have a unique event ID, a display label, and an expected value
	(used for AI).
	"""
	__slots__ = ["event_id", "display_label", "expected_value"]

	def __init__(self, event_id, display_label, expected_value=None):
		self.event_id = event_id
		self.display_label = display_label
		self.expected_value = expected_value
