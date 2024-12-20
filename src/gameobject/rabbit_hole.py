from src.mgmt.event import Event

from src.gameobject.actor import Actor

class RabbitHole:
	"""
	An interface to be extended by GameObjects that characters can
	disappear into.
	"""

	max_capacity: int
	capacity: int

	inside: set[Actor]

	def __init__(self, max_capacity=1):
		self.max_capacity = max_capacity
		self.capacity = max_capacity
		self.inside = set()

	def is_full(self):
		"""Can the rabbit hole hold any more actors?"""
		return self.capacity == 0

	def enter(self, actor: Actor):
		"""Put an actor inside a rabbit hole."""
		if self.capacity == 0:
			return False
		self.inside.add(actor)
		self.capacity -= 1
		return True

	def exit(self, actor: Actor):
		"""Remove an actor from a rabbit hole."""
		if actor in self.inside:
			self.inside.remove(actor)
			self.capacity += 1
			return True
		return False

class EnterRabbitHoleEvent(Event):
	"""
	This event fires when an actor enters a rabbit hole, and therefore should
	be hidden from the map.
	"""

	data = None

	def __init__(self, actor=None, rabbit_hole=None, data=None):
		self.actor = actor
		self.rabbit_hole = rabbit_hole
		self.data = data

	def __eq__(self, other):
		if not isinstance(other, EnterRabbitHoleEvent):
			return False
		return (
			self.actor == other.actor and
			self.rabbit_hole == other.rabbit_hole
		)

class ExitRabbitHoleEvent(Event):
	"""
	This event fires when an actor leaves a rabbit hole, and therefore should
	be shown on the map again.
	"""

	def __init__(self, actor=None, rabbit_hole=None):
		self.actor = actor
		self.rabbit_hole = rabbit_hole

	def __eq__(self, other):
		if not isinstance(other, ExitRabbitHoleEvent):
			return False
		return (
			self.actor == other.actor and
			self.rabbit_hole == other.rabbit_hole
		)
