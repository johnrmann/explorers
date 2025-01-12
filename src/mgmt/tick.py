"""
Anything that should update with the passage of time in the game loop should
implement the Tickable interface.
"""

class Tickable:
	"""See module docstring."""

	def tick(self, dt: float, utc: float):
		"""Do something every frame."""
		return

	def tick_second(self, dt: float, utc: float):
		"""Do something every second."""
		return
