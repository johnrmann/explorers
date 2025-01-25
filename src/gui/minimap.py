import pygame

from src.gui.gui import GuiElement

_ICE_COLOR = (250, 250, 250)
_OCEAN_COLOR = (0, 0, 200)

def minimap_image(terrain, surface_dimensions):
	"""
	Render a minimap image of the world.
	"""

	surface = pygame.Surface(terrain.dimensions)

	d_height = terrain.max_tile_height - terrain.min_tile_height
	min_tile_height = terrain.min_tile_height

	for x in range(terrain.width):
		for y in range(terrain.height):
			cell = terrain.map[y][x]
			cell_p = (cell - min_tile_height) / d_height
			color_scale = int((cell_p * 128) + 127)
			color = (color_scale, 0, 0)
			if terrain.is_cell_ice((x, y)):
				color = _ICE_COLOR
			elif terrain.is_cell_water((x, y)):
				color = _OCEAN_COLOR
			surface.set_at((x, y), color)

	surface = pygame.transform.scale(surface, surface_dimensions)
	return surface.convert()

class MiniMap(GuiElement):
	"""
	A clickable map of the world.
	"""

	_surface = None
	_draw_surface = None

	world = None
	viewport = None

	def __init__(self, world=None, viewport=None, **kwargs):
		self.world = world
		self.viewport = viewport
		super().__init__(**kwargs)
		self._prepare_minimap()

	def _prepare_minimap(self):
		self._surface = minimap_image(self.world.terrain, self.dimensions)
		self._draw_surface = self._surface.copy()

	def _draw_viewport(self):
		# TODO(jm) -- need to make this sensitive to zoom.
		cx, cy = self.viewport.camera_pos
		px = cx / self.world.terrain.width
		py = cy / self.world.terrain.height
		x = int(px * self._surface.get_width())
		y = int(py * self._surface.get_height())
		pygame.draw.circle(
			self._draw_surface,
			(0, 255, 0),
			(x, y),
			10,
			width=1
		)

	def my_draw(self, screen):
		self._draw_surface = self._surface.copy()
		self._draw_viewport()
		screen.blit(self._draw_surface, self.pygame_rect)

	def process_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.pygame_rect.collidepoint(event.pos):
				tx = self.world.terrain.width
				ty = self.world.terrain.height
				x, y = event.pos
				x -= self.pygame_rect.x
				y -= self.pygame_rect.y
				x = int(x / self._surface.get_width() * tx)
				y = int(y / self._surface.get_height() * ty)
				self.viewport.camera_pos = (x, y)
				return True
		return False
