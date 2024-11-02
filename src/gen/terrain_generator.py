import numpy as np
import noise

from ..world.terrain import Terrain

TERRAIN_X = 80
TERRAIN_Y = TERRAIN_X // 2
TERRAIN_Z = 16

LANDING_SIDE_LENGTH = 32

SCALE = 20

class TerrainGenerator(object):
    def __init__(self, width = TERRAIN_X, height = TERRAIN_Y):
        self.terrain = np.zeros((height, width))
        for y in range(height):
            for x in range(width):
                noise_value = noise.pnoise2(
                    x / SCALE,
                    y / SCALE,
                    octaves=6,
                    persistence=0.5,
                    lacunarity=2.0,
                    repeatx=width,
                    repeaty=height,
                    base=0
                )
                self.terrain[y][x] = int((noise_value + 1) / 2 * TERRAIN_Z)
        self.make_landing_area()
    
    def make_landing_area(self):
        width = len(self.terrain[0])
        height = len(self.terrain)
        y = height // 2
        x = width // 2
        s = LANDING_SIDE_LENGTH // 2
        z = 2
        for dx in range(x-s,x+s):
            for dy in range(y-s,y+s):
                self.terrain[dy][dx] = z
    
    def make(self):
        return Terrain(self.terrain)
