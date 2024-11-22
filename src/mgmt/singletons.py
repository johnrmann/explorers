from src.render.viewport import Viewport
from src.mgmt.game_manager import GameManager
from src.world.world import World
from src.render.render import Render

_global_game_manager: GameManager = None

def init_game_manager(world: World, vp: Viewport, on_quit=None, screen=None):
	"""Initializes the game manager singleton."""
	global _global_game_manager
	if _global_game_manager is not None:
		raise ValueError("Game manager already initialized.")
	_global_game_manager = GameManager(world, vp, on_quit=on_quit, screen=screen)
	return _global_game_manager

def get_game_manager():
	"""Returns game manager singleton."""
	if not _global_game_manager:
		raise ValueError("Game manager not initialized.")
	return _global_game_manager
