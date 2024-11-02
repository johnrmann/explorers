import pygame

from src.gameobject.gameobject import GameObject
from src.render.utils import *
from src.render.space import tile_to_screen_coords

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
    x,y = tile_to_screen_coords(go.pos, vp)
    bottom = height_offset_tile(tile_polygon(x, y, vp), height / 8, vp)
    if go.image_path() in image_map:
        img = image_map[go.image_path()]
        draw_rect = stand_rect_on_tile(img.get_rect(), bottom)
        window.blit(img, draw_rect)
    else:
        top = height_offset_tile(bottom, 1, vp)
        top_poly, left, right = box_between_tiles(top, bottom)
        pygame.draw.polygon(window, TOP_COLOR, top_poly)
        pygame.draw.polygon(window, LEFT_COLOR, left)
        pygame.draw.polygon(window, RIGHT_COLOR, right)
