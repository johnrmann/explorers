import pygame

from src.gameobject.gameobject import GameObject
from src.render.utils import *
from src.rendermath.fit_rect import fit_img_rect_on_tile_base
from src.rendermath.multicell import multicell_polygon_on_global_screen

TOP_COLOR = (0, 0, 200)
LEFT_COLOR = (0, 0, 100)
RIGHT_COLOR = (0, 0, 50)

def render_gameobject(
	window=None,
	clickmap=None,
	vp: Viewport=None,
	go: GameObject=None,
	height = 0,
	image_map = None,
	light = None
):
	# Easy out if the gameobject is hidden
	if go.hidden:
		return

	# A "cell polygon" is the position of the tile if there was no terrain.
	multicell_polygon_global = multicell_polygon_on_global_screen(
		go.draw_bounds, vp.camera_orientation, vp.tile_dimensions
	)
	multicell_polygon = [
		vp.global_screen_position_to_screen_position(p)
		for p in multicell_polygon_global
	]
	base_polygon = height_offset_tile(multicell_polygon, height / 8, vp)

	if go.image_path() in image_map:
		img = image_map[go.image_path()].get(light=light)
		alpha = image_map[go.image_path()].get_alpha()
		origin, img_dims = fit_img_rect_on_tile_base(img.get_size(), base_polygon)
		window.blit(
			pygame.transform.scale(img, img_dims),
			pygame.Rect(origin, img_dims),
		)
		clickmap.mark_game_object(
			go, origin, pygame.transform.scale(alpha, img_dims)
		)
	else:
		top = height_offset_tile(base_polygon, 1, vp)
		top_poly, left, right = box_between_tiles(top, base_polygon)
		pygame.draw.polygon(window, TOP_COLOR, top_poly)
		pygame.draw.polygon(window, LEFT_COLOR, left)
		pygame.draw.polygon(window, RIGHT_COLOR, right)
