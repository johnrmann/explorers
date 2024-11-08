from src.mgmt.event_manager import EventManager
from src.mgmt.game_manager import GameManager
from src.world.world import World

_global_event_manager: EventManager = EventManager()
_global_game_manager: GameManager = None

def get_event_manager():
	"""Returns event manager singleton."""
	return _global_event_manager

def init_game_manager(world: World):
	"""Initializes the game manager singleton."""
	global _global_game_manager
	if _global_game_manager is not None:
		raise ValueError("Game manager already initialized.")
	_global_game_manager = GameManager(world)
	return _global_game_manager

def get_game_manager():
	"""Returns game manager singleton."""
	if not _global_game_manager:
		raise ValueError("Game manager not initialized.")
	return _global_game_manager
