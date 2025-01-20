"""
The Catalog class is a wrapper for ButtonGrid that shows GameObject prototypes,
and allows players to select them to place them in the game world.
"""

from src.gameobject.prototype import GameObjectPrototype

from src.gui.gui import GuiElement
from src.gui.button_grid import (
	ImageButtonGridItem,
	ImageButtonGrid,
	ButtonGridSpacing
)



class Catalog(GuiElement):
	"""
	See module-level docs.
	"""

	_grid_items: list[ImageButtonGridItem]
	_button_grid: ImageButtonGrid

	_last_selected: GameObjectPrototype = None

	def __init__(
			self,
			prototypes: list[GameObjectPrototype] = None,
			on_select: callable = None,
			on_deselect: callable = None,
			spacing: ButtonGridSpacing = None,
			parent = None,
			**kwargs
	):
		super().__init__(parent=parent, **kwargs)
		self._grid_items = [
			ImageButtonGridItem(idx, prototype.preview_image, payload=prototype)
			for idx, prototype in enumerate(prototypes)
		]
		self._on_select = on_select
		self._on_deselect = on_deselect

		if spacing is None:
			spacing = ButtonGridSpacing(
				button_dimensions=(50, 50),
				button_margin=5
			)

		self._button_grid = ImageButtonGrid(
			items=self._grid_items,
			callback=self.on_click_button,
			spacing=spacing,
			parent=self,
			**kwargs,
		)


	def on_click_button(self, prototype: GameObjectPrototype):
		"""
		Handle a button click.
		"""
		if self._last_selected == prototype:
			self._last_selected = None
			if self._on_deselect:
				self._on_deselect()
		else:
			if self._on_select:
				self._on_select(prototype)
			self._last_selected = prototype
