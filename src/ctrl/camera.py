import pygame

from src.math.direction import Direction

def pygame_key_to_delta_zoom(key):
	"""
	Converts a key press to whether we should zoom in or zoom out.
	"""
	if key == pygame.K_KP_PLUS or key == pygame.K_EQUALS:
		return 1
	elif key == pygame.K_KP_MINUS or key == pygame.K_MINUS:
		return -1
	return 0

def pygame_key_to_delta_camera_rotate(key):
	if key == pygame.K_LEFTBRACKET:
		return -1
	elif key == pygame.K_RIGHTBRACKET:
		return 1
	return 0

def pygame_key_to_camdir(key):
	"""
	Converts a key press to which direction the camera should move.
	"""
	if key == pygame.K_UP:
		return Direction.NORTHWEST
	elif key == pygame.K_DOWN:
		return Direction.SOUTHEAST
	elif key == pygame.K_RIGHT:
		return Direction.NORTHEAST
	elif key == pygame.K_LEFT:
		return Direction.SOUTHWEST
	return None
