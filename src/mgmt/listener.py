from src.mgmt.event import Event

class Listener:
	"""
	Use this interface to get events from the event manager.
	"""

	def update(self, event: Event):
		"""
		Called once per event per frame when events happen.
		"""
		raise NotImplementedError("update not implemented")
