from src.gameobject.gameobject import GameObject
from src.gameobject.actor import Actor
from src.world.world import World
from src.gui.gui import _GuiManager, init_gui_manager
from src.ctrl.ctrl import Control
from src.ctrl.clickmap import ClickMap
from src.render.render import Render

from src.mgmt.event_manager import EventManager
from src.mgmt.listener import Listener

class GameManager(Listener):
	"""
	Primarily responsible for managing game state and the passage of time.
	"""

	evt_mgr: EventManager
	gui_mgr: _GuiManager
	ctrl: Control
	renderer: Render
	clickmap: ClickMap

	game_objects: set[GameObject]
	utc: float
	world: World
	vp = None

	selected_actors: dict[int, Actor] = None

	def __init__(
			self,
			world: World,
			viewport,
			on_quit=None,
			evt_mgr=None,
			screen=None,
			no_gui=False,
	):
		self.screen = screen
		self.utc = 0.0
		self.game_objects = set()
		self.world = world
		self.world.game_mgr = self
		self.vp = viewport
		self.on_quit = on_quit
		self.selected_actors = {}
		self._init_managers(evt_mgr, no_gui)
		self._subscribe_to_events()

	def _init_managers(self, evt_mgr, no_gui):
		if evt_mgr is not None:
			self.evt_mgr = evt_mgr
		else:
			self.evt_mgr = EventManager()
		if not no_gui:
			self.gui_mgr = init_gui_manager(self)
		self.clickmap = ClickMap(self.vp.window_dims)
		self.ctrl = Control(self, on_quit=self.on_quit, clickmap=self.clickmap)

	def _subscribe_to_events(self):
		self.evt_mgr.sub("ShowSupereventEvent", self)

	def update(self, event):
		# TODO(jm) - this really should be in the gui manager instead of the
		# game manager.
		if event.event_type == 'ShowSupereventEvent':
			event.make_superevent()

	def tick(self, dt: float):
		"""
		Send an event to listeners about the passage of time.
		"""
		if dt <= 0:
			raise ValueError("Time travel not allowed")
		floor_new_utc = int(self.utc + dt)
		floor_old_utc = int(self.utc)
		if floor_new_utc != floor_old_utc:
			self.world.evolve(floor_new_utc - floor_old_utc)
		self.utc += dt
		self.evt_mgr.tick(dt, self.utc)
		for obj in self.game_objects:
			obj.tick(dt, self.utc)

	def prepare_render(self):
		"""
		Call this ONCE if this game manager is going to render things.
		"""
		self.renderer = Render(self.screen, self.world, self.vp, game_mgr=self)

	def render(self):
		self.clickmap.clear()
		self.renderer.render()

	def select_actor(self, player_id=1, actor=None):
		if not actor:
			raise ValueError("Expected actor!")
		self.selected_actors[player_id] = actor

	@property
	def player_character(self):
		"""
		Returns the currently selected player character. DEPRECATED - because
		of future multiplayer.
		"""
		pc = self.selected_actors.get(1)
		if not pc:
			raise ValueError("No player character - should never happen!")
		return pc

	def new_player_character(self, position, owner: int = 1):
		new_character = Actor(self, pos=position, owner=owner)
		new_character.motives.set_all(100)
		self.game_objects.add(new_character)
		if self.selected_actors.get(owner) is None:
			self.selected_actors[owner] = new_character
		return new_character

	def add_game_object(self, go: GameObject):
		"""
		Adds the given game object to the world.
		"""
		self.game_objects.add(go)
		go.on_init()

	def remove_game_object(self, go: GameObject):
		"""
		Removes the given game object from the world.
		"""
		self.game_objects.remove(go)
		go.on_remove()
