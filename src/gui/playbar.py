import pygame

from enum import Enum

from src.gui.gui import GuiElement
from src.gui.primitives import Panel
from src.gui.anchor import Anchor
from src.gui.minimap import MiniMap
from src.gui.actor_motives import ActorMotivesGui
from src.gui.line_graph import LineGraph
from src.gui.scanline import Scanline

class PlaybarMode(Enum):
	"""
	Represents the different modes that the playbar can be in.
	"""
	CHARACTER = 0
	PLANET = 1
	BUILD = 2
	OPTIONS = 3

class Playbar(GuiElement):
	"""
	A bar at the bottom of the screen that contains the controls for the
	game.
	"""

	_mode: PlaybarMode

	_mode_to_elements = None
	_panel = None

	_change_mode_callback = None

	def __init__(self, game, change_mode_callback=None, **kwargs):
		self.game = game
		self.world = game.world
		self.viewport = game.renderer.vp
		self._change_mode_callback = change_mode_callback
		super().__init__(
			origin=(0, 0),
			dimensions=(self.viewport.window_dims[0], 200),
			anchor=Anchor.BOTTOM_LEFT,
			**kwargs
		)
		self._panel = Panel(
			origin=(0, 0),
			dimensions=(self.viewport.window_dims[0], 200),
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
		for elem in self.elements:
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
			parent=self,
		)
		minimap = MiniMap(
			origin=(0, 0),
			dimensions=(400, 200),
			anchor=Anchor.BOTTOM_RIGHT,
			world=self.world,
			viewport=self.viewport,
			parent=self,
		)
		return set([motives, minimap])

	def _make_planet_mode(self):
		scanline = Scanline(
			origin=(0, 0),
			parent=self,
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
		return set()

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
