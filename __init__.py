import pygame

from src.gen.terrain_generator import TerrainGenerator
from src.render.render_terrain import RenderTerrain
from src.render.viewport import Viewport, pygame_key_to_camdir, pygame_key_to_delta_zoom

pygame.init()

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 512

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Explorers")

def make_terrain():
	tg = TerrainGenerator()
	terrain = tg.make()
	return terrain

def main():
	terrain = make_terrain()

	clock = pygame.time.Clock()
	running = True
	vp = Viewport((WINDOW_WIDTH, WINDOW_HEIGHT), terrain)
	rt = RenderTerrain(window, terrain, vp)

	while running:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				d_camdir = pygame_key_to_camdir(event.key)
				d_zoom = pygame_key_to_delta_zoom(event.key)
				vp.move_camera(d_camdir)
				vp.change_zoom(d_zoom)
		rt.render()
		pygame.display.flip()
		clock.tick(60)
	
	pygame.quit()

if __name__ == '__main__':
	main()

