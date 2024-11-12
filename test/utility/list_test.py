import unittest

from src.utility.list import next_index_with_item, prev_index_with_item

class TestListUtilityFunctions(unittest.TestCase):

	def test__next_index_with_item__found(self):
		items = [1, 2, 3, 4, 2, 5]
		self.assertEqual(next_index_with_item(items, 2, 0), 1)
		self.assertEqual(next_index_with_item(items, 2, 2), 4)
		self.assertEqual(next_index_with_item(items, 5, 0), 5)

	def test__next_index_with_item__string(self):
		text = 'It was the best of times, it was the worst of times.'
		self.assertEqual(next_index_with_item(text, ' ', 13), 15)

	def test__next_index_with_item__not_found(self):
		items = [1, 2, 3, 4, 2, 5]
		self.assertEqual(next_index_with_item(items, 6, 0), -1)
		self.assertEqual(next_index_with_item([], 1, 0), -1)

	def test__prev_index_with_item__found(self):
		items = [1, 2, 3, 4, 2, 5]
		self.assertEqual(prev_index_with_item(items, 2, 5), 4)
		self.assertEqual(prev_index_with_item(items, 2, 4), 1)
		self.assertEqual(prev_index_with_item(items, 1, 5), 0)

	def test__prev_index_with_item__string(self):
		text = 'It was the best of times, it was the worst of times.'
		self.assertEqual(prev_index_with_item(text, ' ', 13), 10)

	def test__prev_index_with_item__not_found(self):
		items = [1, 2, 3, 4, 2, 5]
		self.assertEqual(prev_index_with_item(items, 6, 5), -1)
		self.assertEqual(prev_index_with_item([], 1, 0), -1)

if __name__ == '__main__':
	unittest.main()
