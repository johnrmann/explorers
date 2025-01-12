import unittest

import pygame
import os
import sys

# Ensure the current working directory is added to sys.path
sys.path.insert(0, os.getcwd())

def global_setup():
	os.environ['SDL_VIDEODRIVER'] = 'dummy'
	pygame.init()
	pygame.display.set_mode((800, 600))
	print("Pygame initialized without a window.")

def load_tests():
	return unittest.defaultTestLoader.discover(
		start_dir='.',
		pattern='*_test.py'
	)

if __name__ == '__main__':
	global_setup()
	suite = unittest.TestSuite(load_tests())
	unittest.TextTestRunner().run(suite)
	pygame.quit()
