import pygame

from src.gen.terrain_generator import TerrainGenerator
from src.world.world import World
from src.render.render import Render
from src.math.vector2 import Vector2
from src.gameobject.lander import Lander
from src.mgmt.singletons import init_game_manager, get_game_manager
from src.mgmt.constants import TICKS_PER_SECOND
from src.render.viewport import Viewport
from src.ctrl.ctrl import Control
from src.gui.mission_clock import MissionClock
from src.gui.superevent import superevent_from_json
from src.gui.fps import FpsCounter
from src.gui.rangebar import Rangebar
from src.gui.menu import VerticalMenu

pygame.init()

WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 900

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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
	lander_pos = world.terrain.center + Vector2(0, -10)
	lander = Lander(pos=lander_pos)
	get_game_manager().add_game_object(lander)

def make_game(on_quit):
	"""Initialize the game manager."""
	world = make_world()
	vp = Viewport((WINDOW_WIDTH, WINDOW_HEIGHT), world.terrain)
	game_mgr = init_game_manager(world, vp, on_quit=on_quit)
	vp.game_mgr = game_mgr
	game_mgr.new_player_character(world.terrain.center)
	make_lander(world)
	return game_mgr

def main():
	running = True
	def on_quit():
		nonlocal running
		running = False

	game = make_game(on_quit)
	world = game.world

	clock = pygame.time.Clock()
	render = Render(window, world, game.vp)

	mission_clock = MissionClock()
	fps = FpsCounter()
	# vmenu = VerticalMenu(
	# 	origin=(200,200),
	# 	actions=[
	# 		"Alpha",
	# 		"Bravo",
	# 		"Charlie"
	# 	]
	# )
	# health = Rangebar(
	# 	rect=((200,200), (200,30)),
	# 	layers=[
	# 		((250, 0, 0), 0, 0),
	# 		((250, 250, 0), 0, 100),
	# 		((0, 250, 0), 0, 100)
	# 	],
	# 	values=[66,33]
	# )
	# se = superevent_from_json(
	# 	"assets/json/events/landing.json",
	# 	"landing-neutral"
	# )

	while running:
		dt = clock.tick(TICKS_PER_SECOND) / 1000
		game.ctrl.interpret_pygame_input()
		render.render()
		render.render_terrain.highlight_tile_at_screen_pos(pygame.mouse.get_pos())
		game.gui_mgr.update(dt)
		game.gui_mgr.draw(window)
		pygame.display.flip()
		game.tick(1)

	pygame.quit()

if __name__ == '__main__':
	main()
