import pygame
import unittest

from src.render.utils import (
	scale_color,
	alpha_mask_from_surface,
	resize_surface,
	relight_surface
)

class UtilsTest(unittest.TestCase):
	def test__scale_color__three_channels(self):
		color = (255, 0, 0)
		scale = 0.5

		result = scale_color(color, scale)
		expected_color = (128, 0, 0)

		self.assertEqual(result, expected_color)

	def test__scale_color__four_channels(self):
		color = (255, 0, 0, 255)
		scale = 0.5

		result = scale_color(color, scale)
		expected_color = (128, 0, 0, 255)

		self.assertEqual(result, expected_color	)

	def test__scale_color__rejects_invalid(self):
		bad = (4, 8)
		with self.assertRaises(ValueError):
			scale_color(bad, 0.5)

	def test__alpha_mask_from_surface__valid_fill_color(self):
		pygame.init()
		surface = pygame.Surface((2, 2), pygame.SRCALPHA)
		surface.fill((255, 0, 0, 128))  # Semi-transparent red
		fill_color = (255, 0, 0, 255)  # Opaque red

		result = alpha_mask_from_surface(surface, fill_color)
		expected_color = (255, 0, 0, 255)

		for x in range(result.get_width()):
			for y in range(result.get_height()):
				self.assertEqual(result.get_at((x, y)), expected_color)

	def test__alpha_mask_from_surface__valid_fill_color_default(self):
		pygame.init()
		surface = pygame.Surface((2, 2), pygame.SRCALPHA)
		surface.fill((255, 0, 0, 128))

		result = alpha_mask_from_surface(surface)
		expected_color = (255, 255, 255, 255)

		for x in range(result.get_width()):
			for y in range(result.get_height()):
				self.assertEqual(result.get_at((x, y)), expected_color)

	def test__alpha_mask_from_surface__partial_fill(self):
		"""
		Creates an 8x8 image with a transparent border and a red 6x6 center.
		"""
		pygame.init()
		surface = pygame.Surface((8, 8), pygame.SRCALPHA)
		surface.fill((0, 0, 0, 0))
		for x in range(1, 7):
			for y in range(1, 7):
				surface.set_at((x, y), (255, 0, 0, 255))

		result = alpha_mask_from_surface(surface)
		expected_color = (255, 255, 255, 255)

		for x in range(result.get_width()):
			for y in range(result.get_height()):
				if 1 <= x <= 6 and 1 <= y <= 6:
					self.assertEqual(result.get_at((x, y)), expected_color)
				else:
					self.assertEqual(result.get_at((x, y)), (0, 0, 0, 0))

	def test__alpha_mask_from_surface__invalid_fill_color_length(self):
		pygame.init()
		surface = pygame.Surface((2, 2), pygame.SRCALPHA)
		fill_color = (255, 255, 255)

		with self.assertRaises(ValueError) as context:
			alpha_mask_from_surface(surface, fill_color)
		self.assertEqual(
			str(context.exception),
			"Fill color must be a 4-tuple."
		)

	def test__alpha_mask_from_surface__non_opaque_fill_color(self):
		pygame.init()
		surface = pygame.Surface((2, 2), pygame.SRCALPHA)
		fill_color = (255, 255, 255, 128)

		with self.assertRaises(ValueError) as context:
			alpha_mask_from_surface(surface, fill_color)
		self.assertEqual(
			str(context.exception),
			"Fill color must be opaque."
		)

	def test__resize_surface__sizes_down(self):
		pygame.init()
		surface = pygame.Surface((2, 2), pygame.SRCALPHA)
		surface.fill((255, 0, 0, 255))

		result = resize_surface(surface, 0.5)
		expected_size = (1, 1)

		self.assertEqual(result.get_size(), expected_size)

	def test__resize_surface__sizes_up(self):
		pygame.init()
		surface = pygame.Surface((2, 2), pygame.SRCALPHA)
		surface.fill((255, 0, 0, 255))

		result = resize_surface(surface, 2)
		expected_size = (4, 4)

		self.assertEqual(result.get_size(), expected_size)

	def test__relight_surface__works(self):
		pygame.init()
		surface = pygame.Surface((2, 2), pygame.SRCALPHA)
		surface.fill((255, 0, 0, 255))

		result = relight_surface(surface, 0.5)
		expected_color = (128, 0, 0, 255)

		for x in range(result.get_width()):
			for y in range(result.get_height()):
				self.assertEqual(result.get_at((x, y)), expected_color)

if __name__ == "__main__":
	unittest.main()
