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
	_is_set_up = False

	def __init__(self, origin=None, parent=None):
		super().__init__(parent=parent)
		self.relative_origin = origin

	@property
	def origin(self):
		return self.relative_origin

	def update(self, dt: float):
		super().update(dt)
		if self._is_set_up:
			return
		h = 0
		for child in self.elements:
			_, child_h = child.dimensions
			child.translate(0, h)
			h += child_h
		self._is_set_up = True

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
	_is_set_up = False

	def __init__(self, origin=None, parent=None):
		super().__init__(parent=parent)
		self.relative_origin = origin

	@property
	def origin(self):
		return self.relative_origin

	def update(self, dt: float):
		super().update(dt)
		if self._is_set_up:
			return
		w = 0
		for child in self.elements:
			child_w, _ = child.dimensions
			child.translate(w, 0)
			w += child_w
		self._is_set_up = True

	def process_event(self, event):
		"""Returns true if the event was for this controller."""
		for elem in self.elements:
			if elem.process_event(event):
				return True
