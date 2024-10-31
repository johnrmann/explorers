import pygame

from ..world.terrain import Terrain

TILE_WIDTH = 48
TILE_HEIGHT = TILE_WIDTH // 2

TILE_Z = 48 // 8

GROUND_COLOR = (200, 0, 0)
WALL_COLOR = (100, 0, 0)

def global_tile_coords(x, y):
    """
    Returns the center coordinates of this tile on an infinite screen.
    """
    screen_x = (x - y) * (TILE_WIDTH // 2)
    screen_y = (x + y) * (TILE_HEIGHT // 2)
    return (screen_x, screen_y)

def relative_tile_coords(tile, camera):
    """
    tile_x, tile_y = 0, 0 and camera_x, camera_y = 0, 0 -> 
    """
    x,y = tile
    cx,cy = camera
    x2,y2 = global_tile_coords(x,y)
    return (
        x2 + (1024 // 2) - cx,
        y2 + (512 // 2) - cy,
    )

def tile_polygon(x, y):
    return [
        (x, y - TILE_HEIGHT // 2),
        (x + TILE_WIDTH // 2, y),
        (x, y + TILE_HEIGHT // 2),
        (x - TILE_WIDTH // 2, y)
    ]

def polygons(tile, h, camera):
    x2, y2 = relative_tile_coords(tile, camera)
    bottom = tile_polygon(x2, y2)
    top = [(p[0], p[1] - h * TILE_Z) for p in bottom]
    return (
        top,
        [top[3], top[2], bottom[2], bottom[3]],
        [top[2], top[1], bottom[1], bottom[2]]
    )

def render_tile(window, terrain: Terrain, tile):
    x,y = tile
    top, left_wall, right_wall = polygons(tile, terrain.map[y][x], (0,0))
    if top:
        pygame.draw.polygon(window, GROUND_COLOR, top)
    if left_wall:
        pygame.draw.polygon(window, WALL_COLOR, left_wall)
    if right_wall:
        pygame.draw.polygon(window, WALL_COLOR, right_wall)

def render_terrain(window, terrain: Terrain):
    window.fill((0,0,200))
    for x in range(0, 150):
        for y in range(0, 150):
            render_tile(window, terrain, (x,y))
