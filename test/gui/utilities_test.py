import pygame

import unittest

from src.gui.utilities import bounding_box, create_gradient_surface
from src.gui.gui import GuiElement

class TestBoundingBox(unittest.TestCase):

	def test__bounding_box__single_element(self):
		elem = GuiElement(origin=(10, 10), dimensions=(5, 5))
		result = bounding_box([elem])
		self.assertEqual(result, ((10, 10), (5, 5)))

	def test__bounding_box__multiple_elements(self):
		elem1 = GuiElement(origin=(10, 10), dimensions=(5, 5))
		elem2 = GuiElement(origin=(20, 20), dimensions=(10, 10))
		result = bounding_box([elem1, elem2])
		self.assertEqual(result, ((10, 10), (20, 20)))

	def test__bounding_box__overlapping_elements(self):
		elem1 = GuiElement(origin=(10, 10), dimensions=(10, 10))
		elem2 = GuiElement(origin=(15, 15), dimensions=(10, 10))
		result = bounding_box([elem1, elem2])
		self.assertEqual(result, ((10, 10), (15, 15)))

	def test__bounding_box__no_elements(self):
		result = bounding_box([])
		self.assertEqual(result, ((0, 0), (0, 0)))

	def test__create_gradient_surface__single_color(self):
		height = 10
		start_color = (255, 0, 0, 255)
		end_color = (255, 0, 0, 255)
		surface = create_gradient_surface(height, start_color, end_color)
		for y in range(height):
			self.assertEqual(surface.get_at((0, y)), start_color)

	def test__create_gradient_surface__gradient(self):
		height = 11
		start_color = (0, 0, 0, 100)
		end_color = (100, 100, 100, 100)
		surface = create_gradient_surface(height, start_color, end_color)
		for y in range(height):
			expected_color = (y * 10, y * 10, y * 10, 100)
			self.assertEqual(surface.get_at((0, y)), expected_color)

	def test__create_gradient_surface__transparent_to_opaque(self):
		height = 11
		start_color = (255, 0, 0, 0)
		end_color = (255, 0, 0, 100)
		surface = create_gradient_surface(height, start_color, end_color)
		for y in range(height):
			expected_color = (
				255,
				0,
				0,
				y * 10
			)
			self.assertEqual(surface.get_at((0, y)), expected_color)

if __name__ == '__main__':
	unittest.main()
