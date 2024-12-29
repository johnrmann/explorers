import unittest

from src.path.visibility import Visibility

class VisibilityTest(unittest.TestCase):
	def test__init__rejects_empty_dimensions(self):
		with self.assertRaises(ValueError):
			Visibility(None)

	def test__init__rejects_non_2d_dimensions(self):
		with self.assertRaises(ValueError):
			Visibility([1, 2, 3])

	def test__init__creates_empty(self):
		viz = Visibility((32, 32))
		explored = viz.explored_matrix(1)
		self.assertEqual(len(explored), 32)
		self.assertEqual(len(explored[0]), 32)
		for row in explored:
			self.assertEqual(sum(row), 0)
		visible = viz.visible_matrix(1)
		self.assertEqual(len(visible), 32)
		self.assertEqual(len(visible[0]), 32)
		for row in visible:
			self.assertEqual(sum(row), 0)

	def test__mark_explored__marks(self):
		viz = Visibility((32, 32))
		self.assertEqual(viz.is_explored((0, 0), 1), False)
		viz.mark_explored((0, 0), 1)
		self.assertEqual(viz.is_explored((0, 0), 1), True)

	def test__mark_explored__marks_modulo(self):
		viz = Visibility((32, 32))
		viz.mark_explored((32, 0), 1)
		self.assertEqual(viz.is_explored((0, 0), 1), True)

	def test__mark_explored__for_player(self):
		viz = Visibility((32, 32))
		viz.mark_explored((0, 0), 1)
		self.assertEqual(viz.is_explored((0, 0), 1), True)
		self.assertEqual(viz.is_explored((0, 0), 2), False)
		viz.mark_explored((0, 0), 2)
		self.assertEqual(viz.is_explored((0, 0), 1), True)

	def test__explored_matrix__correct(self):
		viz = Visibility((32, 32))
		viz.mark_explored((0, 0), 1)
		viz.mark_explored((1, 1), 2)
		explored1 = viz.explored_matrix(1)
		self.assertEqual(explored1[0][0], 1)
		self.assertEqual(explored1[1][1], 0)
		explored2 = viz.explored_matrix(2)
		self.assertEqual(explored2[0][0], 0)
		self.assertEqual(explored2[1][1], 1)

	def test__toggle_visible__toggles(self):
		viz = Visibility((32, 32))
		self.assertEqual(viz.is_visible((0, 0), 1), False)
		viz.toggle_visible((0, 0), 1)
		self.assertEqual(viz.is_visible((0, 0), 1), True)
		viz.toggle_visible((0, 0), 1)
		self.assertEqual(viz.is_visible((0, 0), 1), False)

	def test__toggle_visible__toggles_modulo(self):
		viz = Visibility((32, 32))
		viz.toggle_visible((32, 0), 1)
		self.assertEqual(viz.is_visible((0, 0), 1), True)

	def test__set_visible__sets(self):
		viz = Visibility((32, 32))
		self.assertEqual(viz.is_visible((0, 0), 1), False)
		viz.set_visible((0, 0), 1)
		self.assertEqual(viz.is_visible((0, 0), 1), True)

	def test__set_invisible__sets(self):
		viz = Visibility((32, 32))
		viz.set_visible((0, 0), 1)
		self.assertEqual(viz.is_visible((0, 0), 1), True)
		viz.set_invisible((0, 0), 1)
		self.assertEqual(viz.is_visible((0, 0), 1), False)

	def test__visible_matrix__correct(self):
		viz = Visibility((32, 32))
		viz.set_visible((0, 0), 1)
		viz.set_visible((1, 1), 2)
		visible1 = viz.visible_matrix(1)
		self.assertEqual(visible1[0][0], 1)
		self.assertEqual(visible1[1][1], 0)
		visible2 = viz.visible_matrix(2)
		self.assertEqual(visible2[0][0], 0)
		self.assertEqual(visible2[1][1], 1)

	def test__visibility_subset_explored(self):
		viz = Visibility((32, 32))
		viz.set_visible((0, 0), 1)
		self.assertEqual(viz.is_visible((0, 0), 1), True)
		self.assertEqual(viz.is_explored((0, 0), 1), True)

if __name__ == "__main__":
	unittest.main()
