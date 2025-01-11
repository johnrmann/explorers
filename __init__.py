import pygame

from argparse import ArgumentParser

from src.gen.gen import make_game
from src.utility.calendar import utc_tuple_to_utc_float
from src.mgmt.constants import TARGET_FPS
from src.gui.mission_clock import MissionClock
from src.gui.fps import FpsCounter
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
arg_parser.add_argument(
	'--epoch-year',
	help='What year to start the game calendar at.'
)
arg_parser.add_argument(
	'--epoch-month',
	help='What month to start the game calendar at.'
)
arg_parser.add_argument(
	'--epoch-day',
	help='What day to start the game calendar at.'
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

epoch_tuple = (
	int(args.epoch_year or 2350),
	int(args.epoch_month or 1),
	int(args.epoch_day or 1)
)
epoch = utc_tuple_to_utc_float(epoch_tuple)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags)
pygame.display.set_caption("Explorers")

def main():
	running = True
	def on_quit():
		nonlocal running
		running = False

	game = make_game(
		on_quit=on_quit,
		screen=window,
		window_dimensions=(WINDOW_WIDTH, WINDOW_HEIGHT),
		epoch=epoch
	)
	clock = pygame.time.Clock()

	while running:
		dt = clock.tick(TARGET_FPS) / 1000
		game.ctrl.interpret_pygame_input()
		game.render()
		game.gui_mgr.update(dt)
		game.gui_mgr.draw(window)
		pygame.display.flip()
		game.tick(dt)

	pygame.quit()

if __name__ == '__main__':
	main()
