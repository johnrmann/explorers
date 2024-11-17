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

	def add_child(self, child: GuiElement):
		return super().add_child(child)
