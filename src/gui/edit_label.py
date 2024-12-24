from src.gui.gui import GuiElement
from src.gui.primitives import Label, Button

class EditLabel(GuiElement):
	"""
	A label that can possibly be edited.
	"""

	_is_editable: bool = True

	_label: Label = None
	_button: Button = None

	def __init__(self, is_editable=True, on_edit=None, text='', **kwargs):
		super().__init__(**kwargs)
		width, height = self.dimensions
		self._is_editable = is_editable
		self._label = Label(
			text=text,
			origin=(0, 0),
			dimensions=(width - height, height),
			parent=self,
		)
		self._button = Button(
			text='Edit',
			origin=(width - height, 0),
			dimensions=(height, height),
			parent=self,
			callback=on_edit,
			hidden=not is_editable,
		)

	@property
	def text(self):
		"""
		The text of the label.
		"""
		return self._label.text

	@text.setter
	def text(self, value):
		self._label.text = value

	@property
	def is_editable(self):
		"""
		Hide the edit button if the edit label is not editable.
		"""
		return self._is_editable

	@is_editable.setter
	def is_editable(self, value):
		self._is_editable = value
		self._button.hidden = not value
