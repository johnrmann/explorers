from src.gameobject.gameobject import GameObject

from src.math.vector2 import Vector2
from src.path.path_runner import PathRunner

class Actor(GameObject):
	_is_playable = True
	_is_played = True

	_path_runner = PathRunner()

	def __init__(self, pos=None, speed=5):
		if not pos:
			pos = Vector2(0,0)
		self._path_runner = PathRunner(position=pos)
		self.size = (1,1)
		# Speed is given in cells per second.
		self.speed = speed
	
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
	
	def set_destination(self, world, dest):
		from src.path.astar import astar
		astar_path = astar(world, self.pos, dest)
		self._path_runner.path = astar_path

	def act(self, dt: float):
		self._path_runner.tick(dt * self.speed)
	
	def image_path(self):
		return "assets/img/astronaut-cropped.png"
