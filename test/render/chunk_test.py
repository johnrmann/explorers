import unittest

from unittest.mock import MagicMock, patch

from src.math.direction import Direction
from src.math.vector2 import Vector2
from src.rendermath.cell import cell_polygon_on_global_screen
from src.world.terrain import Terrain
from src.render.viewport import Viewport
from src.render.terrain_helper import TerrainSurfacer

from src.render.chunk import (
	ChunkSurfaceKey,
	ChunkBounds,
	Chunk,
	TerrainChunker
)

def _vec2s(*args):
	return [Vector2(t) for t in args]

class ChunkBoundsTest(unittest.TestCase):
	def test__cells(self):
		origin = (0, 0)
		size = 2
		bounds = ChunkBounds(origin, size)
		result = [(x, y) for x, y in bounds.cells]
		self.assertIn((0, 0), result)
		self.assertIn((1, 0), result)
		self.assertIn((0, 1), result)
		self.assertIn((1, 1), result)
		self.assertEqual(len(result), 4)


	def test__shift_right_cells(self):
		origin = (0, 0)
		size = 2
		bounds = ChunkBounds(origin, size)
		result = [(x, y) for x, y in bounds.shift_right_cells()]
		self.assertIn((1, 0), result)
		self.assertIn((2, 0), result)
		self.assertIn((1, 1), result)
		self.assertIn((2, 1), result)
		self.assertEqual(len(result), 4)


	def test__top_corner__northwest(self):
		origin = (0, 0)
		size = 4
		bounds = ChunkBounds(origin, size)
		result = bounds.top_corner()
		self.assertEqual(result, (0, 0))


	def test__top_corner__northeast(self):
		origin = (0, 0)
		size = 4
		bounds = ChunkBounds(origin, size)
		result = bounds.top_corner(cam_dir=Direction.NORTHEAST)
		self.assertEqual(result, (3, 0))


	def test__top_corner__southeast(self):
		origin = (0, 0)
		size = 4
		bounds = ChunkBounds(origin, size)
		result = bounds.top_corner(cam_dir=Direction.SOUTHEAST)
		self.assertEqual(result, (3, 3))


	def test__top_corner__southwest(self):
		origin = (0, 0)
		size = 4
		bounds = ChunkBounds(origin, size)
		result = bounds.top_corner(cam_dir=Direction.SOUTHWEST)
		self.assertEqual(result, (0, 3))


	def test__top_corner__invalid(self):
		with self.assertRaises(ValueError):
			origin = (0, 0)
			size = 4
			bounds = ChunkBounds(origin, size)
			bounds.top_corner(cam_dir=Direction.EAST)


	def test__inner_wall_cells__single(self):
		origin = (0, 0)
		size = 1
		bounds = ChunkBounds(origin, size)
		result = [(x, y) for x, y in bounds.inner_wall_cells()]
		self.assertEqual(result, [(0, 0), (0, 0)])


	def test__inner_wall_cells__2by2(self):
		origin = (0, 0)
		size = 2
		bounds = ChunkBounds(origin, size)
		result = [(x, y) for x, y in bounds.inner_wall_cells()]
		self.assertEqual(result, [
			(1, 0), (1, 1),
			(1, 1), (0, 1)
		])


	def test__outer_wall_cells__single(self):
		origin = (0, 0)
		size = 1
		bounds = ChunkBounds(origin, size)
		result = [(x, y) for x, y in bounds.outer_wall_cells()]
		self.assertEqual(result, [
			(1, 0), (0, 1)
		])


	def test__outer_wall_cells__2by2(self):
		origin = (0, 0)
		size = 2
		bounds = ChunkBounds(origin, size)
		result = [(x, y) for x, y in bounds.outer_wall_cells()]
		self.assertEqual(result, [
			(2, 0), (2, 1),
			(1, 2), (0, 2),
		])



