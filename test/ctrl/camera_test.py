import unittest
import pygame

from src.math.direction import Direction
from src.ctrl.camera import (
	pygame_key_to_delta_zoom,
	pygame_key_to_delta_camera_rotate,
	pygame_key_to_camdir,
)

class CameraTest(unittest.TestCase):
	def test__pygame_key_to_delta_zoom__zoom_in(self):
		self.assertEqual(pygame_key_to_delta_zoom(pygame.K_KP_PLUS), 1)
		self.assertEqual(pygame_key_to_delta_zoom(pygame.K_PLUS), 1)

	def test__pygame_key_to_delta_zoom__zoom_out(self):
		self.assertEqual(pygame_key_to_delta_zoom(pygame.K_KP_MINUS), -1)
		self.assertEqual(pygame_key_to_delta_zoom(pygame.K_MINUS), -1)

	def test__pygame_key_to_delta_zoom__no_zoom(self):
		self.assertEqual(pygame_key_to_delta_zoom(pygame.K_a), 0)
		self.assertEqual(pygame_key_to_delta_zoom(pygame.K_SPACE), 0)

	def test__pygame_key_to_delta_camera_rotate__rotates(self):
		self.assertEqual(
			pygame_key_to_delta_camera_rotate(pygame.K_LEFTBRACKET), -1
		)
		self.assertEqual(
			pygame_key_to_delta_camera_rotate(pygame.K_RIGHTBRACKET), 1
		)

	def test__pygame_key_to_delta_camera_rotate__no_rotate(self):
		self.assertEqual(pygame_key_to_delta_camera_rotate(pygame.K_a), 0)
		self.assertEqual(pygame_key_to_delta_camera_rotate(pygame.K_SPACE), 0)

	def test__pygame_key_to_camdir__arrow_keys(self):
		self.assertEqual(
			pygame_key_to_camdir(pygame.K_UP), Direction.NORTHWEST
		)
		self.assertEqual(
			pygame_key_to_camdir(pygame.K_DOWN), Direction.SOUTHEAST
		)
		self.assertEqual(
			pygame_key_to_camdir(pygame.K_RIGHT), Direction.NORTHEAST
		)
		self.assertEqual(
			pygame_key_to_camdir(pygame.K_LEFT), Direction.SOUTHWEST
		)

	def test__pygame_key_to_camdir__no_movement(self):
		self.assertIsNone(pygame_key_to_camdir(pygame.K_a))
		self.assertIsNone(pygame_key_to_camdir(pygame.K_SPACE))


if __name__ == "__main__":
	unittest.main()
