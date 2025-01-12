import unittest

from unittest.mock import MagicMock, Mock

from src.gameobject.lander import Lander

from src.world.terrain import Terrain
from src.world.world import World
from src.render.viewport import Viewport
from src.math.vector2 import Vector2

from src.mgmt.game_manager import GameManager

_FLAT_MAP = [
	[1] * 64 for _ in range(32)
]

class GameManagerTest(unittest.TestCase):
	def setUp(self):
		self.viewport = MagicMock(spec=Viewport)
		self.viewport.window_dims = (800, 600)
		self.terrain = Terrain(_FLAT_MAP)
		self.world = MagicMock(spec=World)
		self.world.terrain = self.terrain

	def test__utc(self):
		"""Test that UTC changes with the flow of time."""
		gm = GameManager(self.world, self.viewport, no_gui=True)
		self.assertEqual(gm.utc, 0)
		gm.tick(1 / 50)
		self.assertEqual(gm.utc, 1 / 50)
		gm.tick(49 / 50)
		self.assertEqual(gm.utc, 1)

	def test__select_actor(self):
		"""Test that we can select an actor."""
		gm = GameManager(self.world, self.viewport, no_gui=True)
		actor1 = gm.new_player_character((0, 0))
		actor2 = gm.new_player_character((1, 1))
		self.assertEqual(gm.selected_actors[1], actor1)
		gm.select_actor(1, actor2)
		self.assertEqual(gm.selected_actors[1], actor2)

	def test__select_actor__multiplayer(self):
		"""Test that we can select an actor in multiplayer mode."""
		gm = GameManager(self.world, self.viewport, no_gui=True)
		actor1 = gm.new_player_character((0, 0), owner=1)
		actor2 = gm.new_player_character((1, 1), owner=2)
		actor3 = gm.new_player_character((2, 2), owner=2)
		self.assertEqual(gm.selected_actors[1], actor1)
		self.assertEqual(gm.selected_actors[2], actor2)
		gm.select_actor(2, actor3)
		self.assertEqual(gm.selected_actors[1], actor1)
		self.assertEqual(gm.selected_actors[2], actor3)

	def test__tick__noop_when_paused(self):
		"""
		Ensure that pausing the game does not render events or tick objects.
		"""
		gm = GameManager(self.world, self.viewport, no_gui=True)
		p1 = gm.new_player_character((0, 0))
		p2 = gm.new_player_character((1, 1))
		p1.tick = MagicMock()
		p2.tick = MagicMock()
		gm.paused = True
		gm.tick(1)
		p1.tick.assert_not_called()
		p2.tick.assert_not_called()

	def test__tick__ticks_objects(self):
		"""Ensure that game objects are ticked."""
		gm = GameManager(self.world, self.viewport, no_gui=True)
		p1 = gm.new_player_character((0, 0))
		p2 = gm.new_player_character((1, 1))
		p1.tick = MagicMock()
		p2.tick = MagicMock()
		gm.tick(1)
		p1.tick.assert_called_once()
		p2.tick.assert_called_once()

	def test__tick__rejects_time_travel(self):
		"""Ensure that an error is thrown if we try to tick with a negative
		dt."""
		gm = GameManager(self.world, self.viewport, no_gui=True)
		self.assertRaises(ValueError, lambda: gm.tick(-1))

	def test__tick__evolves_world(self):
		"""Test that the world evolves one second at a time."""
		gm = GameManager(self.world, self.viewport, no_gui=True)
		gm.world.tick_second = MagicMock()
		gm.tick(0.5)
		gm.world.tick_second.assert_not_called()
		gm.tick(0.5)
		gm.world.tick_second.assert_called_once_with(1)

	def test__tick__evolves_world_multiple_seconds(self):
		"""Test that the world evolves multiple seconds at a time."""
		gm = GameManager(self.world, self.viewport, no_gui=True)
		gm.world.tick_second = MagicMock()
		gm.tick(2)
		gm.world.tick_second.assert_called_once_with(2)

	def test__add_game_object__calls_init(self):
		"""Test that add_game_object calls the object's init method."""
		gm = GameManager(self.world, self.viewport, no_gui=True)
		obj = MagicMock()
		obj.on_init = Mock()
		gm.add_game_object(obj)
		obj.on_init.assert_called_once()

	def test__add_game_object__adds_game_object(self):
		"""Test that add_game_object adds the object to the game_objects set."""
		gm = GameManager(self.world, self.viewport, no_gui=True)
		obj = MagicMock()
		gm.add_game_object(obj)
		self.assertIn(obj, gm.game_objects)

	def test__remove_game_object__calls_remove(self):
		"""Test that remove_game_object calls the object's remove method."""
		gm = GameManager(self.world, self.viewport, no_gui=True)
		obj = MagicMock()
		obj.on_remove = Mock()
		gm.add_game_object(obj)
		gm.remove_game_object(obj)
		obj.on_remove.assert_called_once()

	def test__remove_game_object__removes_game_object(self):
		"""Test that remove_game_object removes the object from the game_objects
		set."""
		gm = GameManager(self.world, self.viewport, no_gui=True)
		obj = MagicMock()
		gm.add_game_object(obj)
		gm.remove_game_object(obj)
		self.assertNotIn(obj, gm.game_objects)

	def test__new_colony(self):
		"""Test that new_colony creates a new colony."""
		gm = GameManager(self.world, self.viewport, no_gui=True)
		self.assertEqual(len(gm.colonies), 0)
		gm.new_colony(
			position=(0,0),
			owner=1,
			is_first=True
		)
		self.assertEqual(len(gm.colonies), 1)

	def test__new_colony__adds_structures(self):
		"""Test that new_colony adds structures to the world."""
		gm = GameManager(self.world, self.viewport, no_gui=True)
		lander = Lander(
			pos=(0, 0),
			game_mgr=gm,
		)
		lander.owner = 1
		gm.add_game_object(lander)
		colony = gm.new_colony(
			position=(0,0),
			owner=1,
			is_first=True
		)
		self.assertEqual(len(colony.structures), 1)
		self.assertIn(lander, colony.structures)

	def test__can_place_gameobject_at__works(self):
		"""Test that can_place_gameobject_at works."""
		gm = GameManager(self.world, self.viewport)
		obj = MagicMock()
		obj.size = (1,1)
		gm.is_cell_occupied = Mock(return_value=False)
		self.assertTrue(gm.can_place_gameobject_at(obj, Vector2(0,0)))

	def test__can_place_gameobject_at__occupied(self):
		"""Test that can_place_gameobject_at returns False when the cell is
		occupied."""
		gm = GameManager(self.world, self.viewport)
		obj = MagicMock()
		obj.size = (1,1)
		gm.is_cell_occupied = Mock(return_value=True)
		self.assertFalse(gm.can_place_gameobject_at(obj, Vector2(0,0)))

	def test__can_place_gameobject_at__position_out_of_bounds(self):
		"""Test that can_place_gameobject_at returns False when the object is
		out of bounds."""
		gm = GameManager(self.world, self.viewport)
		obj = MagicMock()
		obj.size = (1,1)
		gm.is_cell_occupied = Mock(return_value=False)
		self.assertFalse(gm.can_place_gameobject_at(obj, Vector2(0,-1)))

	def test__can_place_gameobject_at__size_out_of_bounds(self):
		"""Test that can_place_gameobject_at returns False when the object is
		out of bounds."""
		gm = GameManager(self.world, self.viewport)
		obj = MagicMock()
		obj.size = Vector2(5,5)
		gm.is_cell_occupied = Mock(return_value=False)
		self.assertFalse(gm.can_place_gameobject_at(obj, Vector2(0,30)))

	def test__can_place_gameobject_at__not_flat(self):
		"""Test that can_place_gameobject_at returns False when the cell is
		occupied."""
		gm = GameManager(self.world, self.viewport)
		obj = MagicMock()
		obj.size = Vector2(1,1)
		gm.world.terrain.is_area_flat = Mock(return_value=False)
		self.assertFalse(gm.can_place_gameobject_at(obj, Vector2(0,0)))

if __name__ == "__main__":
	unittest.main()
