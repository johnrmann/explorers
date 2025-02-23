import unittest

from unittest.mock import MagicMock

from src.mgmt.game_manager import GameManager
from src.mgmt.event_manager import EventManager
from src.world.world import World
from src.world.terrain import Terrain

from src.gameobject.gameobject import GameObject
from src.math.direction import Direction

class _Widget(GameObject):
	"""
	GameObject is meant to be a sort of abstract class, so we stub it here
	for our tests.
	"""

class GameObjectTest(unittest.TestCase):
	def setUp(self):
		mock_world = MagicMock(spec=World)
		mock_terrain = MagicMock(spec=Terrain)
		mock_world.terrain = mock_terrain
		mock_terrain.height_at.return_value = 0
		evt_mgr = MagicMock(spec=EventManager)
		game_mgr = MagicMock(spec=GameManager)
		game_mgr.evt_mgr = evt_mgr
		game_mgr.world = mock_world
		self.game_mgr = game_mgr
		self.widget = _Widget(game_mgr=game_mgr, pos=(1,1), size=(2,2,2))

	def test__pos__correct(self):
		self.assertEqual(self.widget.pos, (1,1))

	def test__pos3__injects_terrain_height(self):
		self.game_mgr.world.terrain.height_at.return_value = 5
		self.assertEqual(self.widget.pos3, (1,1,5))

	def test__size__correct_2d(self):
		widget = _Widget(
			game_mgr=self.game_mgr, pos=(1,1), size=(2,2)
		)
		self.assertEqual(widget.size, (2,2,None))

	def test__size__correct_3d(self):
		self.assertEqual(self.widget.size, (2,2,2))

	def test__draw_point__northwest(self):
		point = self.widget.draw_point(Direction.NORTHWEST)
		self.assertEqual(point, (3, 3))

	def test__draw_point__northeast(self):
		point = self.widget.draw_point(Direction.NORTHEAST)
		self.assertEqual(point, (1, 3))

	def test__draw_point__southeast(self):
		point = self.widget.draw_point(Direction.SOUTHEAST)
		self.assertEqual(point, (3, 1))

	def test__draw_point__southwest(self):
		point = self.widget.draw_point(Direction.SOUTHWEST)
		self.assertEqual(point, (1, 1))

	def test__draw_point__default(self):
		point = self.widget.draw_point(None)
		self.assertEqual(point, (3, 3))

	def test__occupies_cell__true(self):
		self.assertTrue(self.widget.occupies_cell((1,1)))
		self.assertTrue(self.widget.occupies_cell((2,2)))

	def test__occupies_cell__false(self):
		self.assertFalse(self.widget.occupies_cell((0,0)))
		self.assertFalse(self.widget.occupies_cell((0,1)))
		self.assertFalse(self.widget.occupies_cell((1,0)))
		self.assertFalse(self.widget.occupies_cell((3,4)))
		self.assertFalse(self.widget.occupies_cell((3,3)))

	def test__not_manipulable_by_default(self):
		self.assertFalse(self.widget.is_deleteable(1))
		self.assertFalse(self.widget.is_moveable(1))
		self.assertFalse(self.widget.is_selectable(1))

if __name__ == '__main__':
	unittest.main()
