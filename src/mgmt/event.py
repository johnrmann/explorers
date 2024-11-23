class Event:
	"""
	Base type for events, which are messages broadcasted between different
	objects in the game.
	"""

	event_type: str

	def __init__(self, event_type: str = None):
		if event_type is None:
			raise ValueError("Event type must be defined")
		self.event_type = event_type
