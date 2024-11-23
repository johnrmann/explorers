import unittest

from src.path.path_runner import PathRunner

from src.math.direction import Direction
from src.math.vector2 import Vector2

BASIC_PATH = [
	Vector2(0,0),
	Vector2(1,0),
	Vector2(1,1)
]

class PathRunnerTest(unittest.TestCase):
	def test__position(self):
		runner = PathRunner(position=Vector2(4,8))
		self.assertEqual(runner.position, Vector2(4,8))

	def test__position__interpolates(self):
		runner = PathRunner(path=BASIC_PATH)
		self.assertEqual(runner.position, Vector2(0,0))
		runner.tick(0.25)
		self.assertEqual(runner.position, Vector2(0, 0))
		runner.tick(0.5)
		self.assertEqual(runner.position, Vector2(1, 0))
		runner.tick(0.25)
		self.assertEqual(runner.position, Vector2(1, 0))
		runner.tick(0.55)
		self.assertEqual(runner.position, Vector2(1, 1))
	
	def test__draw_position__still(self):
		runner = PathRunner(position=Vector2(4,8))
		self.assertEqual(runner.draw_position, Vector2(4,8))
	
	def test__draw_position__interpolates(self):
		runner = PathRunner(path=BASIC_PATH)
		self.assertEqual(runner.draw_position, Vector2(0,0))
		runner.tick(0.25)
		self.assertEqual(runner.draw_position, Vector2(0.25, 0))
		runner.tick(0.5)
		self.assertEqual(runner.draw_position, Vector2(0.75, 0))
		runner.tick(0.25)
		self.assertEqual(runner.draw_position, Vector2(1, 0))
		runner.tick(0.50)
		self.assertEqual(runner.draw_position, Vector2(1, 0.5))

	def test__is_moving__still(self):
		runner = PathRunner()
		self.assertFalse(runner.is_moving)
	
	def test__is_moving__moving(self):
		runner = PathRunner(path = BASIC_PATH)
		self.assertTrue(runner.is_moving)
	
	def test__is_moving__stopped(self):
		runner = PathRunner(path = BASIC_PATH)
		runner.tick(0.5)
		self.assertTrue(runner.is_moving)
		runner.tick(0.5)
		self.assertTrue(runner.is_moving)
		runner.tick(0.5)
		self.assertTrue(runner.is_moving)
		runner.tick(0.5)
		self.assertFalse(runner.is_moving)
	
	def test__direction__default(self):
		runner = PathRunner()
		self.assertEqual(runner.direction, Direction.SOUTH)
		runner2 = PathRunner(direction=Direction.SOUTHEAST)
		self.assertEqual(runner2.direction, Direction.SOUTHEAST)
	
	def test__direction__when_moving(self):
		runner = PathRunner(path = BASIC_PATH, direction=Direction.NORTH)
		self.assertEqual(runner.direction, Direction.EAST)
		runner.tick(0.5)
		self.assertEqual(runner.direction, Direction.EAST)
		runner.tick(0.5)
		self.assertEqual(runner.direction, Direction.SOUTH)
		runner.tick(0.5)
		self.assertEqual(runner.direction, Direction.SOUTH)
		runner.tick(0.5)
		self.assertEqual(runner.direction, Direction.SOUTH)

	def test__tick__calls_on_done(self):
		callback_called = False
		def on_done():
			nonlocal callback_called
			callback_called = True

		runner = PathRunner(path=BASIC_PATH, on_done=on_done)
		runner.tick(0.5)
		runner.tick(0.5)
		runner.tick(0.5)
		runner.tick(0.5)
		runner.tick(0.5)
		self.assertTrue(callback_called)
		self.assertEqual(runner.position, Vector2(1, 1))
		self.assertFalse(runner.is_moving)

if __name__ == "__main__":
	unittest.main()
