import pygame
import math

from ..world.terrain import Terrain
from src.render.viewport import Viewport, TILE_WIDTH, TILE_HEIGHT, TILE_Z

GROUND_COLOR = (200, 0, 0)
WALL_COLOR = (100, 0, 0)

def tile_coords_to_global_screen_coords(x, y, tile_width = TILE_WIDTH):
    """
    Returns the center coordinates of this tile on an infinite screen.
    """
    tile_height = tile_width // 2
    screen_x = (x - y) * (tile_width // 2)
    screen_y = (x + y) * (tile_height // 2)
    return (screen_x, screen_y)

def tile_coords_to_screen_coords(tile, camera_screen, tile_width = TILE_WIDTH):
    """
    tile_x, tile_y = 0, 0 and camera_x, camera_y = 0, 0 -> 
    """
    win_width, win_height = pygame.display.get_window_size()
    x,y = tile
    cx,cy = camera_screen
    x2,y2 = tile_coords_to_global_screen_coords(x, y, tile_width)
    return (
        x2 + (win_width // 2) - cx,
        y2 + (win_height // 2) - cy,
    )

def tile_polygon(x, y, tile_width = TILE_WIDTH):
    tile_height = tile_width // 2
    return [
        (x, y - tile_height // 2),
        (x + tile_width // 2, y),
        (x, y + tile_height // 2),
        (x - tile_width // 2, y)
    ]

def polygons(vp, terrain, tile):
    x,y = tile
    h = terrain.map[y][x]
    camera_screen = tile_coords_to_global_screen_coords(vp.camera_pos[0], vp.camera_pos[1], vp.tile_width)
    tx_screen, ty_screen = tile_coords_to_screen_coords(tile, camera_screen)
    bottom = tile_polygon(tx_screen, ty_screen, vp.tile_width)
    top = [(p[0], p[1] - h * TILE_Z) for p in bottom]
    return (
        top,
        [top[3], top[2], bottom[2], bottom[3]],
        [top[2], top[1], bottom[1], bottom[2]]
    )

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
            pygame.draw.polygon(self.window, WALL_COLOR, left_wall)
        if right_wall:
            pygame.draw.polygon(self.window, WALL_COLOR, right_wall)
    
    def render(self):
        self.window.fill((0,0,200))
        for x in self.vp.get_x_range():
            for y in self.vp.get_y_range():
                p = (x,y)
                self.render_tile(p)