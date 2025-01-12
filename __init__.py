import pygame

from argparse import ArgumentParser

from src.gen.gen import make_game, MakeTerrainOptions
from src.utility.calendar import utc_tuple_to_utc_float
from src.mgmt.constants import TARGET_FPS

flags = pygame.DOUBLEBUF

arg_parser = ArgumentParser()

# Arguments related to the game display.
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

# Arguments related to the game calendar.
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

# Arguments related to terrain generation.
arg_parser.add_argument(
	'--terrain-width',
	help='The width of the terrain.'
)
arg_parser.add_argument(
	'--terrain-ice-cap-size',
	help='The size of the ice caps on the terrain.'
)
arg_parser.add_argument(
	'--terrain-landmass-size',
	help='The size of the landmasses on the terrain.'
)
arg_parser.add_argument(
	'--terrain-ocean',
	help='Whether the terrain should have an ocean.'
)

# Arguments related to debugging.
arg_parser.add_argument(
	'--debug-print-atm',
	help='Print the atmospheric composition to the CLI once per frame.'
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

print_atm = False
if args.debug_print_atm:
	print_atm = True

epoch_tuple = (
	int(args.epoch_year or 2350),
	int(args.epoch_month or 1),
	int(args.epoch_day or 1)
)
epoch = utc_tuple_to_utc_float(epoch_tuple)

terrain_options = MakeTerrainOptions()
if args.terrain_width:
	terrain_options.width = int(args.terrain_width)
if args.terrain_ice_cap_size:
	terrain_options.ice_cap_size = int(args.terrain_ice_cap_size)
if args.terrain_landmass_size:
	terrain_options.landmass_cell_radius = int(args.terrain_landmass_size)
if args.terrain_ocean:
	terrain_options.ocean = True

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags)
pygame.display.set_caption("Explorers")

def main():
	running = True
	def on_quit():
		nonlocal running
		running = False

	game = make_game(
		terrain_options=terrain_options,
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
		if print_atm:
			print(game.world.atmosphere)

	pygame.quit()

if __name__ == '__main__':
	main()
