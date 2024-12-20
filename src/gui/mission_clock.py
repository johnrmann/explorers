from src.gui.gui import GuiElement
from src.gui.primitives import Label, Panel, Button

DIMENSIONS = (150, 30)

DEFAULT_FUNCTION_MAP = [
	("UTC", lambda _: "2469-08-20"),
	("MT", lambda _: "001-001")
]

class MissionClock(GuiElement):
	"""
	The mission clock is an element that appears in the top-left corner of the
	screen, and shows the current time. There is also a button that you can
	click to toggle between calendars (Mission Time and UTC).
	"""

	_mode_idx: int = 0

	def __init__(self, entries=None):
		super().__init__()
		if entries is None:
			entries = DEFAULT_FUNCTION_MAP
		self.function_map = entries
		self.button = Button(
			rect=((0, 0), (50, 30)),
			text=entries[0][0],
			callback=self.on_click_clock_mode,
			parent=self
		)
		self.panel = Panel(rect=((50, 0), (100, 30)), parent=self)
		self.label = Label(
			rect=((0, 0), (100, 30)),
			text=self.get_label_text(0),
			parent=self.panel,
		)

	def __del__(self):
		del self.button
		del self.label
		del self.panel
	
	@property
	def origin(self):
		return (0,0)

	@property
	def dimensions(self):
		return(150, 30)

	def on_click_clock_mode(self):
		"""When we click the clock mode button, toggle between calendars."""
		self._mode_idx = (self._mode_idx + 1) % len(self.function_map)
		self.button.text = self.get_button_text(0)

	def get_button_text(self, _: float):
		"""The text on the button is the ID of the calendar."""
		key, _ = self.function_map[self._mode_idx]
		return key

	def get_label_text(self, dt):
		"""The text on the label is the current date."""
		_, func = self.function_map[self._mode_idx]
		return func(dt)
