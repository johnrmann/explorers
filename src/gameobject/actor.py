from src.gameobject.gameobject import GameObject

from src.math.vector2 import Vector2
from src.path.path_runner import PathRunner
from src.mgmt.listener import Listener

from src.gameobject.actor_motives import (
	ActorMotiveVector,
	BASE_MOTIVE_DELTAS,
	MOVEMENT_MOTIVE_DELTAS,
)

class Actor(GameObject, Listener):
	_is_playable = True
	_is_played = True
	_dead = False

	_path_runner = PathRunner()

	def __init__(self, game_mgr=None, pos=None, speed=5):
		if not pos:
			pos = Vector2(0,0)
		super().__init__(game_mgr=game_mgr, pos=pos)
		self._path_runner = PathRunner(position=pos)
		self.motives = ActorMotiveVector()
		self.size = (1,1,5)
		# Speed is given in cells per second.
		self.speed = speed
		self.evt_mgr.sub("main.character.go", self)
	
	def update(self, event_type, data):
		if event_type == "main.character.go":
			self.set_destination(data)

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
		return self._path_runner.is_moving

	def is_dead(self):
		return self.motives.is_dead()

	def set_destination(self, dest):
		from src.path.astar import astar
		from src.mgmt.singletons import get_game_manager
		world = get_game_manager().world
		astar_path = astar(world, self.pos, dest)
		self._path_runner.path = astar_path

	def _tick_motives(self, dt: float):
		d_motives = ActorMotiveVector(BASE_MOTIVE_DELTAS) * dt
		if self.is_moving:
			d_motives.mutate(ActorMotiveVector(MOVEMENT_MOTIVE_DELTAS) * dt)
		self.motives.mutate(d_motives)
		if self.is_dead():
			self.evt_mgr.pub("character.died", self)

	def tick(self, dt: float, t: float):
		self._path_runner.tick(dt * self.speed)
		self._tick_motives(dt)

	def image_path(self):
		return "assets/img/astronaut-cropped.png"
