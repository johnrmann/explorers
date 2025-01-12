"""
A Prototype is a blueprint for a GameObject. It's used for the catalog when
creating and placing new GameObjects.
"""

class GameObjectPrototype:
	"""See module docs."""

	# A name for objects of this prototype. Example names could be "Palm Tree"
	# or "Habitation Module." This is required.
	name: str

	# A path to an image that represents the object. For use in the catalog.
	# This is optional.
	preview_image: str

	def __init__(self, name = None, preview_image = None):
		if name is None:
			raise ValueError("Expected name!")
		self.name = name
		self.preview_image = preview_image
