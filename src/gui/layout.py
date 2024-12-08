"""
These classes automatically lay out elements in a vertical or horizontal line.
"""

from src.gui.gui import GuiElement

class VerticalLayout(GuiElement):
	"""
	Automatically lays out its children top to bottom.
	"""

	_height = 0
	_width = 0

	def __init__(self, origin=None, parent=None):
		self.relative_origin = origin
		super().__init__(parent=parent)

	def add_child(self, child):
		super().add_child(child)
		ox, oy = child.relative_origin
		child.relative_origin = (ox, oy + self._height)
		self._height += child.dimensions[1]

	def process_event(self, event):
		"""Returns true if the event was for this controller."""
		for elem in self.elements:
			if elem.process_event(event):
				return True

class HorizontalLayout(GuiElement):
	"""
	Automatically lays out its children left to right.
	"""

	_height = 0
	_width = 0

	def __init__(self, origin=None, parent=None):
		self.relative_origin = origin
		super().__init__(parent=parent)

	def add_child(self, child):
		super().add_child(child)
		ox, oy = child.relative_origin
		child.relative_origin = (ox + self._width, oy)
		self._width += child.dimensions[0]

	def process_event(self, event):
		"""Returns true if the event was for this controller."""
		for elem in self.elements:
			if elem.process_event(event):
				return True
