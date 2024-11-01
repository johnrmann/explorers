from enum import Enum

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
    