import unittest

from src.gui.anchor import (
	Anchor,
	is_top_anchor,
	is_bottom_anchor,
	is_left_anchor,
	is_right_anchor,
	is_center_x_anchor,
	is_center_y_anchor,
	origin_via_anchor
)

class TestAnchor(unittest.TestCase):

	def test__is_top_anchor__true(self):
		self.assertTrue(is_top_anchor(Anchor.TOP_LEFT))
		self.assertTrue(is_top_anchor(Anchor.TOP_RIGHT))
		self.assertTrue(is_top_anchor(Anchor.TOP_CENTER))

	def test__is_top_anchor__false(self):
		self.assertFalse(is_top_anchor(Anchor.BOTTOM_LEFT))
		self.assertFalse(is_top_anchor(Anchor.CENTER))

	def test__is_bottom_anchor__true(self):
		self.assertTrue(is_bottom_anchor(Anchor.BOTTOM_LEFT))
		self.assertTrue(is_bottom_anchor(Anchor.BOTTOM_RIGHT))
		self.assertTrue(is_bottom_anchor(Anchor.BOTTOM_CENTER))

	def test__is_bottom_anchor__false(self):
		self.assertFalse(is_bottom_anchor(Anchor.TOP_LEFT))
		self.assertFalse(is_bottom_anchor(Anchor.CENTER))

	def test__is_left_anchor__true(self):
		self.assertTrue(is_left_anchor(Anchor.TOP_LEFT))
		self.assertTrue(is_left_anchor(Anchor.BOTTOM_LEFT))
		self.assertTrue(is_left_anchor(Anchor.LEFT_CENTER))

	def test__is_left_anchor__false(self):
		self.assertFalse(is_left_anchor(Anchor.TOP_RIGHT))
		self.assertFalse(is_left_anchor(Anchor.CENTER))

	def test__is_right_anchor__true(self):
		self.assertTrue(is_right_anchor(Anchor.TOP_RIGHT))
		self.assertTrue(is_right_anchor(Anchor.BOTTOM_RIGHT))
		self.assertTrue(is_right_anchor(Anchor.RIGHT_CENTER))

	def test__is_right_anchor__false(self):
		self.assertFalse(is_right_anchor(Anchor.TOP_LEFT))
		self.assertFalse(is_right_anchor(Anchor.CENTER))

	def test__is_center_x_anchor__true(self):
		self.assertTrue(is_center_x_anchor(Anchor.CENTER))
		self.assertTrue(is_center_x_anchor(Anchor.TOP_CENTER))
		self.assertTrue(is_center_x_anchor(Anchor.BOTTOM_CENTER))

	def test__is_center_x_anchor__false(self):
		self.assertFalse(is_center_x_anchor(Anchor.TOP_LEFT))
		self.assertFalse(is_center_x_anchor(Anchor.LEFT_CENTER))

	def test__is_center_y_anchor__true(self):
		self.assertTrue(is_center_y_anchor(Anchor.CENTER))
		self.assertTrue(is_center_y_anchor(Anchor.LEFT_CENTER))
		self.assertTrue(is_center_y_anchor(Anchor.RIGHT_CENTER))

	def test__is_center_y_anchor__false(self):
		self.assertFalse(is_center_y_anchor(Anchor.TOP_LEFT))
		self.assertFalse(is_center_y_anchor(Anchor.TOP_CENTER))

	def test__origin_via_anchor__top_left(self):
		self.assertEqual(
			origin_via_anchor((0, 0), (10, 10), (100, 100), Anchor.TOP_LEFT),
			(0, 0)
		)

	def test__origin_via_anchor__top_right(self):
		self.assertEqual(
			origin_via_anchor((0, 0), (10, 10), (50, 50), Anchor.TOP_RIGHT),
			(40, 0)
		)

	def test__origin_via_anchor__bottom_right(self):
		self.assertEqual(
			origin_via_anchor((0, 0), (10, 10), (50, 50), Anchor.BOTTOM_RIGHT),
			(40, 40)
		)

	def test__origin_via_anchor__bottom_right_with_parent(self):
		self.assertEqual(
			origin_via_anchor(
				(0, 0),
				(10, 10),
				(50, 50),
				Anchor.BOTTOM_RIGHT,
				parent_origin=(100, 100)
			),
			(140, 140)
		)

	def test__origin_via_anchor__bottom_left(self):
		self.assertEqual(
			origin_via_anchor((0, 0), (10, 10), (100, 100), Anchor.BOTTOM_LEFT),
			(0, 90)
		)

	def test__origin_via_anchor__center(self):
		self.assertEqual(
			origin_via_anchor((0, 0), (10, 10), (100, 100), Anchor.CENTER),
			(45, 45)
		)

	def test__origin_via_anchor__center_left(self):
		self.assertEqual(
			origin_via_anchor((0, 0), (10, 10), (100, 100), Anchor.LEFT_CENTER),
			(0, 45)
		)

	def test__origin_via_anchor__center_right(self):
		self.assertEqual(
			origin_via_anchor((0, 0), (10, 10), (100, 100), Anchor.RIGHT_CENTER),
			(90, 45)
		)

	def test__origin_via_anchor__center_top(self):
		self.assertEqual(
			origin_via_anchor((0, 0), (10, 10), (100, 100), Anchor.TOP_CENTER),
			(45, 0)
		)

	def test__origin_via_anchor__center_bottom(self):
		self.assertEqual(
			origin_via_anchor((0, 0), (10, 10), (50, 50), Anchor.BOTTOM_CENTER),
			(20, 40)
		)

if __name__ == '__main__':
	unittest.main()
