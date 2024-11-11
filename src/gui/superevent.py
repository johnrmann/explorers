import json

from src.gui.gui import GuiElement
from src.gui.constants import TITLE_HEIGHT
from src.gui.primitives import Label, Panel, Button, TextBox, Image

SUPEREVENT_IMG_WIDTH = 800
SUPEREVENT_IMG_HEIGHT = int(SUPEREVENT_IMG_WIDTH * (9 / 16))

SUPEREVENT_BODY_HEIGHT = 200

class Superevent(GuiElement):
	"""
	A "Superevent" is a large pop up dominated by a large image, with some
	flavor text below the image. They offer zero options. They are used for
	either...

	1)	Marking major events in the game, such as the first landing,
		the first rainfall, asteroid strikes.
	
	2)	Offering a "gut check" to the player, telling them how they're
		doing.
	"""
	def __init__(self, title="", image_path="", body="", dismiss_text=""):
		super().__init__()
		w, h = self.dimensions()
		self.panel = Panel(
			rect=(self.origin(), self.dimensions()),
		)
		self.title = Label(
			rect=((0, 0), (w, TITLE_HEIGHT)),
			text=title,
			container=self.panel,
		)
		self.img = Image(
			rect=((0, TITLE_HEIGHT), (w, SUPEREVENT_IMG_HEIGHT)),
			image=image_path,
			container=self.panel
		)
		self.body = TextBox(
			rect=((0, TITLE_HEIGHT + SUPEREVENT_IMG_HEIGHT), (w, 200)),
			text=body,
			container=self.panel
		)
		self.button = Button(
			rect=((0, h - TITLE_HEIGHT), (w, TITLE_HEIGHT)),
			label=dismiss_text,
			container=self.panel
		)
	
	def origin(self):
		width, height = self.dimensions()
		s_width, s_height = self.screen_dimensions
		x = (s_width - width) // 2
		y = (s_height - height) // 2
		return (x, y)

	def width(self):
		return SUPEREVENT_IMG_WIDTH
	
	def height(self):
		title = TITLE_HEIGHT
		img = SUPEREVENT_IMG_HEIGHT
		body = SUPEREVENT_BODY_HEIGHT
		button = TITLE_HEIGHT
		return title + img + body + button

	def dimensions(self):
		return (self.width(), self.height())

def superevent_from_json(file: str, event_key: str):
	json_f = open(file, 'r')
	json_s = json_f.read()
	json_f.close()
	obj = json.loads(json_s)
	path = event_key.split('-')
	while path:
		key = path.pop(0)
		obj = obj[key]
	title = obj['title']
	image = obj['image']
	body = obj['body']
	dismiss = obj['dismiss']
	return Superevent(
		title=title,
		image_path=image,
		body=body,
		dismiss_text=dismiss
	)
