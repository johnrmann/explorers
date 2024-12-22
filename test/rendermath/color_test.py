import unittest

from src.rendermath.color import ensure_rgba

class ColorTest(unittest.TestCase):
	def test__ensure_rgba__3_tuple(self):
		self.assertEqual(ensure_rgba((255, 0, 0)), (255, 0, 0, 255))

	def test__ensure_rgba__3_tuple_default(self):
		self.assertEqual(
			ensure_rgba((255, 0, 0), default_a=100),
			(255, 0, 0, 100)
		)

	def test__ensure_rgba__4_tuple(self):
		self.assertEqual(ensure_rgba((255, 0, 0, 127)), (255, 0, 0, 127))

	def test__ensure_rgba__invalid_length(self):
		with self.assertRaises(ValueError):
			ensure_rgba((255, 0))

if __name__ == '__main__':
	unittest.main()
