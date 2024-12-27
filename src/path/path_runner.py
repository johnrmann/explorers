from src.math.direction import (
	Direction,
	delta_to_direction,
	direction_to_delta
)
from src.math.vector2 import Vector2

class PathRunner:
	"""
	An object on the game grid can either be stationary, or moving on a path.
	This class represents both cases.
	"""

	_position: Vector2
	_path: list[Vector2] = []
	_idx = -1
	_direction: Direction
	_on_done = None

	# Should be between [-0.5, 0.5) which represents how far we are to the next
	# cell in the path.
	_k = 0

	def __init__(
			self,
			position = None,
			path = None,
			direction = None,
			on_done = None
	):
		if position is None:
			position = Vector2(0,0)
		if direction is None:
			direction = Direction.SOUTH
		self._direction = direction
		self._position = position
		self.path = path
		self._on_done = on_done

	def _clearPath(self):
		self._path = []
		self._k = 0
		self._idx = -1

	@property
	def position(self):
		"""
		Returns the current cell position of the object.
		"""
		if not self.is_moving:
			return self._position
		else:
			return self._path[self._idx]

	@property
	def is_moving(self):
		"""
		A path runner is moving if it has a path.
		"""
		return self._path is not None and len(self._path) > 1

	def _delta(self) -> Vector2:
		if not self.is_moving:
			return Vector2(0,0)
		now = self._path[self._idx]
		delta = Vector2(0,0)
		if self._k < 0:
			prv = self._path[self._idx - 1]
			delta = now - prv
		else:
			nxt = self._path[self._idx + 1]
			delta = nxt - now
		return delta
	
	@property
	def direction(self):
		"""
		Returns the direction the object is facing.

		Objects will have a programmer-defined initial direction (defaults to
		SOUTH), but as time --> infinity, the direction will become a function
		of the movement down the path.

		If we've completed a path, the direction will be that of the last step.
		"""
		if self.is_moving:
			delta = self._delta()
			return delta_to_direction(delta)
		else:
			return self._direction

	@property
	def draw_position(self) -> Vector2:
		"""
		Returns a floating point vector of the coordinates, in tile space (not
		screen space), of where this object should be drawn.
		"""
		if not self.is_moving:
			return self.position
		delta = self._delta() * self._k
		return self.position + delta

	@property
	def path(self):
		"""
		Returns the points left on the path.

		Setting a new path if a current one is in progress stops it.
		"""
		return self._path

	@path.setter
	def path(self, value):
		if value is None:
			self._clearPath()
		elif value[0] != self.position:
			raise ValueError("path must start at current position")
		elif len(value) == 1:
			raise ValueError("path must be longer than 1")
		else:
			self._path = value
			self._k = 0
			self._idx = 0
			last, prev_last = value[-1], value[-2]
			dir_delta = last - prev_last
			self._direction = delta_to_direction(dir_delta)

	def tick(self, dk: float):
		"""
		Evolves this object by `dk` in game time.
		"""
		if not self.is_moving:
			return
		self._k += dk
		d_idx, new_k = path_evolve_modulo(self._k)
		self._idx += d_idx
		self._k = new_k
		if self._k >= 0 and self._idx == len(self._path) - 1:
			self._position = self._path[-1]
			self._clearPath()
			if self._on_done:
				self._on_done()

def path_evolve_modulo(k: float):
	"""
	Our interpolation variable `k` should be between -0.5 and 0.5. If it goes
	beyond that, it's time to move on to the next point in the path.
	"""
	if k >= 0.5:
		return (1, k - 1.0)
	else:
		return (0, k)
