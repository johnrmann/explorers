from dataclasses import dataclass
import random

from src.math.vector2 import Vector2
from src.mgmt.singletons import init_game_manager
from src.gameobject.lander import Lander
from src.gameobject.plant_flag import PlantFlag
from src.world.world import World
from src.world.astronomy import Astronomy

from src.render.viewport import Viewport

from src.gen.atmosphere_generator import (
	AtmosphereType,
	generate_atmosphere_composition
)
from src.gen.terrain_generator import TerrainGenerator

@dataclass
class MakeTerrainOptions:
	"""Options for making terrain."""
	width: int = 512
	height: int = 256
	ice_cap_size: int = 0
	landmass_cell_radius: int = 5
	ocean: bool = False


def make_terrain(options: MakeTerrainOptions = None):
	"""Create a terrain."""
	if options is None:
		options = MakeTerrainOptions()
	tgen = TerrainGenerator(width=options.width, height=options.height)
	if options.ice_cap_size:
		tgen.set_ice_caps(cells_tall=options.ice_cap_size)
	tgen.set_landmasses(cell_radius=options.landmass_cell_radius)
	if options.ocean:
		tgen.set_ocean()
	return tgen.make()


def make_world(
		terrain_options: MakeTerrainOptions = None,
		atmosphere_type = AtmosphereType.MARS_LIKE,
):
	terrain = make_terrain(options=terrain_options)
	world = World(
		terrain,
		astronomy=Astronomy(),
		atmosphere_composition=generate_atmosphere_composition(atmosphere_type)
	)
	return world


def make_plant_flag(game_mgr, lz_position=None, player_id=1):
	"""Create the flag the player plants."""
	flag_pos = lz_position + Vector2(0, 10)
	flag = PlantFlag(pos=flag_pos, is_first=True)
	flag.owner = player_id
	game_mgr.add_game_object(flag)


def make_landing_zone(
		game_mgr = None,
		player_id = 1,
		position = None,
):
	"""Create a landing zone."""
	if game_mgr is None:
		raise ValueError("game_mgr must be provided.")
	if position is None:
		raise ValueError("position must be provided.")
	world = game_mgr.world
	lander_position = position + Vector2(-5, -12)
	lander = Lander(game_mgr, pos=lander_position)
	lander.owner = player_id
	game_mgr.add_game_object(lander)
	game_mgr.new_player_character(world.terrain.center)
	game_mgr.new_player_character(world.terrain.center + Vector2(2, 0))
	game_mgr.new_player_character(world.terrain.center + Vector2(-2, 0))
	make_plant_flag(game_mgr, lz_position=position, player_id=player_id)
	return lander


def make_game(
		terrain_options: MakeTerrainOptions = None,
		num_players = 1,
		window_dimensions = None,
		on_quit = None,
		screen = None,
		epoch = None,
):
	"""Create the game."""
	if window_dimensions is None:
		raise ValueError("window_dimensions must be provided.")
	world = make_world(terrain_options=terrain_options)
	vp = Viewport(window_dimensions, world.terrain)
	game_mgr = init_game_manager(
		world,
		vp,
		on_quit=on_quit,
		screen=screen,
		epoch=epoch,
		no_gui=False
	)
	vp.game_mgr = game_mgr
	positions = [world.terrain.center]
	if num_players > 1:
		positions = []
		for _ in range(num_players):
			rand_x = int(random.random() * world.terrain.width)
			rand_y = int(random.random() * world.terrain.height)
			positions.append((rand_x, rand_y))
	for player_id, position in zip(range(1, num_players + 1), positions):
		make_landing_zone(
			game_mgr=game_mgr,
			player_id=player_id,
			position=position
		)
	return game_mgr
