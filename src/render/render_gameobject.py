import pygame

from src.gameobject.gameobject import GameObject
from src.render.utils import *
from src.tile.fit_rect import fit_img_rect_on_tile_base
from src.tile.tile import tile_polygon

TOP_COLOR = (0, 0, 200)
LEFT_COLOR = (0, 0, 100)
RIGHT_COLOR = (0, 0, 50)

def render_gameobject(
	window=None,
	vp: Viewport=None,
	go: GameObject=None,
	height = 0,
	image_map = {}
):
	# An "ideal tile" is the position of the tile if there was no terrain.
	go_size = max(go.size[0], go.size[1])
	go_center = go.draw_position
	screen_pos = vp.tile_to_screen_coords(go_center)
	ideal_tile = tile_polygon(screen_pos, vp.tile_dimensions, go_size)

	# Now, move up by height to find the terrain start point.
	terrain = height_offset_tile(ideal_tile, height / 8, vp)
	if go.image_path() in image_map:
		img = image_map[go.image_path()]
		origin, img_dims = fit_img_rect_on_tile_base(img.get_size(), terrain)
		window.blit(
			pygame.transform.scale(img, img_dims),
			pygame.Rect(origin, img_dims),
		)
	else:
		top = height_offset_tile(terrain, 1, vp)
		top_poly, left, right = box_between_tiles(top, terrain)
		pygame.draw.polygon(window, TOP_COLOR, top_poly)
		pygame.draw.polygon(window, LEFT_COLOR, left)
		pygame.draw.polygon(window, RIGHT_COLOR, right)
