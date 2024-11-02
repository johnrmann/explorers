import pygame

from src.gameobject.gameobject import GameObject
from src.render.utils import *

TOP_COLOR = (0, 0, 200)
LEFT_COLOR = (0, 0, 100)
RIGHT_COLOR = (0, 0, 50)

def render_gameobject(window, vp: Viewport, go: GameObject, h_offset = 0):
    x,y = tile_coords_to_screen_coords(go.pos, vp)
    bottom = height_offset_tile(tile_polygon(x, y, vp), h_offset, vp)
    top = height_offset_tile(bottom, 8, vp)
    top_poly, left, right = box_between_tiles(top, bottom)
    pygame.draw.polygon(window, TOP_COLOR, top_poly)
    pygame.draw.polygon(window, LEFT_COLOR, left)
    pygame.draw.polygon(window, RIGHT_COLOR, right)
