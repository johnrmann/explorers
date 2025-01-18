import pygame

from src.render.chunk import (
	TerrainChunker,
	Chunk,
	ChunkBounds,
	ChunkSurfaceKey
)
from src.render.terrain_helper import TerrainSurfacer
from src.render.viewport import Viewport

from src.world.terrain import Terrain

pygame.init()
window = pygame.display.set_mode((1440, 900))

flat_map = [
	[1] * 64 for _ in range(64)
]
flat_map[0][0] = 8
flat_map[2][2] = 8

terrain = Terrain(flat_map)
vp = Viewport((1440, 900), terrain)
surfacer = TerrainSurfacer()
chunker = TerrainChunker(terrain=terrain, surfacer=surfacer, chunk_size=16)

chunk = chunker.make_chunk((0, 0))

pygame.image.save(chunk._get_surface(ChunkSurfaceKey(
	orientation=vp.camera_orientation,
	tile_width=vp.tile_width,
	light=7
)), 'chunk.png')

pygame.quit()
