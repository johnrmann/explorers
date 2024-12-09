from src.gameobject.gameobject import GameObject
from src.gameobject.action import Action

from src.math.vector2 import Vector2
from src.path.path_runner import PathRunner
from src.mgmt.listener import Listener
from src.mgmt.event import Event

from src.gameobject.actor_motives import (
	ActorMotiveVector,
	BASE_MOTIVE_DELTAS,
	MOVEMENT_MOTIVE_DELTAS,
)

class Actor(GameObject, Listener):
	"""
	This class represents characters in the game.
	"""

	_is_playable = True
	_dead = False

	_path_runner: PathRunner = None
	_action: Action = None

	name: str

	motives: ActorMotiveVector = None

	def __init__(self, game_mgr=None, pos=None, speed=5, owner=0, name=None):
		if name is None:
			name = "Default"
		if not pos:
			pos = Vector2(0,0)
		super().__init__(game_mgr=game_mgr, pos=pos, owner=owner)
		self._path_runner = PathRunner(
			position=pos,
			on_done=self._finished_path
		)
		self.name = name
		self.motives = ActorMotiveVector(maxs=100)
		self.size = (1,1,5)
		# Speed is given in cells per second.
		self.speed = speed
		# Subscribe to events.
		self.evt_mgr.sub("main.character.go", self)
		self.evt_mgr.sub("main.character.action", self)
		self.evt_mgr.sub("rabbit_hole.enter", self)
		self.evt_mgr.sub("rabbit_hole.exit", self)

	def update(self, event: Event):
		if isinstance(event, MoveActorEvent) and event.actor == self:
			self.set_destination(event.to_position)
		elif isinstance(event, ActorDoActionEvent) and event.actor == self:
			self.set_destination(event.action.position)
			self._action = event.action
		elif event.event_type == 'rabbit_hole.enter' and event.actor == self:
			self.hidden = True
		elif event.event_type == 'rabbit_hole.exit' and event.actor == self:
			self.hidden = False

	@property
	def pos(self):
		return self._path_runner.position

	@property
	def direction(self):
		return self._path_runner.direction

	@property
	def draw_position(self):
		return self._path_runner.draw_position

	@property
	def is_moving(self):
		"""Is the actor currently running a path?"""
		return self._path_runner.is_moving

	def is_dead(self):
		"""Is the actor dead?"""
		return self.motives.is_dead()

	def set_destination(self, dest):
		self._action = None
		from src.path.astar import astar
		world = self.game_mgr.world
		astar_path = astar(world, self.pos, dest)
		self._path_runner.path = astar_path

	def _finished_path(self):
		if self._action:
			self.evt_mgr.pub(self._action.event)
			self._action = None

	def _tick_motives(self, dt: float):
		d_motives = ActorMotiveVector(BASE_MOTIVE_DELTAS) * dt
		if self.is_moving:
			d_motives.mutate(ActorMotiveVector(MOVEMENT_MOTIVE_DELTAS) * dt)
		self.motives.mutate(d_motives)
		if self.is_dead():
			self.evt_mgr.pub(ActorDiedEvent(actor=self))

	def tick(self, dt: float, utc: float):
		self._path_runner.tick(dt * self.speed)
		self._tick_motives(dt)

	def image_path(self):
		return "assets/img/astronaut-cropped.png"

class MoveActorEvent(Event):
	"""
	An event to tell an actor to move to a position on the map.
	"""

	actor: Actor
	to_position: Vector2

	def __init__(
			self,
			actor: Actor = None,
			to_position: Vector2 = None
	):
		super().__init__(event_type="main.character.go")
		self.actor = actor
		self.to_position = to_position

	def __eq__(self, other):
		if not isinstance(other, MoveActorEvent):
			return False
		return (
			other.actor == self.actor and
			other.to_position == self.to_position
		)

class ActorDoActionEvent(Event):
	"""
	An event to tell an actor to do an action.
	"""

	actor: Actor
	action: Action

	def __init__(
			self,
			actor: Actor = None,
			action: Action = None
	):
		super().__init__(event_type="main.character.action")
		self.actor = actor
		self.action = action

	def __eq__(self, other):
		if not isinstance(other, ActorDoActionEvent):
			return False
		return (
			other.actor == self.actor and
			other.action == self.action
		)

class ActorDiedEvent(Event):
	"""
	An event broadcasted by an actor indicating that they just died :-(
	"""

	actor: Actor

	def __init__(self, actor: Actor = None):
		super().__init__(event_type="character.died")
		self.actor = actor

	def __eq__(self, other):
		if not isinstance(other, ActorDiedEvent):
			return False
		return (
			other.actor == self.actor
		)
