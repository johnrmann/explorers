import pygame

pygame.init()

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 512

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Explorers")

def main():
	clock = pygame.time.Clock()
	running = True

	while running:
		window.fill((0,0,0))
		clock.tick(60)
	
	pygame.quit()

if __name__ == '__main__':
	main()

