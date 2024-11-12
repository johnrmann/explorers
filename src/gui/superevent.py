import json

from src.gui.gui import GuiElement
from src.gui.constants import TITLE_HEIGHT
from src.gui.primitives import Label, Panel, Button, TextBox, Image

SUPEREVENT_IMG_WIDTH = 800
SUPEREVENT_IMG_HEIGHT = int(SUPEREVENT_IMG_WIDTH * (9 / 16))

SUPEREVENT_BODY_HEIGHT = 200

SUPEREVENT_WIDTH = SUPEREVENT_IMG_WIDTH
SUPEREVENT_HEIGHT = (
	TITLE_HEIGHT +
	SUPEREVENT_IMG_HEIGHT + 
	SUPEREVENT_BODY_HEIGHT +
	TITLE_HEIGHT
)

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
		w, h = SUPEREVENT_WIDTH, SUPEREVENT_HEIGHT
		super().__init__()
		self.panel = Panel(
			rect=((0,0), (w,h)),
			parent=self,
		)
		self.title = Label(
			rect=((0, 0), (w, TITLE_HEIGHT)),
			text=title,
			parent=self.panel,
		)
		self.img = Image(
			rect=((0, TITLE_HEIGHT), (w, SUPEREVENT_IMG_HEIGHT)),
			image=image_path,
			parent=self.panel
		)
		self.body = TextBox(
			rect=((0, TITLE_HEIGHT + SUPEREVENT_IMG_HEIGHT), (w, 200)),
			text=body,
			parent=self.panel
		)
		self.button = Button(
			rect=((0, h - TITLE_HEIGHT), (w, TITLE_HEIGHT)),
			text=dismiss_text,
			parent=self.panel
		)

	@property
	def origin(self):
		w, h = self.dimensions
		screen_w, screen_h = self.gui_mgr.surface.get_size()
		return ((screen_w - w) // 2, (screen_h - h) // 2)

	@property
	def dimensions(self):
		return (SUPEREVENT_WIDTH, SUPEREVENT_HEIGHT)


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
