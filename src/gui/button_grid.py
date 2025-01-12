from dataclasses import dataclass

from src.gui.primitives import Button, ImageButton
from src.gui.gui import GuiElement


class ButtonGridItem:
	"""An item in the button grid."""
	uid: int
	payload = None

	def __init__(self, uid: int, payload=None):
		self.uid = uid
		self.payload = payload


	def __hash__(self):
		return hash(self.uid)



@dataclass
class ButtonGridSpacing:
	"""
	This class is used to calculate the spacing of buttons in a grid.
	"""

	button_dimensions: tuple[int, int]
	button_margin: int = 0

	def buttons_per_row(self, container_width: int) -> int:
		"""
		Calculate the number of buttons that can fit in a row.
		"""
		button_width, _ = self.button_dimensions
		return container_width // (button_width + self.button_margin)

	def buttons_per_column(self, container_height: int) -> int:
		"""
		Calculate the number of buttons that can fit in a column.
		"""
		_, button_height = self.button_dimensions
		return container_height // (button_height + self.button_margin)

	def buttons_per_grid(self, dimensions: tuple[int, int]) -> int:
		"""
		Calculate the number of buttons that can fit in a grid.
		"""
		width, height = dimensions
		return self.buttons_per_row(width) * self.buttons_per_column(height)

	def button_coordinates(
			self,
			n: int,
			dimensions: tuple[int, int]
	) -> tuple[int, int]:
		"""
		Generate the coordinates for a grid of buttons.
		"""

		per_row = self.buttons_per_row(dimensions[0])
		per_grid = self.buttons_per_grid(dimensions)
		if n >= per_grid:
			raise ValueError(
				f"Button index {n} is out of range for grid size {dimensions}"
			)
		x = (n % per_row) * (self.button_dimensions[0] + self.button_margin)
		y = (n // per_row) * (self.button_dimensions[1] + self.button_margin)
		return x, y



class _ButtonGrid(GuiElement):
	"""
	A grid of buttons.
	"""

	_spacing: ButtonGridSpacing = None
	_items: list[ButtonGridItem] = None
	_buttons: dict[ButtonGridItem, Button] = None
	_button_callbacks: dict[ButtonGridItem, callable] = None
	_callback: callable = None

	def __init__(
			self,
			spacing: ButtonGridSpacing = None,
			callback: callable = None,
			items: list[ButtonGridItem] = None,
			**kwargs
	):
		if items is None:
			items = []
		if callback is None:
			raise ValueError("Need a callback.")
		if spacing is None:
			raise ValueError("Need a spacing object.")
		super().__init__(**kwargs)
		self._spacing = spacing
		self._callback = callback
		self._items = items
		self._make_buttons(items)


	def _make_buttons(self, items: list[ButtonGridItem]):
		"""Create buttons for each item."""
		self._make_callbacks(items)
		self._buttons = {}
		for item in items:
			callback = self._button_callbacks[item]
			button = self.button_for_item_and_callback(item, callback)
			self._buttons[item] = button


	def _make_callbacks(self, items: list[ButtonGridItem]):
		"""Create callbacks for each item."""
		self._button_callbacks = {}
		for item in items:
			self._button_callbacks[item] = self._callback_for_item(item.payload)


	def _callback_for_item(self, item: ButtonGridItem) -> callable:
		return lambda: self._callback(item)


	def button_for_item_and_callback(
			self,
			item: ButtonGridItem,
			button_cb
	) -> Button:
		"""This abstract class takes in a button item and callback, and creates
		a button for it."""
		raise NotImplementedError()



class ImageButtonGridItem(ButtonGridItem):
	"""An item in the image button grid."""
	image_path: str = None

	def __init__(self, uid: int, image_path: str, payload=None):
		super().__init__(uid, payload)
		self.image_path = image_path


	@staticmethod
	def from_pairs(texts_and_payloads: list[tuple[str, any]]) -> list:
		"""Create a list of TextButtonGridItems from a list of text strings."""
		items = []
		for i, (text, payload) in enumerate(texts_and_payloads):
			items.append(ImageButtonGridItem(i, text, payload))
		return items



class ImageButtonGrid(_ButtonGrid):
	"""A grid of image buttons."""

	def button_for_item_and_callback(self, item, button_cb):
		if not isinstance(item, ImageButtonGridItem):
			raise ValueError("Item is not an ImageButtonGridItem.")
		origin = self._spacing.button_coordinates(item.uid, self.dimensions)
		button_dimensions = self._spacing.button_dimensions
		return ImageButton(
			origin=origin,
			dimensions=button_dimensions,
			image_path=item.image_path,
			callback=button_cb,
			parent=self,
		)



class TextButtonGridItem(ButtonGridItem):
	"""An item in the text button grid."""
	text: str = None

	def __init__(self, uid: int, text: str, payload=None):
		super().__init__(uid, payload)
		self.text = text


	@staticmethod
	def from_pairs(texts_and_payloads: list[tuple[str, any]]) -> list:
		"""Create a list of TextButtonGridItems from a list of text strings."""
		items = []
		for i, (text, payload) in enumerate(texts_and_payloads):
			items.append(TextButtonGridItem(i, text, payload))
		return items



class TextButtonGrid(_ButtonGrid):
	"""A grid of text buttons."""

	def button_for_item_and_callback(self, item, button_cb):
		if not isinstance(item, TextButtonGridItem):
			raise ValueError("Item is not a TextButtonGridItem.")
		origin = self._spacing.button_coordinates(item.uid, self.dimensions)
		button_dimensions = self._spacing.button_dimensions
		return Button(
			origin=origin,
			dimensions=button_dimensions,
			text=item.text,
			callback=button_cb,
			parent=self,
		)
