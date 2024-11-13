"""
TODO(jm) - very temporary.
"""

from src.gameobject.interactable import Interactable

class Lander(Interactable):
	def __init__(self, pos=None):
		if pos is None:
			pos = (0,0)
		super().__init__(
			pos=pos,
			size=(5,5)
		)
	
	def image_path(self):
		return "assets/img/lander.png"
