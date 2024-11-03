from src.gameobject.gameobject import GameObject

class Actor(GameObject):
	_is_playable = True
	_is_played = True

	_path = None
	_path_idx = -1

	def __init__(self, pos=(0,0)):
		self.pos = pos
	
	def _set_path(self, path):
		self._path = path
		self._path_idx = 0
	
	def set_destination(self, world, dest):
		from src.path.astar import astar
		astar_path = astar(world, self.pos, dest)
		self._set_path(astar_path)

	def act(self):
		if self._path is None:
			return
		if self._path_idx == len(self._path):
			self._path = None
			self._path_idx = -1
		else:
			self.pos = self._path[self._path_idx]
			self._path_idx += 1
	
	def image_path(self):
		return "assets/img/astronaut-cropped.png"
