"""
Objects for testing sending events and managing time.
"""

from src.mgmt.listener import Listener
from src.mgmt.event import Event
from src.gameobject.gameobject import GameObject

class RocketLaunchEvent(Event):
	def __init__(self):
		super().__init__(event_type='rocket_launch')

	def __eq__(self, other):
		return self.event_type == other.event_type

class RocketCruiseEvent(Event):
	def __init__(self, distance):
		super().__init__(event_type='rocket_cruise')
		self.distance = distance

	def __eq__(self, other):
		return (
			other.event_type == self.event_type and
			other.distance == self.distance
		)

class RocketArriveEvent(Event):
	def __init__(self):
		super().__init__(event_type='rocket_arrive')

	def __eq__(self, other):
		return self.event_type == other.event_type

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
		self.evt_mgr.sub('rocket_launch', self)
		self.evt_mgr.sub('rocket_arrive', self)

	def update(self, event: Event):
		event_type = event.event_type
		if event_type == 'rocket_launch':
			self.in_transit = True
		if event_type == 'rocket_arrive':
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
		self.evt_mgr.sub('rocket_cruise', self)

	def update(self, event: Event):
		event_type = event.event_type
		distance = event.distance
		if event_type == 'rocket_cruise' and distance == 10:
			self.evt_mgr.pub(RocketArriveEvent())

class OmniListener(Listener):
	"""Listens to everything."""
	evt_mgr = None

	def __init__(self, evt_mgr):
		self.evt_mgr = evt_mgr
		self.evt_mgr.sub('rocket_launch', self)
		self.evt_mgr.sub('rocket_cruise', self)
		self.evt_mgr.sub('rocket_arrive', self)
