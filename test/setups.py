from unittest.mock import MagicMock

from src.mgmt.event_manager import EventManager
from src.mgmt.game_manager import GameManager

from src.world.world import World
from src.world.terrain import Terrain

from src.render.viewport import Viewport

def make_flat_terrain_map():
	return [[1] * 16 for _ in range(16)]

def make_flat_terrain():
	return Terrain(make_flat_terrain_map())

def make_flat_world():
	return World(terrain=make_flat_terrain())

def make_viewport(terrain):
	return Viewport((800, 600), terrain)

def make_basic_game_manager():
	world = make_flat_world()
	viewport = make_viewport(world.terrain)
	return GameManager(world, viewport, evt_mgr=EventManager(), no_gui=True)
