from enum import Enum

from src.utility.calendar import (
	utc_float_to_utc_string,
	utc_float_to_mission_string,
	DEFAULT_EPOCH
)

from src.gui.gui import GuiElement
from src.gui.primitives import Label, Panel, Button

DIMENSIONS = (150, 30)

class MissionClockMode(Enum):
	EARTH_CALENDAR = 0
	MISSION_CALENDAR = 1

class MissionClock(GuiElement):
	"""
	The mission clock is an element that appears in the top-left corner of the
	screen, and shows the current time. There is also a button that you can
	click to toggle between calendars (Mission Time and UTC).
	"""

	_mode: MissionClockMode = MissionClockMode.EARTH_CALENDAR

	_utc_per_earth_day: float = 1

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.button = Button(
			rect=((0, 0), (50, 30)),
			text='UTC',
			callback=self.on_click_clock_mode,
			parent=self
		)
		self.panel = Panel(rect=((50, 0), (100, 30)), parent=self)
		self.label = Label(
			rect=((0, 0), (100, 30)),
			text='0000-00-00',
			parent=self.panel,
		)
		self._update_label(0)

	def __del__(self):
		del self.button
		del self.label
		del self.panel
	
	@property
	def origin(self):
		return (0,0)

	@property
	def dimensions(self):
		return DIMENSIONS

	def on_click_clock_mode(self):
		"""When we click the clock mode button, toggle between calendars."""
		if self._mode == MissionClockMode.EARTH_CALENDAR:
			self._mode = MissionClockMode.MISSION_CALENDAR
			self.button.text = 'MT'
		else:
			self._mode = MissionClockMode.EARTH_CALENDAR
			self.button.text = 'UTC'
		self._update_label(self.gui_mgr.game_mgr.utc)

	def my_update(self, dt):
		return self._update_label(self.gui_mgr.game_mgr.utc)

	def _update_label(self, utc):
		if self._mode == MissionClockMode.EARTH_CALENDAR:
			self.label.text = utc_float_to_utc_string(
				utc,
				utc_per_day=self._utc_per_earth_day,
				epoch=DEFAULT_EPOCH,
			)
		else:
			self.label.text = utc_float_to_mission_string(
				utc,
				utc_per_day=self._utc_per_earth_day,
				days_per_year=360,
			)
