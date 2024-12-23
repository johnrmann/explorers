from src.render.utils import (
	alpha_mask_from_surface,
	resize_surface,
	relight_surface,
)

DEFAULT_LIGHT_LEVEL = 1.0

DEFAULT_ZOOM_FACTOR = 1.0

NUM_LIGHT_LEVELS = 8
LIGHT_LEVELS = [
	0.3 + (0.1 * i) for i in range(NUM_LIGHT_LEVELS - 1)
] + [1.0]

MIN_LIGHT_LEVEL_IDX = 0
MAX_LIGHT_LEVEL_IDX = NUM_LIGHT_LEVELS - 1

class MultiSurface:
	"""
	Give this class a surface and it will...

		-	Resize it for different zooms.

		-	Create an alpha mask for it (at different zooms!).

		-	Relight it for different light levels.
	"""

	# Surface cache is a dict of zoom factors to brightness levels to surfaces.
	_cache = None

	# Alpha cache is a dict of zoom factors to alpha masks. No need to cache
	# different light levels here since we don't care about that with alpha
	# masks.
	_alpha_cache = None

	_zooms: list[float]
	_light_levels: list[float]

	_using_light: bool = False
	_default_light: float = DEFAULT_LIGHT_LEVEL

	def __init__(
			self,
			# Interface 1
			surface=None, zoom_factors=None,
			# Interface 2
			zoomed_surfaces=None,
			# Optional
			lights=LIGHT_LEVELS,
			alpha_color=None
	):
		"""
		We provide two interfaces for initialization: users can provide a
		surface and a list of zoom factors, or they can provide a dict of
		already-zoomed surfaces with the zoom factors as keys.
		"""
		self._cache = {}
		self._alpha_cache = {}

		if lights is None:
			lights = [DEFAULT_LIGHT_LEVEL]
		else:
			self._using_light = True
			self._default_light = lights[-1]

		if surface is not None and zoom_factors is not None:
			self._init_from_surface(surface, zoom_factors, lights, alpha_color)
		elif zoomed_surfaces is not None:
			self._init_from_zoomed_surfaces(
				zoomed_surfaces, lights, alpha_color
			)
		else:
			raise ValueError("No surface - see Multisurface docs.")

	def _init_from_surface(self, surface, zoom_factors, lights, alpha_color):
		"""
		Generate the cache from a single surface.
		"""
		self._zooms = zoom_factors
		self._light_levels = lights
		for zoom in zoom_factors:
			zoomed = resize_surface(surface, zoom)
			self._cache[zoom] = {}
			mask = alpha_mask_from_surface(zoomed, alpha_color)
			self._alpha_cache[zoom] = mask
			for idx, light in enumerate(lights):
				self._cache[zoom][idx] = relight_surface(zoomed, light)

	def _init_from_zoomed_surfaces(self, zoomed_surfaces, lights, alpha_color):
		"""
		Generate the cache from a list of already-zoomed surfaces.
		"""
		self._zooms = list(zoomed_surfaces.keys())
		self._light_levels = lights
		for zoom, surface in zoomed_surfaces.items():
			self._cache[zoom] = {}
			mask = alpha_mask_from_surface(surface, alpha_color)
			self._alpha_cache[zoom] = mask
			for idx, light in enumerate(lights):
				self._cache[zoom][idx] = relight_surface(surface, light)

	def get(self, zoom=DEFAULT_ZOOM_FACTOR, light=None):
		"""
		Get the surface for the given zoom and light index.
		"""
		if not self._using_light or light is None:
			return self._cache[zoom][self._default_light]
		return self._cache[zoom][light]

	def get_by_light_level(self, zoom=DEFAULT_ZOOM_FACTOR, light_level=1.0):
		"""
		This is an alternate implementation of .get() where the light level
		value is known but the index key is not. Try to avoid this as it's
		much slower!
		"""
		closest_idx = min(
			range(len(self._light_levels)),
			key=lambda i: abs(self._light_levels[i] - light_level)
		)
		return self._cache[zoom][closest_idx]

	def get_alpha(self, zoom=DEFAULT_ZOOM_FACTOR):
		"""
		Get the alpha mask for the given zoom.
		"""
		return self._alpha_cache[zoom]
