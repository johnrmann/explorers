from src.gameobject.gameobject import GameObject
from src.gameobject.actor import Actor
from src.world.world import World
from src.gui.gui import _GuiManager, init_gui_manager
from src.ctrl.ctrl import Control

from src.mgmt.event_manager import EventManager
from src.mgmt.constants import TICKS_PER_SECOND

class GameManager:
	"""
	Primarily responsible for managing game state and the passage of time.
	"""

	evt_mgr: EventManager
	gui_mgr: _GuiManager
	ctrl: Control

	game_objects: list[GameObject]
	ticks: int
	world: World
	vp = None

	def __init__(self, world: World, viewport, on_quit=None, evt_mgr=None):
		self.ticks = 0
		self.game_objects = []
		self.world = world
		self.vp = viewport
		self.on_quit = on_quit
		self._init_managers(evt_mgr)

	def _init_managers(self, evt_mgr):
		if evt_mgr is not None:
			self.evt_mgr = evt_mgr
		else:
			self.evt_mgr = EventManager()
		self.gui_mgr = init_gui_manager()
		self.ctrl = Control(self, on_quit=self.on_quit)

	@property
	def utc(self) -> float:
		"""
		Seconds since game start.
		"""
		return self.ticks / TICKS_PER_SECOND

	def tick(self, n_ticks=1):
		"""
		Send an event to listeners about the passage of time.
		"""
		if n_ticks <= 0:
			raise ValueError("Time travel not allowed")
		self.ticks += n_ticks
		dt = n_ticks / TICKS_PER_SECOND
		self.evt_mgr.tick(dt, self.utc)
		for obj in self.game_objects:
			obj.tick(dt, self.utc)

	@property
	def player_character(self):
		"""
		Returns the currently selected player character.
		"""
		for go in self.game_objects:
			if isinstance(go, Actor):
				if go._is_played: # TODO(jm) - evil private access
					return go
		raise ValueError("No player character - should never happen!")
	
	def new_player_character(self, position):
		self.game_objects.append(Actor(self, pos=position))

	def add_game_object(self, go: GameObject):
		self.game_objects.append(go)
