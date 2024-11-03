"""
TODO(jm) - very temporary.
"""

from src.gameobject.gameobject import GameObject

class Lander(GameObject):
	def __init__(self, pos=(0,0)):
		self.pos = pos
		self.size = (5, 5)
	
	def image_path(self):
		return "assets/img/lander.png"
