import unittest

from unittest.mock import MagicMock, Mock

from src.world.terrain import Terrain
from src.world.world import World
from src.render.viewport import Viewport

from src.mgmt.game_manager import GameManager

class GameManagerTest(unittest.TestCase):
	def setUp(self):
		self.viewport = MagicMock(spec=Viewport)
		self.viewport.window_dims = (800, 600)
		self.terrain = MagicMock(spec=Terrain)
		self.world = MagicMock(spec=World)
		self.world.terrain = self.terrain

	def test__utc(self):
		"""Test that UTC changes with the flow of time."""
		gm = GameManager(self.world, self.viewport)
		self.assertEqual(gm.utc, 0)
		gm.tick(1 / 50)
		self.assertEqual(gm.utc, 1 / 50)
		gm.tick(49 / 50)
		self.assertEqual(gm.utc, 1)

	def test__select_actor(self):
		"""Test that we can select an actor."""
		gm = GameManager(self.world, self.viewport)
		actor1 = gm.new_player_character((0, 0))
		actor2 = gm.new_player_character((1, 1))
		self.assertEqual(gm.selected_actors[1], actor1)
		gm.select_actor(1, actor2)
		self.assertEqual(gm.selected_actors[1], actor2)

	def test__select_actor__multiplayer(self):
		"""Test that we can select an actor in multiplayer mode."""
		gm = GameManager(self.world, self.viewport)
		actor1 = gm.new_player_character((0, 0), owner=1)
		actor2 = gm.new_player_character((1, 1), owner=2)
		actor3 = gm.new_player_character((2, 2), owner=2)
		self.assertEqual(gm.selected_actors[1], actor1)
		self.assertEqual(gm.selected_actors[2], actor2)
		gm.select_actor(2, actor3)
		self.assertEqual(gm.selected_actors[1], actor1)
		self.assertEqual(gm.selected_actors[2], actor3)

	def test__tick__rejects_time_travel(self):
		"""Ensure that an error is thrown if we try to tick with a negative
		dt."""
		gm = GameManager(self.world, self.viewport)
		self.assertRaises(ValueError, lambda: gm.tick(-1))

	def test__tick__evolves_world(self):
		"""Test that the world evolves one second at a time."""
		gm = GameManager(self.world, self.viewport)
		gm.world.evolve = MagicMock()
		gm.tick(0.5)
		gm.world.evolve.assert_not_called()
		gm.tick(0.5)
		gm.world.evolve.assert_called_once_with(1)

	def test__tick__evolves_world_multiple_seconds(self):
		"""Test that the world evolves multiple seconds at a time."""
		gm = GameManager(self.world, self.viewport)
		gm.world.evolve = MagicMock()
		gm.tick(2)
		gm.world.evolve.assert_called_once_with(2)

	def test__add_game_object__calls_init(self):
		"""Test that add_game_object calls the object's init method."""
		gm = GameManager(self.world, self.viewport)
		obj = MagicMock()
		obj.on_init = Mock()
		gm.add_game_object(obj)
		obj.on_init.assert_called_once()

	def test__add_game_object__adds_game_object(self):
		"""Test that add_game_object adds the object to the game_objects set."""
		gm = GameManager(self.world, self.viewport)
		obj = MagicMock()
		gm.add_game_object(obj)
		self.assertIn(obj, gm.game_objects)

	def test__remove_game_object__calls_remove(self):
		"""Test that remove_game_object calls the object's remove method."""
		gm = GameManager(self.world, self.viewport)
		obj = MagicMock()
		obj.on_remove = Mock()
		gm.add_game_object(obj)
		gm.remove_game_object(obj)
		obj.on_remove.assert_called_once()

	def test__remove_game_object__removes_game_object(self):
		"""Test that remove_game_object removes the object from the game_objects
		set."""
		gm = GameManager(self.world, self.viewport)
		obj = MagicMock()
		gm.add_game_object(obj)
		gm.remove_game_object(obj)
		self.assertNotIn(obj, gm.game_objects)

if __name__ == "__main__":
	unittest.main()
