import pygame

from src.gen.terrain_generator import TerrainGenerator
from src.world.world import World
from src.render.render import Render
from src.math.vector2 import Vector2
from src.gameobject.lander import Lander
from src.mgmt.singletons import init_game_manager, get_game_manager, get_event_manager
from src.ctrl.ctrl import Control
from src.render.viewport import Viewport

pygame.init()

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

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

def make_game():
	"""Initialize the game manager."""
	world = make_world()
	vp = Viewport((WINDOW_WIDTH, WINDOW_HEIGHT), world.terrain)
	game_mgr = init_game_manager(world, vp)
	game_mgr.new_player_character(world.terrain.center)
	make_lander(world)
	return game_mgr

def main():
	game = make_game()
	ctrl = Control()
	world = game.world

	clock = pygame.time.Clock()
	running = True
	render = Render(window, world, game.vp)

	while running:
		ctrl.interpret_pygame_input()
		render.render()
		render.render_terrain.highlight_tile_at_screen_pos(pygame.mouse.get_pos())
		pygame.display.flip()
		clock.tick()
		game.tick(1)
	
	pygame.quit()

if __name__ == '__main__':
	main()

