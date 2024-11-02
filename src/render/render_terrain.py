import pygame
import math

from ..world.terrain import Terrain
from src.render.viewport import Viewport
from src.render.utils import *

GROUND_COLOR = (200, 0, 0)
WALL_COLOR_1 = (100, 0, 0)
WALL_COLOR_2 = (50, 0, 0)

def polygons(vp, terrain, tile):
    x,y = tile
    h = terrain.map[y][x]
    tx_screen, ty_screen = tile_coords_to_screen_coords(tile, vp)
    bottom = tile_polygon(tx_screen, ty_screen, vp)
    top = height_offset_tile(bottom, h, vp)
    return box_between_tiles(top, bottom)

class RenderTerrain(object):
    def __init__(self, window, terrain: Terrain, vp: Viewport):
        self.terrain = terrain
        self.window = window
        self.vp = vp

    def render_tile(self, p):
        top, left_wall, right_wall = polygons(self.vp, self.terrain, p)
        if top:
            pygame.draw.polygon(self.window, GROUND_COLOR, top)
        if left_wall:
            pygame.draw.polygon(self.window, WALL_COLOR_1, left_wall)
        if right_wall:
            pygame.draw.polygon(self.window, WALL_COLOR_2, right_wall)
