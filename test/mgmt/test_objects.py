"""
Objects for testing sending events and managing time.
"""

from src.mgmt.listener import Listener
from src.mgmt.event import Event
from src.gameobject.gameobject import GameObject

class RocketLaunchEvent(Event):
	def __eq__(self, other):
		return isinstance(other, self.__class__)

class RocketCruiseEvent(Event):
	def __init__(self, distance):
		self.distance = distance

	def __eq__(self, other):
		return (
			isinstance(other, self.__class__) and
			other.distance == self.distance
		)

class RocketArriveEvent(Event):
	def __eq__(self, other):
		return isinstance(other, self.__class__)

class Rocket(GameObject, Listener):
	"""
	Rockets LISTEN for events for when they launch and arrive at their
	destination, and SEND events as they cruise. Their position increments
	with the passage of time.
	"""

	t = 0
	in_transit = False

	def __init__(self, game_mgr=None):
		super().__init__(game_mgr=game_mgr)
		self.evt_mgr.sub('RocketLaunchEvent', self)
		self.evt_mgr.sub('RocketArriveEvent', self)

	def update(self, event: Event):
		event_type = event.event_type
		if event_type == 'RocketLaunchEvent':
			self.in_transit = True
		if event_type == 'RocketArriveEvent':
			self.in_transit = False

	def tick(self, dt, utc):
		if self.in_transit:
			self.evt_mgr.pub(RocketCruiseEvent(utc))

class Launchpad(GameObject):
	"""
	Launchpads SEND events to rockets.
	"""

	def __init__(self, game_mgr=None):
		super().__init__(game_mgr=game_mgr)

	def launch(self):
		"""Liftoff!"""
		self.evt_mgr.pub(RocketLaunchEvent())

class Moon(GameObject, Listener):
	"""
	The Moon LISTENS for cruise events from rockets. When the Rocket gets to
	the Moon, the moon SENDS an arrive event to the Rocket.
	"""

	def __init__(self, game_mgr=None):
		super().__init__(game_mgr=game_mgr)
		self.evt_mgr.sub('RocketCruiseEvent', self)

	def update(self, event: Event):
		event_type = event.event_type
		distance = event.distance
		if event_type == 'RocketCruiseEvent' and distance == 10:
			self.evt_mgr.pub(RocketArriveEvent())

class OmniListener(Listener):
	"""Listens to everything."""
	evt_mgr = None

	def __init__(self, evt_mgr):
		self.evt_mgr = evt_mgr
		self.evt_mgr.sub('RocketLaunchEvent', self)
		self.evt_mgr.sub('RocketCruiseEvent', self)
		self.evt_mgr.sub('RocketArriveEvent', self)