class ChunkTest(unittest.TestCase):
	def setUp(self):
		def _mock_surfacer_draws(**kwargs):
			return [(7, 'tile_surface')]

		self.mock_surfacer = MagicMock(spec=TerrainSurfacer)
		self.mock_surfacer.draws = _mock_surfacer_draws


	def test__is_unobstructed_internally__flat(self):
		heightmap = [
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
		]
		terrain = Terrain(heightmap)
		chunk = Chunk(terrain=terrain, bounds=ChunkBounds((0, 0), 2))
		result = chunk.is_unobstructed_internally()
		self.assertTrue(result)


	def test__is_unobstructed_internally__raised(self):
		heightmap = [
			[8, 8, 9, 0],
			[8, 8, 9, 0],
			[9, 9, 9, 9],
			[0, 0, 0, 0],
		]
		terrain = Terrain(heightmap)
		chunk = Chunk(terrain=terrain, bounds=ChunkBounds((0, 0), 2))
		result = chunk.is_unobstructed_internally()
		self.assertTrue(result)


	def test__is_unobstructed_internally__descending(self):
		heightmap = [
			[8, 7, 6, 5],
			[7, 6, 5, 4],
			[6, 5, 4, 3],
			[5, 4, 3, 2],
		]
		terrain = Terrain(heightmap)
		chunk = Chunk(terrain=terrain, bounds=ChunkBounds((0, 0), 2))
		result = chunk.is_unobstructed_internally()
		self.assertTrue(result)


	def test__is_unobstructed_internally__obstructed(self):
		heightmap = [
			[0, 1, 0, 0],
			[1, 2, 1, 0],
			[0, 1, 0, 0],
			[0, 0, 0, 0],
		]
		terrain = Terrain(heightmap)
		chunk = Chunk(terrain=terrain, bounds=ChunkBounds((0, 0), 2))
		result = chunk.is_unobstructed_internally()
		self.assertFalse(result)


	def test__is_unobstructed_exernally__flat(self):
		heightmap = [
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
		]
		terrain = Terrain(heightmap)
		chunk = Chunk(terrain=terrain, bounds=ChunkBounds((0, 0), 2))
		result = chunk.is_unobstructed_externally()
		self.assertTrue(result)


	def test__is_unobstructed_externally__raised_outside(self):
		heightmap = [
			[0, 0, 8, 8],
			[0, 0, 8, 8],
			[8, 8, 8, 8],
			[8, 8, 8, 8],
		]
		terrain = Terrain(heightmap)
		chunk = Chunk(terrain=terrain, bounds=ChunkBounds((0, 0), 2))
		result = chunk.is_unobstructed_externally()
		self.assertFalse(result)


	def test__wall_height__flat(self):
		heightmap = [
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
		]
		terrain = Terrain(heightmap)
		helper = TerrainSurfacer()
		chunk = Chunk(
			terrain=terrain,
			bounds=ChunkBounds((0, 0), 2),
			terrain_surfacer=helper
		)
		result = chunk.wall_height(Direction.NORTHWEST)
		self.assertEqual(result, 0)


	def test__wall_height__raised(self):
		heightmap = [
			[8, 8, 0, 0],
			[8, 8, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
		]
		terrain = Terrain(heightmap)
		chunk = Chunk(terrain=terrain, bounds=ChunkBounds((0, 0), 2))
		result = chunk.wall_height(Direction.NORTHWEST)
		self.assertEqual(result, 8)


	def test__wall_height__raised_flat(self):
		heightmap = [
			[8, 8, 8, 0],
			[8, 8, 8, 0],
			[8, 8, 8, 0],
			[0, 0, 0, 0],
		]
		terrain = Terrain(heightmap)
		chunk = Chunk(terrain=terrain, bounds=ChunkBounds((0, 0), 2))
		result = chunk.wall_height(Direction.NORTHWEST)
		self.assertEqual(result, 0)


	def test__sanity__cell_polygon(self):
		cell_polygon = cell_polygon_on_global_screen(
			(0, 0),
			Direction.NORTHWEST,
			(48, 24)
		)
		self.assertEqual(cell_polygon[0], (0, -12))
		self.assertEqual(cell_polygon[1], (24, 0))
		self.assertEqual(cell_polygon[2], (0, 12))
		self.assertEqual(cell_polygon[3], (-24, 0))


	def test__get_rect__single(self):
		heightmap = [
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
		]
		terrain = Terrain(heightmap)
		chunk = Chunk(terrain=terrain, bounds=ChunkBounds((0, 0), 1))
		offset, dimensions = chunk.get_rect(
			cam_dir=Direction.NORTHWEST,
			tile_width=48
		)
		self.assertEqual(offset, (-24.0, -12.0))
		self.assertEqual(dimensions, (48, 24))


	def test__get_rect__flat(self):
		heightmap = [
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
		]
		terrain = Terrain(heightmap)
		chunk = Chunk(terrain=terrain, bounds=ChunkBounds((0, 0), 2))
		offset, dimensions = chunk.get_rect(
			cam_dir=Direction.NORTHWEST,
			tile_width=48
		)
		self.assertEqual(offset, (-48, -12.0))
		self.assertEqual(dimensions, (96, 48))


	def test__get_rect__raised(self):
		heightmap = [
			[8, 8, 0, 0],
			[8, 8, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
		]
		terrain = Terrain(heightmap)
		chunk = Chunk(terrain=terrain, bounds=ChunkBounds((0, 0), 2))
		offset, dimensions = chunk.get_rect(
			cam_dir=Direction.NORTHWEST,
			tile_width=64
		)
		self.assertEqual(tuple(offset), (-64, -48))
		self.assertEqual(dimensions, (128, 64 + 32))


	def test__get_rect__raised_flat(self):
		heightmap = [
			[8, 8, 8, 0],
			[8, 8, 8, 0],
			[8, 8, 8, 0],
			[0, 0, 0, 0],
		]
		terrain = Terrain(heightmap)
		chunk = Chunk(terrain=terrain, bounds=ChunkBounds((0, 0), 2))
		offset, dimensions = chunk.get_rect(
			cam_dir=Direction.NORTHWEST,
			tile_width=64
		)
		self.assertEqual(tuple(offset), (-64, -48))
		self.assertEqual(dimensions, (128, 64))


	def test__draws__adds_height_offsets(self):
		heightmap = [
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
		]
		terrain = Terrain(heightmap)
		chunk = Chunk(
			terrain=terrain,
			bounds=ChunkBounds((0, 0), 2),
			terrain_surfacer=self.mock_surfacer
		)
		result = list(chunk.draws(key=ChunkSurfaceKey(
			Direction.NORTHWEST, 7, 64
		)))
		self.assertEqual(len(result), 4)
		self.assertEqual(result[0], ((-32, -16 + 7), "tile_surface"))
		self.assertEqual(result[1], ((-64, 7), "tile_surface"))
		self.assertEqual(result[2], ((0, 7), "tile_surface"))
		self.assertEqual(result[3], ((-32, 16 + 7), "tile_surface"))



class TerrainChunkerTest(unittest.TestCase):
	def setUp(self):
		basic_heightmap = [
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
		]
		self.basic_terrain = Terrain(basic_heightmap)
		self.viewport = Viewport((800, 600), self.basic_terrain)
		self.surfacer = TerrainSurfacer()


	def test__all_chunk_origins(self):
		chunker = TerrainChunker(
			terrain=self.basic_terrain,
			surfacer=self.surfacer,
			chunk_size=2
		)
		result = set(chunker.all_chunk_origins())
		result_tuples = [(x, y) for x, y in result]
		self.assertIn((0, 0), result_tuples)
		self.assertIn((2, 0), result_tuples)
		self.assertIn((0, 2), result_tuples)
		self.assertIn((2, 2), result_tuples)


	def test__make_all_chunks__basic(self):
		chunker = TerrainChunker(
			terrain=self.basic_terrain,
			surfacer=self.surfacer,
			chunk_size=2
		)
		self.assertEqual(len(chunker.get_chunks()), 0)
		chunker.make_all_chunks()
		self.assertEqual(len(chunker.get_chunks()), 4)
		for chunk in chunker.get_chunks():
			self.assertIsInstance(chunk, Chunk)


	def test__make_chunk__wont_remake(self):
		chunker = TerrainChunker(
			terrain=self.basic_terrain,
			surfacer=self.surfacer,
			chunk_size=2
		)
		make1 = chunker.make_chunk((0, 0))
		self.assertEqual(len(chunker.get_chunks()), 1)
		make2 = chunker.make_chunk((0, 0))
		self.assertEqual(len(chunker.get_chunks()), 1)
		self.assertEqual(make1, make2)


	def test__chunk_index_for_cell__basic(self):
		chunker = TerrainChunker(
			terrain=self.basic_terrain,
			surfacer=self.surfacer,
			chunk_size=2
		)
		result = chunker.chunk_index_for_cell(Vector2(3, 3))
		self.assertEqual(result, (1, 1))


	def test__chunk_index_for_cell__negative(self):
		chunker = TerrainChunker(
			terrain=self.basic_terrain,
			surfacer=self.surfacer,
			chunk_size=2
		)
		result = chunker.chunk_index_for_cell(Vector2(-1, 0))
		self.assertEqual(result, (1, 0))


	def test__chunk_index_for_cell__looped(self):
		chunker = TerrainChunker(
			terrain=self.basic_terrain,
			surfacer=self.surfacer,
			chunk_size=2
		)
		result = chunker.chunk_index_for_cell(Vector2(4, 0))
		self.assertEqual(result, (0, 0))


	def test__init__nothing_dirty(self):
		chunker = TerrainChunker(
			terrain=self.basic_terrain,
			surfacer=self.surfacer,
			chunk_size=2
		)
		for x in range(4):
			for y in range(4):
				self.assertFalse(chunker.is_cell_dirty(Vector2(x, y)))


	def test__mark_is_cell_dirty__exact(self):
		chunker = TerrainChunker(
			terrain=self.basic_terrain,
			surfacer=self.surfacer,
			chunk_size=2
		)
		chunker.mark_cell_dirty((0, 0))
		self.assertTrue(chunker.is_cell_dirty((0, 0)))


	def test__mark_is_cell_dirty__chunk(self):
		chunker = TerrainChunker(
			terrain=self.basic_terrain,
			surfacer=self.surfacer,
			chunk_size=2
		)
		chunker.mark_cell_dirty((0, 0))
		self.assertTrue(chunker.is_cell_dirty((0, 0)))
		self.assertTrue(chunker.is_cell_dirty((0, 1)))
		self.assertTrue(chunker.is_cell_dirty((1, 1)))
		self.assertTrue(chunker.is_cell_dirty((1, 0)))


	def test__chunks_intersecting_rect__single(self):
		chunker = TerrainChunker(
			terrain=self.basic_terrain,
			surfacer=self.surfacer,
			chunk_size=2
		)
		chunker.make_all_chunks()
		result = list(chunker.chunks_intersecting_rect(((0, 0), (1, 1))))
		self.assertEqual(len(result), 1)
		self.assertEqual(tuple(result[0].bounds.origin), (0, 0))


	def test__chunks_intersecting_rect__span_x(self):
		chunker = TerrainChunker(
			terrain=self.basic_terrain,
			surfacer=self.surfacer,
			chunk_size=2
		)
		chunker.make_all_chunks()
		result = list(chunker.chunks_intersecting_rect(((1, 1), (2, 1))))
		self.assertEqual(len(result), 2)
		self.assertEqual(tuple(result[0].bounds.origin), (0, 0))
		self.assertEqual(tuple(result[1].bounds.origin), (2, 0))


	def test__chunks_intersecting_rect__span_y(self):
		chunker = TerrainChunker(
			terrain=self.basic_terrain,
			surfacer=self.surfacer,
			chunk_size=2
		)
		chunker.make_all_chunks()
		result = list(chunker.chunks_intersecting_rect(((1, 1), (1, 2))))
		self.assertEqual(len(result), 2)
		self.assertEqual(tuple(result[0].bounds.origin), (0, 0))
		self.assertEqual(tuple(result[1].bounds.origin), (0, 2))


	def test__chunks_intersecting_rect__span_both(self):
		chunker = TerrainChunker(
			terrain=self.basic_terrain,
			surfacer=self.surfacer,
			chunk_size=2
		)
		chunker.make_all_chunks()
		result = list(chunker.chunks_intersecting_rect(((1, 1), (2, 2))))
		self.assertEqual(len(result), 4)
		self.assertEqual(tuple(result[0].bounds.origin), (0, 0))
		self.assertEqual(tuple(result[1].bounds.origin), (0, 2))
		self.assertEqual(tuple(result[2].bounds.origin), (2, 0))
		self.assertEqual(tuple(result[3].bounds.origin), (2, 2))



if __name__ == '__main__':
	unittest.main()
