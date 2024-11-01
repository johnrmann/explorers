import pygame

from src.gen.terrain_generator import TerrainGenerator
from src.render.render_terrain import render_terrain

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
	cx = 0
	cy = 0

	while running:
		window.fill((255,255,255))
		camera_center = terrain.center()
		render_terrain(window, terrain, (cx,cy))
		pygame.display.flip()
		clock.tick(60)
	
	pygame.quit()

if __name__ == '__main__':
	main()

