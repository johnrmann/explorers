"""
Unit tests for the cube module.
"""

import unittest

from src.math.direction import Direction

from src.rendermath.box import Box, compare_boxes, are_boxes_overlapping

class CubeTest(unittest.TestCase):
	"""
	Note about the test names - they're named based on the second cube's
	relationship to the first. For example, "front left" means the second cube
	is in front of and to the left of the first.
	"""

	def setUp(self):
		self.unit = Box(p=(1,1,0), size=(1,1,1))

	def test__init__raises_value_error_when_origin_not_defined(self):
		"""
		__init__ should raise ValueError when origin is not defined.
		"""
		with self.assertRaises(ValueError):
			Box()

	def test__init__raises_value_error_when_both_q_and_size_are_none(self):
		"""
		__init__ should raise ValueError when both q and size are None.
		"""
		with self.assertRaises(ValueError):
			Box(p=(1, 1, 1))

	def test__init__raises_value_error_when_both_q_and_size_are_defined(self):
		"""
		__init__ should raise ValueError when both q and size are defined.
		"""
		with self.assertRaises(ValueError):
			Box(p=(1, 1, 1), q=(2, 2, 2), size=(1, 1, 1))

	def test__init__sets_correct_q_when_size_is_defined(self):
		"""
		__init__ should set the correct q when size is defined.
		"""
		box = Box(p=(1, 1, 1), size=(2, 2, 2))
		self.assertEqual(box.q, (3, 3, 3))

	def test__init__sets_correct_size_when_q_is_defined(self):
		"""
		__init__ should set the correct size when q is defined.
		"""
		box = Box(p=(1, 1, 1), q=(2, 2, 2))
		self.assertEqual(box.size, (1, 1, 1))

	def test__box__multicell__works_unit(self):
		"""
		Test 1x1x1 case.
		"""
		self.assertEqual(self.unit.multicell(), ((1,1), (1,1)))

	def test__box__multicell__works_big(self):
		"""
		Test 2x2x2 case.
		"""
		box = Box(p=(1, 1, 1), size=(2, 2, 2))
		self.assertEqual(box.multicell(), ((1,1), (2,2)))

	def test__compare_boxes__independent(self):
		"""
		So far apart draw order doesn't matter.
		"""
		c2 = Box(p=(9,9,0), size=(1,1,1))
		self.assertEqual(compare_boxes(self.unit, c2), 0)

	def test__compare_boxes__front_left(self):
		"""
		The second cube `c2` appears to be in front of and to the left of the
		first when rendered on the screen.
		"""
		c2 = Box(p=(1,2,0), size=(1,1,1))
		self.assertEqual(compare_boxes(self.unit, c2), 1)

	def test__compare_boxes__front_right(self):
		"""
		The second cube `c2` appears to be in front of and to the right of the
		first when rendered on the screen.
		"""
		c2 = Box(p=(1,2,0), size=(1,1,1))
		self.assertEqual(compare_boxes(self.unit, c2), 1)

	def test__compare_boxes__behind(self):
		"""
		The second cube is behind the first.
		"""
		c2 = Box(p=(0,0,0), size=(1,1,1))
		self.assertEqual(compare_boxes(self.unit, c2), -1)

	def test__compare_boxes__behind_southeast(self):
		"""
		The second cube is in front the first if the camera direction is
		opposite.
		"""
		c2 = Box(p=(0,0,0), size=(1,1,1))
		self.assertEqual(
			compare_boxes(self.unit, c2, cam_dir=Direction.SOUTHEAST),
			1
		)

	def test__compare_boxes__on_top(self):
		"""
		The second cube is on top of the first.
		"""
		c2 = Box(p=(1,1,1), size=(1,1,1))
		self.assertEqual(compare_boxes(self.unit, c2), 1)

	def test__compare_boxes__below(self):
		"""
		The second cube is below the first.
		"""
		c2 = Box(p=(1,1,1), size=(1,1,1))
		self.assertEqual(compare_boxes(c2, self.unit), -1)

	def test__are_boxes_overlapping__no_overlap(self):
		"""
		are_boxes_overlapping should return False when boxes do not overlap.
		"""
		box1 = Box(p=(1, 1, 0), size=(1, 1, 1))
		box2 = Box(p=(5, 5, 0), size=(1, 1, 1))
		self.assertFalse(
			are_boxes_overlapping(box1, box2, Direction.NORTHWEST, (48, 24))
		)

	def test__are_boxes_overlapping__overlap(self):
		"""
		are_boxes_overlapping should return True when boxes overlap.
		"""
		box1 = Box(p=(1, 1, 0), size=(2, 2, 2))
		box2 = Box(p=(2, 2, 0), size=(2, 2, 2))
		self.assertTrue(
			are_boxes_overlapping(box1, box2, Direction.NORTHWEST, (48, 24))
		)

	def test__are_boxes_overlapping__touching_edges(self):
		"""
		Ideally this should be False but it's not the end of the world if it's
		True.
		"""
		box1 = Box(p=(1, 1, 0), size=(1, 1, 1))
		box2 = Box(p=(2, 1, 0), size=(1, 1, 1))
		self.assertTrue(
			are_boxes_overlapping(box1, box2, Direction.NORTHWEST, (48, 24))
		)

	def test__are_boxes_overlapping__overlapping_with_different_cam_dir(self):
		"""
		are_boxes_overlapping should return True when boxes overlap with
		different camera direction.
		"""
		box1 = Box(p=(1, 1, 0), size=(2, 2, 2))
		box2 = Box(p=(2, 2, 0), size=(2, 2, 2))
		self.assertTrue(
			are_boxes_overlapping(box1, box2, Direction.SOUTHEAST, (48, 24))
		)

if __name__ == "__main__":
	unittest.main()
