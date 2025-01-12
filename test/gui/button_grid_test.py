import unittest

from src.gui.button_grid import (
	ButtonGridItem,
	TextButtonGridItem,
	ImageButtonGridItem,
	ButtonGridSpacing,
)

class ButtonGridItemTest(unittest.TestCase):
	def test__init__sets_uid(self):
		item = ButtonGridItem(uid=1)
		self.assertEqual(item.uid, 1)


	def test__hash__by_uid(self):
		item = ButtonGridItem(uid=1)
		self.assertEqual(hash(item), hash(1))


class TextButtonGridItemTest(unittest.TestCase):
	def test__init__sets_text(self):
		item = TextButtonGridItem(uid=1, text="Test")
		self.assertEqual(item.text, "Test")


	def test__from_pairs__sets_pairs(self):
		pairs = [
			("Alice", "alpha"),
			("Bob", "bravo"),
			("Charlie", "charlie")
		]
		items = TextButtonGridItem.from_pairs(pairs)
		self.assertEqual(len(items), 3)
		self.assertEqual(items[0].text, "Alice")
		self.assertEqual(items[1].text, "Bob")
		self.assertEqual(items[2].text, "Charlie")
		self.assertEqual(items[0].payload, "alpha")
		self.assertEqual(items[1].payload, "bravo")
		self.assertEqual(items[2].payload, "charlie")


	def test__from_pairs__sets_uids(self):
		pairs = [
			("Alice", "alpha"),
			("Bob", "bravo"),
			("Charlie", "charlie")
		]
		items = TextButtonGridItem.from_pairs(pairs)
		self.assertEqual(items[0].uid, 0)
		self.assertEqual(items[1].uid, 1)
		self.assertEqual(items[2].uid, 2)


class ImageButtonGridItemTest(unittest.TestCase):
	def test__init__sets_image_path(self):
		item = ImageButtonGridItem(uid=1, image_path="test.png")
		self.assertEqual(item.image_path, "test.png")


	def test__from_pairs__sets_pairs(self):
		pairs = [
			("Alice", "alpha.png"),
			("Bob", "bravo.png"),
			("Charlie", "charlie.png")
		]
		items = ImageButtonGridItem.from_pairs(pairs)
		self.assertEqual(len(items), 3)
		self.assertEqual(items[0].image_path, "Alice")
		self.assertEqual(items[1].image_path, "Bob")
		self.assertEqual(items[2].image_path, "Charlie")
		self.assertEqual(items[0].payload, "alpha.png")
		self.assertEqual(items[1].payload, "bravo.png")
		self.assertEqual(items[2].payload, "charlie.png")


	def test__from_pairs__sets_uids(self):
		pairs = [
			("Alice", "alpha"),
			("Bob", "bravo"),
			("Charlie", "charlie")
		]
		items = ImageButtonGridItem.from_pairs(pairs)
		self.assertEqual(items[0].uid, 0)
		self.assertEqual(items[1].uid, 1)
		self.assertEqual(items[2].uid, 2)


class ButtonGridSpacingTest(unittest.TestCase):
	def test__buttons_per_row__no_margin(self):
		spacing = ButtonGridSpacing(
			button_dimensions=(10, 10),
			button_margin=0
		)
		self.assertEqual(spacing.buttons_per_row(100), 10)


	def test__buttons_per_row__with_margin(self):
		spacing = ButtonGridSpacing(
			button_dimensions=(10, 10),
			button_margin=1
		)
		self.assertEqual(spacing.buttons_per_row(100), 9)


	def test__buttons_per_column__no_margin(self):
		spacing = ButtonGridSpacing(button_dimensions=(10, 10), button_margin=0)
		self.assertEqual(spacing.buttons_per_column(100), 10)


	def test__buttons_per_column__with_margin(self):
		spacing = ButtonGridSpacing(button_dimensions=(10, 10), button_margin=1)
		self.assertEqual(spacing.buttons_per_column(100), 9)


	def test__buttons_per_grid__no_margin(self):
		spacing = ButtonGridSpacing(button_dimensions=(10, 10), button_margin=0)
		self.assertEqual(spacing.buttons_per_grid((100, 100)), 100)


	def test__buttons_per_grid__with_margin(self):
		spacing = ButtonGridSpacing(button_dimensions=(10, 10), button_margin=1)
		self.assertEqual(spacing.buttons_per_grid((100, 100)), 81)


	def test__button_coordinates__no_margin_origin(self):
		spacing = ButtonGridSpacing(button_dimensions=(10, 10), button_margin=0)
		self.assertEqual(spacing.button_coordinates(0, (100, 100)), (0, 0))


	def test__button_coordinates__no_margin_second_column(self):
		spacing = ButtonGridSpacing(button_dimensions=(10, 10), button_margin=0)
		self.assertEqual(spacing.button_coordinates(1, (100, 100)), (10, 0))


	def test__button_coordinates__no_margin_second_row(self):
		spacing = ButtonGridSpacing(button_dimensions=(10, 10), button_margin=0)
		self.assertEqual(spacing.button_coordinates(10, (100, 100)), (0, 10))


	def test__button_coordinates__no_margin_last(self):
		spacing = ButtonGridSpacing(button_dimensions=(10, 10), button_margin=0)
		self.assertEqual(spacing.button_coordinates(99, (100, 100)), (90, 90))


	def test__button_coordinates__out_of_bounds(self):
		spacing = ButtonGridSpacing(button_dimensions=(10, 10), button_margin=0)
		with self.assertRaises(ValueError):
			spacing.button_coordinates(100, (100, 100))


if __name__ == '__main__':
	unittest.main()
