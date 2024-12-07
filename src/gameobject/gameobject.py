from src.math.direction import Direction
from src.math.cart_prod import spatial_cart_prod
from src.math.vector2 import Vector2

from src.rendermath.box import Box

from src.gameobject.constants import NO_OWNER

class GameObject:
	"""
	Represents a thing in the game world. Can be a character, a prop, or
	invisible tiles that can be interacted with.
	"""

	evt_mgr = None
	_pos = (0, 0)
	hidden: bool = False

	owner: int = NO_OWNER

	def __init__(self, game_mgr=None, pos = None, size = None, owner = 0):
		"""
		Position is the top left cell that the game object occupies.
		"""
		if pos is None:
			pos = (0, 0)
		if size is None:
			size = (1, 1, 1)
		if game_mgr is None:
			from src.mgmt.singletons import get_game_manager
			game_mgr = get_game_manager()
		self._pos = pos
		self.size = size
		self.game_mgr = game_mgr
		self.evt_mgr = game_mgr.evt_mgr
		self.owner = owner

	@property
	def pos(self):
		return self._pos

	@property
	def draw_position(self) -> Vector2:
		x, y = self.pos
		sx, sy, _ = self.size
		return (x + (sx / 2), y + (sy / 2))

	def x_range(self):
		"""
		The x-range this object occupies.
		"""
		x, _ = self.pos
		w, _, _ = self.size
		return range(x, x + w)

	def y_range(self):
		"""
		The y-range this object occupies.
		"""
		_, y = self.pos
		_, h, _ = self.size
		return range(y, y + h)

	def bounding_box(self):
		"""
		Returns the bounding box that this game object occupies.
		"""
		x, y = self.pos
		z = self.game_mgr.world.terrain.height_at(self.pos) // 8 # TODO(jm)
		return Box(p=(x, y, z), size=self.size)

	def cells_occupied(self, view_sort = Direction.NORTHWEST):
		"""
		Returns an array of cells that this object occupies. Optional view_sort
		is nice for determining draw order.
		"""
		xs = self.x_range()
		ys = self.y_range()
		return spatial_cart_prod(xs, ys, view_sort)

	def draw_point(self, camera_direction):
		"""
		Returns the point the object occupies that's closest to the camera.
		"""
		x, y = self.pos
		w, h, _ = self.size
		if camera_direction == Direction.NORTHWEST:
			return (x + w, y + h)
		elif camera_direction == Direction.NORTHEAST:
			return (x, y + h)
		elif camera_direction == Direction.SOUTHEAST:
			return (x + w, y)
		elif camera_direction == Direction.SOUTHWEST:
			return (x, y)
		return (x + w, y + h)

	def image_path(self):
		"""
		Override this to specify an image to render.
		"""
		return None

	def tick(self, dt: float, utc: float):
		"""
		Signal from the game manager that time has passed. dt is the time since
		the last draw in seconds. UTC is time since mission start in seconds.
		"""
		pass
