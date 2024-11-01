import math

from enum import Enum

TILE_WIDTH = 48
TILE_HEIGHT = TILE_WIDTH // 2

TILE_Z = 48 // 8

SAFETY = 3

class CameraDirection(Enum):
    NORTH = 1
    NORTHEAST = 2
    EAST = 3
    SOUTHEAST = 4
    SOUTH = 5
    SOUTHWEST = 6
    WEST = 7
    NORTHWEST = 8

def camera_direction_to_delta(camdir: CameraDirection):
    if camdir == CameraDirection.NORTH:
        return (0, -1)
    elif camdir == CameraDirection.NORTHEAST:
        return (1, -1)
    elif camdir == CameraDirection.EAST:
        return (1, 0)
    elif camdir == CameraDirection.SOUTHEAST:
        return (1, 1)
    elif camdir == CameraDirection.SOUTH:
        return (0, 1)
    elif camdir == CameraDirection.SOUTHWEST:
        return (-1, 1)
    elif camdir == CameraDirection.WEST:
        return (-1, 0)
    elif camdir == CameraDirection.NORTHWEST:
        return (-1, -1)
    raise "Unknown camera direction"

class Viewport(object):
    def __init__(self, window_dims, terrain):
        self.window_dims = window_dims
        self.terrain = terrain
        self.camera_pos = terrain.center()
    
    def move_camera(self, camdir: CameraDirection):
        dx,dy = camera_direction_to_delta(camdir)
        cx,cy = self.camera_pos
        cx2,cy2 = (cx + dx, cy + dy)

        if cy2 < 0:
            cy2 = 0
        elif cy2 >= self.terrain.height():
            cy2 = self.terrain.height() - 1
        
        if cx2 == -1:
            cx2 = self.terrain.width() - 1
        if cx2 >= self.terrain.width():
            cx2 = 0
        
        self.camera_pos = (cx2, cy2)
    
    def get_x_range(self):
        win_width, _ = self.window_dims
        cx, _ = self.camera_pos
        left = max(
            0,
            math.ceil(cx - (win_width / TILE_WIDTH)) - SAFETY
        )
        right = min(
            self.terrain.width(),
            math.ceil(cx + (win_width / TILE_WIDTH)) + SAFETY
        )
        return range(left, right)
    
    def get_y_range(self):
        _, win_height = self.window_dims
        _, cy = self.camera_pos
        top = max(
            0,
            math.ceil(cy - (win_height / TILE_HEIGHT)) - SAFETY
        )
        bottom = min(
            self.terrain.height(),
            math.ceil(cy + (win_height / TILE_HEIGHT)) + SAFETY
        )
        return range(top, bottom)
    