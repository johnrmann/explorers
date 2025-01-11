import random

from src.gameobject.gameobject import GameObject
from src.gameobject.actor import Actor
from src.gameobject.structure import Structure
from src.gui.superevent import ShowSupereventEvent
from src.world.world import World
from src.colony.colony import Colony
from src.ctrl.ctrl import Control
from src.ctrl.clickmap import ClickMap
from src.render.render import Render
from src.utility.calendar import next_christmas, utc_tuple_to_utc_float

from src.gui.gui import _GuiManager, init_gui_manager
from src.gui.mission_clock import MissionClock
from src.gui.fps import FpsCounter
from src.gui.playbar import Playbar
from src.gui.colony_name import ColonyName

from src.mgmt.event_manager import EventManager
from src.mgmt.listener import Listener

def christmas_event(score):
	return random.choice([
		"first_christmas-good",
		"first_christmas-bad",
	])

def y3k_event(score):
	return random.choice([
		"y3k-good",
		"y3k-bad",
	])

class CoreGuiElements:
	"""
	Creates the basic gui elements.
	"""

	def __init__(self, game):
		self.mission_clock = MissionClock()
		self.fps = FpsCounter()
		self.playbar = Playbar(game)
		self.colony_name = ColonyName()

class GameManager(Listener):
	"""
	Primarily responsible for managing game state and the passage of time.
	"""

	evt_mgr: EventManager
	gui_mgr: _GuiManager
	core_gui_elements: CoreGuiElements
	ctrl: Control
	renderer: Render = None
	clickmap: ClickMap

	# UTC is used to keep track of the current time in the game world. Epoch
	# is used as a mostly cosmetic offset for the game clock, although it does
	# have some minor gameplay effects (holidays).
	utc: float
	epoch: float

	# Whether time is paused or not.
	paused: bool = False

	game_objects: set[GameObject]
	colonies: set[Colony]
	world: World
	vp = None

	selected_actors: dict[int, Actor] = None

	is_single_player = True

	def __init__(
			self,
			world: World,
			viewport,
			epoch=0,
			on_quit=None,
			evt_mgr=None,
			screen=None,
			no_gui=True,
	):
		self.screen = screen
		self.utc = 0.0
		self.epoch = epoch
		self.game_objects = set()
		self.colonies = []
		self.world = world
		self.world.game_mgr = self
		self.vp = viewport
		self.on_quit = on_quit
		self.selected_actors = {}
		if screen:
			self.prepare_render()
		self._init_managers(evt_mgr, no_gui)
		self._subscribe_to_events()
		self._make_holiday_queue()
		if not no_gui:
			self.core_gui_elements = CoreGuiElements(self)

	def _init_managers(self, evt_mgr, no_gui):
		if evt_mgr is not None:
			self.evt_mgr = evt_mgr
		else:
			self.evt_mgr = EventManager()
		if not no_gui:
			self.gui_mgr = init_gui_manager(self)
		self.clickmap = ClickMap(self.vp.window_dims)
		screen_to_tile = None
		if self.renderer:
			screen_to_tile = self.renderer.render_terrain.tile_at_screen_pos
		self.ctrl = Control(
			self,
			on_quit=self.on_quit,
			clickmap=self.clickmap,
			screen_to_tile=screen_to_tile
		)

	def _subscribe_to_events(self):
		self.evt_mgr.sub("ShowSupereventEvent", self)
		self.evt_mgr.sub("FlagPlantedEvent", self)

	def _make_holiday_queue(self):
		"""
		Holidays are used as "gut checks" - they show the player flavor text
		about how they're doing. They're implemented as a float -> function
		dictionary, where the float is the UTC time at which the holiday
		occurs, and the function takes in a game score and outputs which
		event ID to signal.
		"""
		christmas = next_christmas(0, epoch=self.epoch)
		y3k = utc_tuple_to_utc_float((3000, 1, 1), epoch=self.epoch)
		self._holiday_queue = {
			christmas: christmas_event,
			y3k: y3k_event,
		}

	def update(self, event):
		# TODO(jm) - this really should be in the gui manager instead of the
		# game manager.
		if event.event_type == 'ShowSupereventEvent':
			event.make_superevent()
			self.paused = True
		# TODO(jm) - move this to world?
		if event.event_type == 'FlagPlantedEvent':
			self.new_colony(
				position=event.position,
				owner=event.owner,
				is_first=event.is_first
			)

	def tick(self, dt: float):
		"""
		Send an event to listeners about the passage of time.
		"""
		if dt <= 0:
			raise ValueError("Time travel not allowed")
		self.ctrl.tick(dt)
		if self.paused:
			return
		floor_new_utc = int(self.utc + dt)
		floor_old_utc = int(self.utc)
		if floor_new_utc != floor_old_utc:
			self.world.evolve(floor_new_utc - floor_old_utc)
			self._check_for_holidays(int(self.utc + dt))
		self.utc += dt
		self.evt_mgr.tick(dt, self.utc)
		for obj in self.game_objects:
			obj.tick(dt, self.utc)

	def _check_for_holidays(self, new_utc):
		if new_utc in self._holiday_queue:
			holiday = self._holiday_queue[new_utc]
			score = 0
			self.evt_mgr.pub(
				ShowSupereventEvent(
					json_file="assets/json/events/holiday.json",
					json_id=holiday(score)
				)
			)

	def prepare_render(self):
		"""
		Call this ONCE if this game manager is going to render things.
		"""
		self.renderer = Render(self.screen, self.world, self.vp, game_mgr=self)

	def render(self):
		self.clickmap.clear()
		self.renderer.render()
		self.renderer.highlight_tile(self.ctrl.cell_under_mouse)

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

	def new_colony(self, position=None, owner=None, is_first=False):
		"""
		Establish a new colony at the given position for the given owner, and
		add any player-owned structures already in it to the colony.
		"""
		colony = Colony(
			owner=owner,
			position=position,
			is_first=is_first,
			game_mgr=self
		)
		self.colonies.append(colony)
		for gobj in self.game_objects:
			if (
				gobj.owner == owner and
				isinstance(gobj, Structure) and
				colony.is_structure_inside(gobj)
			):
				colony.add_structure(gobj)
		return colony

	def is_cell_occupied(self, position):
		"""
		Returns True if the given position is occupied by a game object.
		"""
		for go in self.game_objects:
			if go.occupies_cell(position):
				return True
		return False
