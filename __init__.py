import pygame

from src.gen.terrain_generator import TerrainGenerator
from src.world.world import World
from src.render.render import Render
from src.render.viewport import Viewport, pygame_key_to_camdir, pygame_key_to_delta_zoom, pygame_key_to_delta_camera_rotate
from src.render.space import screen_to_tile_coords
from src.math.vector2 import Vector2
from src.gameobject.lander import Lander
from src.mgmt import init_game_manager, get_game_manager, get_event_manager

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
	game_mgr = init_game_manager(world)
	game_mgr.new_player_character(world.terrain.center)
	make_lander(world)
	return game_mgr

def main():
	game = make_game()
	world = game.world

	clock = pygame.time.Clock()
	running = True
	vp = Viewport((WINDOW_WIDTH, WINDOW_HEIGHT), world.terrain)
	render = Render(window, world, vp)

	while running:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				d_camdir = pygame_key_to_camdir(event.key)
				d_zoom = pygame_key_to_delta_zoom(event.key)
				d_rotate = pygame_key_to_delta_camera_rotate(event.key)
				vp.move_camera(d_camdir)
				vp.change_zoom(d_zoom)
				vp.rotate_camera(d_rotate)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				click_x, click_y = pygame.mouse.get_pos()
				click_tile = screen_to_tile_coords((click_x, click_y), vp)
				click_tile = (
					int(click_tile[0]), int(click_tile[1])
				)
				game.player_character.set_destination(world, click_tile)
		render.render()
		render.render_terrain.highlight_tile_at_screen_pos(pygame.mouse.get_pos())
		pygame.display.flip()
		clock.tick()
		game.tick(1)
	
	pygame.quit()

if __name__ == '__main__':
	main()

