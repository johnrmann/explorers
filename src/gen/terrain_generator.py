import numpy as np
import noise

from ..world.terrain import Terrain

TERRAIN_X = 512
TERRAIN_Y = TERRAIN_X // 2
TERRAIN_Z = TERRAIN_Y // 2

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
    
    def make(self):
        return Terrain(self.terrain)
