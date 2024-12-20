class Event:
	"""
	Base type for events, which are messages broadcasted between different
	objects in the game.
	"""

	@property
	def event_type(self):
		"""Easy access to this class name."""
		return self.__class__.__name__
