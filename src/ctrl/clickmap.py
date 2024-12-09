import pygame

class ClickMap:
	"""
	Used to determine whether we've clicked on terrain or game object, as
	game objects are composed of images and can't have their "is clicked?"
	calculated at random access, unlike terrain, whose (x,y,z) system makes
	such logic easy.
	"""

	screen_dimensions: tuple[int, int]

	_surface = None
	_draws = None

	_rendered_gameobject = False

	def __init__(self, screen_dimensions=None):
		if screen_dimensions is None:
			raise ValueError("Screen dimensions must be provided.")
		self.screen_dimensions = screen_dimensions
		self._surface = pygame.Surface(screen_dimensions)
		self.clear()

	def clear(self):
		"""Call this once per frame."""
		self._surface.fill((0, 0, 0))
		self._rendered_gameobject = False
		self._draws = []

	def mark_terrain(self, screen_pos, alpha_mask):
		"""
		Blit a terrain alpha mask onto the click map surface.

		Note that we make an assumption that most pixels will be terrain, so we
		don't do any bliting until we've seen at least one game object.
		"""
		if not self._rendered_gameobject:
			return
		self._surface.blit(alpha_mask, screen_pos)

	def mark_game_object(self, gobj, screen_pos, alpha_mask):
		"""
		Blit the game object alpha mask onto the click map surface.
		"""
		self._rendered_gameobject = True
		self._draws.append((gobj, screen_pos, alpha_mask))
		self._surface.blit(alpha_mask, screen_pos)
		return id

	def is_terrain(self, screen_pos):
		"""
		Returns true if the pixel at the given screen position is terrain.
		"""
		sx, sy = screen_pos
		color = self._surface.get_at((sx, sy))
		r, g, b, _ = color
		return (r == 0 and g == 0 and b == 0)

	def game_object_at(self, screen_pos):
		"""
		Returns the game object at the given screen position.
		"""
		sx, sy = screen_pos
		for gobj, gobj_screen_pos, alpha_mask in reversed(self._draws):
			px, py = gobj_screen_pos
			px, py = int(px), int(py)
			qx = px + alpha_mask.get_width()
			qy = py + alpha_mask.get_height()
			if not px <= sx < qx or not py <= sy < qy:
				continue
			color = alpha_mask.get_at((sx - px, sy - py))
			if color[0] != 0 and color[1] != 0 and color[2] != 0:
				return gobj
		return None
