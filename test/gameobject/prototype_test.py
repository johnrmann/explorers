import unittest

from src.gameobject.prototype import GameObjectPrototype

class GameObjectPrototypeTest(unittest.TestCase):
	"""
	Tests for the GameObjectPrototype class.
	"""

	def test__init__requires_name(self):
		"""
		When we create a GameObjectPrototype, we must provide a name.
		"""
		with self.assertRaises(ValueError):
			GameObjectPrototype()


	def test__init__sets_name(self):
		"""
		When we create a GameObjectPrototype, we should set the name.
		"""
		prototype = GameObjectPrototype(name="Test Object")
		self.assertEqual(prototype.name, "Test Object")


	def test__init__sets_preview_image(self):
		"""
		When we create a GameObjectPrototype, we should set the preview image.
		"""
		prototype = GameObjectPrototype(
			name="Test Object",
			preview_image="test.png"
		)
		self.assertEqual(prototype.preview_image, "test.png")


if __name__ == '__main__':
	unittest.main()
