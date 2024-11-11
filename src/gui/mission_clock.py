from src.gui.gui import GuiElement
from src.gui.primitives import Label, Panel, Button

DIMENSIONS = (150, 50)

def print_hello():
	print("Hello from clock button")

class MissionClock(GuiElement):
	clock_mode = "UTC" # or "MT"

	def __init__(self):
		super().__init__()
		self.button = Button(
			rect=((0, 0), (50, 50)),
			label=self.clock_mode,
		)
		self.panel = Panel(rect=((50, 0), (100, 50)))
		self.label = Label(
			rect=((0, 0), (100, 50)),
			text="2469-08-20",
			container=self.panel
		)

	def __del__(self):
		del self.button
		del self.label
		del self.panel
