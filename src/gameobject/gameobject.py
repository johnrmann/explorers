
from src.math.direction import Direction
from src.math.cart_prod import spatial_cart_prod
from src.math.vector2 import Vector2

from src.gameobject.constants import NO_OWNER

class GameObject:
	"""
	Represents a thing in the game world. Can be a character, a prop, or
	invisible tiles that can be interacted with.
	"""

	_pos = (0, 0)

	evt_mgr = None
	game_mgr = None
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
		elif len(size) == 2:
			size = (size[0], size[1], None)
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
		"""
		Returns the 2D position of the object.
		"""
		return self._pos

	@pos.setter
	def pos(self, new_pos):
		self._pos = new_pos

	@property
	def pos3(self):
		"""
		Returns the 3D position of the object, with the z-coordinate being the
		height of the terrain at that position.
		"""
		x, y = self.pos
		return (x, y, self.game_mgr.world.terrain.height_at(self.pos))

	@property
	def draw_position(self) -> Vector2:
		"""
		The position of the object must be an integer. The draw position can be
		a float to represent an interpolated position for rendering purposes.
		"""
		return self.pos

	@property
	def draw_bounds(self):
		"""
		Returns a tuple of two points that represent the bounding box of the
		object when rendered.
		"""
		x, y = self.draw_position
		w, h, _ = self.size
		return ((x, y), (x + w - 1, y + h - 1))

	def on_init(self):
		"""
		Called when the object is added to the game manager.
		"""
		pass

	def on_remove(self):
		"""
		Called when the object is removed from the game world.
		"""
		pass

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

	def cells_occupied(self, view_sort = Direction.NORTHWEST):
		"""
		Returns an array of cells that this object occupies. Optional view_sort
		is nice for determining draw order.
		"""
		xs = self.x_range()
		ys = self.y_range()
		return spatial_cart_prod(xs, ys, view_sort)

	def occupies_cell(self, position):
		"""
		Returns True if the given position is occupied by this object.
		"""
		min_x, min_y = self.pos
		max_x = min_x + self.size[0]
		max_y = min_y + self.size[1]
		x, y = position
		return min_x <= x < max_x and min_y <= y < max_y

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

	def image_path(self) -> str:
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
