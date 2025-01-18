import unittest

from unittest.mock import MagicMock, Mock

from src.render.chunk import Chunk
from src.render.render_order import (
	RenderTuple,
	RenderOrder,
)


def n_by_n(n):
	"""Make a list of tuples representing an n x n grid."""
	return set([(x, y) for x in range(n) for y in range(n)])



class RenderTupleTest(unittest.TestCase):
	def test__init(self):
		gobj = MagicMock()
		chunk = MagicMock()
		rtuple = RenderTuple(tile=(4, 8), game_object=gobj, chunk=chunk)
		self.assertEqual(rtuple.cell, (4, 8))
		self.assertEqual(rtuple.game_object, gobj)
		self.assertEqual(rtuple.chunk, chunk)



class RenderOrderTest(unittest.TestCase):
	def setUp(self):
		self.mock_game_object = MagicMock()
		self.mock_game_object.cells_occupied = Mock()
		self.mock_game_object.cells_occupied.return_value = [
			(0, 0), (0, 1), (1, 0), (1, 1)
		]

		self.mock_chunk = MagicMock(spec=Chunk)
		self.mock_chunk.bounds = MagicMock()
		self.mock_chunk.bounds.cells = n_by_n(2)


	def test__init__empty(self):
		ro = RenderOrder()
		self.assertEqual(len(ro), 0)


	def test__add_cell__single(self):
		render_order = RenderOrder()
		render_order.add_cell((4, 8))
		ro = list(render_order)
		self.assertEqual(len(ro), 1)
		self.assertEqual(ro[0].cell, (4, 8))


	def test__add_cell__many(self):
		render_order = RenderOrder()
		render_order.add_cell((4,8))
		render_order.add_cell((15, 16))
		render_order.add_cell((23, 42))
		ro = list(render_order)
		self.assertEqual(len(ro), 3)
		self.assertEqual(ro[0].cell, (4, 8))
		self.assertEqual(ro[1].cell, (15, 16))
		self.assertEqual(ro[2].cell, (23, 42))


	def test__add_cells(self):
		render_order = RenderOrder()
		render_order.add_cells(n_by_n(2))
		ro = list(render_order)
		self.assertEqual(len(ro), 4)


	def test__add_game_object__single(self):
		render_order = RenderOrder()
		render_order.add_game_object(self.mock_game_object)
		ro = list(render_order)
		self.assertEqual(len(ro), 5)
		self.assertEqual(ro[0].cell, (0, 0))
		self.assertEqual(ro[1].cell, (0, 1))
		self.assertEqual(ro[2].cell, (1, 0))
		self.assertEqual(ro[3].cell, (1, 1))
		self.assertEqual(ro[4].game_object, self.mock_game_object)


	def test__add_chunk__single(self):
		render_order = RenderOrder()
		render_order.add_chunk(self.mock_chunk)
		ro = list(render_order)
		self.assertEqual(len(ro), 1)
		self.assertEqual(ro[0].chunk, self.mock_chunk)


	def test__contains__cell(self):
		ro = RenderOrder()
		ro.add_cell((4, 8))
		self.assertTrue((4, 8) in ro)


	def test__contains__cell_false(self):
		ro = RenderOrder()
		self.assertFalse((4, 8) in ro)


	def test__contains__game_object(self):
		ro = RenderOrder()
		ro.add_game_object(self.mock_game_object)
		self.assertTrue(self.mock_game_object in ro)


	def test__contains__game_object_false(self):
		ro = RenderOrder()
		self.assertFalse(self.mock_game_object in ro)


	def test__contains__game_object_cells(self):
		ro = RenderOrder()
		ro.add_game_object(self.mock_game_object)
		self.assertTrue((0, 0) in ro)
		self.assertTrue((0, 1) in ro)
		self.assertTrue((1, 0) in ro)
		self.assertTrue((1, 1) in ro)


	def test__contains__chunk(self):
		ro = RenderOrder()
		ro.add_chunk(self.mock_chunk)
		self.assertTrue(self.mock_chunk in ro)


	def test__contains__chunk_cells(self):
		ro = RenderOrder()
		ro.add_chunk(self.mock_chunk)
		for cell in n_by_n(2):
			self.assertTrue(cell in ro)



if __name__ == '__main__':
	unittest.main()
