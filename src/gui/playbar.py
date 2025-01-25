import pygame

from enum import Enum

from src.gameobject.flora import DEBUG_TREE

from src.gui.gui import GuiElement
from src.gui.primitives import Panel
from src.gui.anchor import Anchor
from src.gui.minimap import MiniMap
from src.gui.actor_motives import ActorMotivesGui
from src.gui.line_graph import LineGraph
from src.gui.scanline import Scanline
from src.gui.catalog import Catalog
from src.gui.button_grid import (
	ImageButtonGrid,
	ImageButtonGridItem,
	ButtonGridSpacing
)

class PlaybarMode(Enum):
	"""
	Represents the different modes that the playbar can be in.
	"""
	CHARACTER = 0
	PLANET = 1
	BUILD = 2
	OPTIONS = 3

GRID_ITEMS = [
	ImageButtonGridItem(
		0,
		"assets/img/icon/astronaut.png",
		payload=PlaybarMode.CHARACTER
	),
	ImageButtonGridItem(
		1,
		"assets/img/icon/planet.png",
		payload=PlaybarMode.PLANET
	),
	ImageButtonGridItem(
		2,
		"assets/img/icon/tool.png",
		payload=PlaybarMode.BUILD
	),
	ImageButtonGridItem(
		3,
		"assets/img/icon/setting.png",
		payload=PlaybarMode.OPTIONS
	),
]

class Playbar(GuiElement):
	"""
	A bar at the bottom of the screen that contains the controls for the
	game.
	"""

	_mode: PlaybarMode

	_mode_to_elements: dict[PlaybarMode, set[GuiElement]] = None

	_panel: Panel = None
	_icons: ImageButtonGrid = None

	_change_mode_callback = None
	_selected_build_object_callback = None
	_deselected_build_object_callback = None

	def __init__(
			self,
			game,
			change_mode_callback=None,
			selected_build_object_callback=None,
			deselected_build_object_callback=None,
			**kwargs
	):
		self.game = game
		self.world = game.world
		self.viewport = game.renderer.vp
		self._change_mode_callback = change_mode_callback
		self._selected_build_object_callback = selected_build_object_callback
		self._deselected_build_object_callback = deselected_build_object_callback
		super().__init__(
			origin=(0, 0),
			dimensions=(self.viewport.window_dims[0], 200),
			anchor=Anchor.BOTTOM_LEFT,
			**kwargs
		)
		self._icons = ImageButtonGrid(
			items=GRID_ITEMS,
			parent=self,
			origin=(0, 0),
			spacing=ButtonGridSpacing(
				button_dimensions=(50, 50),
				button_margin=0,
			),
			dimensions=(50, 200),
			callback=lambda mode: setattr(self, "mode", mode),
			**kwargs,
		)
		self._panel = Panel(
			origin=(50, 0),
			dimensions=(self.viewport.window_dims[0] - 50, 200),
			parent=self,
		)
		self._mode_to_elements = {
			PlaybarMode.CHARACTER: self._make_character_mode(),
			PlaybarMode.PLANET: self._make_planet_mode(),
			PlaybarMode.BUILD: self._make_build_mode(),
			PlaybarMode.OPTIONS: self._make_options_mode(),
		}
		self._hide_all()
		self._panel.hidden = False
		self._mode = PlaybarMode.CHARACTER
		self._unhide_current_mode()


	def _hide_all(self):
		for elem_set in self._mode_to_elements.values():
			for elem in elem_set:
				elem.hidden = True


	def _unhide_current_mode(self):
		for elem in self._mode_to_elements[self._mode]:
			elem.hidden = False


	@property
	def mode(self):
		return self._mode


	@mode.setter
	def mode(self, new_mode):
		if self._mode == new_mode:
			return
		for elem in self._mode_to_elements[self._mode]:
			elem.hidden = True
		self._mode = new_mode
		self._unhide_current_mode()
		if self._change_mode_callback:
			self._change_mode_callback(new_mode)


	def _make_character_mode(self):
		"""
		Initialize actor motives and minimap.
		"""
		motives = ActorMotivesGui(
			get_motives=lambda: self.game.player_character.motives,
			origin=(0, 0),
			anchor=Anchor.BOTTOM_LEFT,
			parent=self._panel,
		)
		minimap = MiniMap(
			origin=(0, 0),
			dimensions=(400, 200),
			anchor=Anchor.BOTTOM_RIGHT,
			world=self.world,
			viewport=self.viewport,
			parent=self._panel,
		)
		return set([motives, minimap])


	def _make_planet_mode(self):
		scanline = Scanline(
			origin=(0, 0),
			parent=self._panel,
			start_color=(0, 255, 0, 0),
			end_color=(0, 255, 0, 100),
		)
		line_graph = LineGraph(
			origin=(0, 0),
			dimensions=(300, 200),
			parent=scanline,
			series=[list([x**2 for x in range(10)])],
			colors=[(255, 0, 0)],
		)
		return set([scanline])


	def _make_build_mode(self):
		catalog = Catalog(
			origin=(0, 0),
			parent=self._panel,
			dimensions=(500, 200),
			on_select=self._selected_build_object_callback,
			on_deselect=self._deselected_build_object_callback,
			prototypes=[DEBUG_TREE],
		)
		return set([catalog])


	def _make_options_mode(self):
		return set()


	def my_process_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_F1:
				self.mode = PlaybarMode.CHARACTER
				return True
			elif event.key == pygame.K_F2:
				self.mode = PlaybarMode.PLANET
				return True
			elif event.key == pygame.K_F3:
				self.mode = PlaybarMode.BUILD
				return True
			elif event.key == pygame.K_F4:
				self.mode = PlaybarMode.OPTIONS
				return True
		return False
