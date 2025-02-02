"""
This package contains all sorts of color definitions.
"""

from src.world.biome import Biome

from src.render.utils import average_color, scale_color



DEFAULT_LUSH_COLOR = (0, 200, 0)

# Earth's barren color is sand.
EARTH_BARREN_COLOR = (210, 180, 140)

# Mars's barren color is iron oxide.
MARS_BARREN_COLOR = (200, 0, 0)
DEFAULT_BARREN_COLOR = MARS_BARREN_COLOR

# The Moon's barren color is dust.
MOON_BARREN_COLOR = (200, 200, 200)

# Dark orange for the Australian Outback.
OUTBACK_COLOR = (150, 75, 0)

class BiomeColorScheme:
	"""
	This class computes the colors for each biome.
	"""

	_lush_color: tuple[int, int, int]
	_barren_color: tuple[int, int, int]

	_color_map: dict[Biome, tuple[int, int, int]]

	def __init__(self, lush_color = None, barren_color = None):
		if lush_color is None:
			lush_color = DEFAULT_LUSH_COLOR
		if barren_color is None:
			barren_color = DEFAULT_BARREN_COLOR
		self._lush_color = lush_color
		self._barren_color = barren_color
		self._make_color_map()


	def _make_color_map(self):
		self._color_map = {
			Biome.BARREN: self._barren_color,
			Biome.BEACH: self._barren_color,

			Biome.TROPICAL: scale_color(self._lush_color, 0.75),
			Biome.DESERT: self._barren_color,

			Biome.LUSH: self._lush_color,
			Biome.SAVANNAH: average_color(self._lush_color, self._barren_color),

			Biome.SNOW: (255, 255, 255),
			Biome.TUNDRA: (50, 50, 50),

			Biome.OUTBACK: OUTBACK_COLOR,
		}


	def get_color(self, biome: Biome) -> tuple[int, int, int]:
		"""Get the color for a biome."""
		return self._color_map[biome]


	def items(self):
		"""Iterate over all biome-color pairs."""
		return self._color_map.items()
