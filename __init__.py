import pygame

from src.gen.terrain_generator import TerrainGenerator
from src.world.world import World
from src.render.render import Render
from src.render.viewport import Viewport, pygame_key_to_camdir, pygame_key_to_delta_zoom, pygame_key_to_delta_camera_rotate
from src.render.space import screen_to_tile_coords

pygame.init()

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Explorers")

def make_terrain():
	tg = TerrainGenerator()
	terrain = tg.make()
	return terrain

def make_world():
	"""
	Generate some terrain, put the player character and lander in it.
	"""
	terrain = make_terrain()
	world = World(terrain)
	world.new_player_character(terrain.center)
	return world

def main():
	world = make_world()

	clock = pygame.time.Clock()
	running = True
	vp = Viewport((WINDOW_WIDTH, WINDOW_HEIGHT), world.terrain)
	render = Render(window, world, vp)

	while running:
		world.player_character.act()
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
				world.player_character.set_destination(world, click_tile)
		render.render()
		render.render_terrain.highlight_tile_at_screen_pos(pygame.mouse.get_pos())
		pygame.display.flip()
		clock.tick()
		world.utc = pygame.time.get_ticks() / 1000
	
	pygame.quit()

if __name__ == '__main__':
	main()

