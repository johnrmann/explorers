import pygame
import math

from ..world.terrain import Terrain
from src.render.viewport import Viewport, TILE_WIDTH, TILE_HEIGHT, TILE_Z

GROUND_COLOR = (200, 0, 0)
WALL_COLOR = (100, 0, 0)

def tile_coords_to_global_screen_coords(x, y):
    """
    Returns the center coordinates of this tile on an infinite screen.
    """
    screen_x = (x - y) * (TILE_WIDTH // 2)
    screen_y = (x + y) * (TILE_HEIGHT // 2)
    return (screen_x, screen_y)

def tile_coords_to_screen_coords(tile, camera_screen):
    """
    tile_x, tile_y = 0, 0 and camera_x, camera_y = 0, 0 -> 
    """
    win_width, win_height = pygame.display.get_window_size()
    x,y = tile
    cx,cy = camera_screen
    x2,y2 = tile_coords_to_global_screen_coords(x,y)
    return (
        x2 + (win_width // 2) - cx,
        y2 + (win_height // 2) - cy,
    )

def tile_polygon(x, y):
    return [
        (x, y - TILE_HEIGHT // 2),
        (x + TILE_WIDTH // 2, y),
        (x, y + TILE_HEIGHT // 2),
        (x - TILE_WIDTH // 2, y)
    ]

def polygons(terrain, tile, camera_screen):
    x,y = tile
    h = terrain.map[y][x]
    tx_screen, ty_screen = tile_coords_to_screen_coords(tile, camera_screen)
    bottom = tile_polygon(tx_screen, ty_screen)
    top = [(p[0], p[1] - h * TILE_Z) for p in bottom]
    return (
        top,
        [top[3], top[2], bottom[2], bottom[3]],
        [top[2], top[1], bottom[1], bottom[2]]
    )

class RenderTerrain(object):
    def __init__(self, window, vp: Viewport):
        self.window = window
        self.vp = vp

    def render_tile(self, p):
        cx,cy = self.vp.camera_pos
        camera_screen = tile_coords_to_global_screen_coords(cx,cy)
        top, left_wall, right_wall = polygons(self.vp.terrain, p, camera_screen)
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