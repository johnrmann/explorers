import pygame

from argparse import ArgumentParser

from src.gen.terrain_generator import TerrainGenerator
from src.world.world import World
from src.render.render import Render
from src.math.vector2 import Vector2
from src.gameobject.lander import Lander
from src.gameobject.plant_flag import PlantFlag
from src.mgmt.singletons import init_game_manager, get_game_manager
from src.mgmt.constants import TARGET_FPS
from src.render.viewport import Viewport
from src.ctrl.ctrl import Control
from src.gui.anchor import Anchor
from src.gui.mission_clock import MissionClock
from src.gui.superevent import superevent_from_json
from src.gui.fps import FpsCounter
from src.gui.rangebar import Rangebar
from src.gui.actor_motives import ActorMotivesGui
from src.gui.playbar import Playbar
from src.gui.colony_name import ColonyName

flags = pygame.DOUBLEBUF

arg_parser = ArgumentParser()
arg_parser.add_argument(
	'--fullscreen',
	help='Run the game in fullscreen mode.',
)
arg_parser.add_argument(
	'-sw','--screen-width',
	help='The width of the game window.',
)
arg_parser.add_argument(
	'-sh', '--screen-height',
	help='The height of the game window.',
)

args = arg_parser.parse_args()

WINDOW_WIDTH = None
WINDOW_HEIGHT = None

pygame.init()

if args.fullscreen:
	flags = flags | pygame.FULLSCREEN
	if not args.screen_width and not args.screen_height:
		info = pygame.display.Info()
		WINDOW_WIDTH = info.current_w
		WINDOW_HEIGHT = info.current_h
	else:
		WINDOW_WIDTH = int(args.screen_width)
		WINDOW_HEIGHT = int(args.screen_height)
else:
	if args.screen_width and args.screen_height:
		WINDOW_WIDTH = int(args.screen_width)
		WINDOW_HEIGHT = int(args.screen_height)
	else:
		WINDOW_WIDTH = 1440
		WINDOW_HEIGHT = 900

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags)
pygame.display.set_caption("Explorers")

def make_terrain():
	"""Create the world's terrain."""
	tg = TerrainGenerator()
	terrain = tg.make()
	return terrain

def make_world():
	"""Create the game world."""
	terrain = make_terrain()
	world = World(terrain)
	return world

def make_lander(world: World):
	"""Create the lander the player character arrives in."""
	lander_pos = world.terrain.center + Vector2(-5, -12)
	lander = Lander(pos=lander_pos)
	lander.owner = 1
	get_game_manager().add_game_object(lander)

def make_plant_flag(world: World):
	"""Create the flag the player plants."""
	flag_pos = world.terrain.center + Vector2(0, 10)
	flag = PlantFlag(pos=flag_pos, is_first=True)
	flag.owner = 1
	get_game_manager().add_game_object(flag)

def make_game(on_quit):
	"""Initialize the game manager."""
	world = make_world()
	vp = Viewport((WINDOW_WIDTH, WINDOW_HEIGHT), world.terrain)
	game_mgr = init_game_manager(world, vp, on_quit=on_quit, screen=window)
	vp.game_mgr = game_mgr
	game_mgr.new_player_character(world.terrain.center)
	game_mgr.new_player_character(world.terrain.center + Vector2(2, 0))
	game_mgr.new_player_character(world.terrain.center + Vector2(-2, 0))
	make_lander(world)
	make_plant_flag(world)
	return game_mgr

def main():
	running = True
	def on_quit():
		nonlocal running
		running = False

	game = make_game(on_quit)
	clock = pygame.time.Clock()
	game.prepare_render()

	mission_clock = MissionClock()
	fps = FpsCounter()
	playbar = Playbar(
		game,
	)
	cname = ColonyName()

	while running:
		dt = clock.tick(TARGET_FPS) / 1000
		game.ctrl.interpret_pygame_input()
		game.render()
		game.renderer.render_terrain.highlight_tile_at_screen_pos(
			pygame.mouse.get_pos()
		)
		game.gui_mgr.update(dt)
		game.gui_mgr.draw(window)
		pygame.display.flip()
		game.tick(dt)

	pygame.quit()

if __name__ == '__main__':
	main()
