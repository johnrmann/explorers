import json

from src.mgmt.event import Event

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
		super().__init__(dimensions=(w, h))
		screen_w, screen_h = self.gui_mgr.surface.get_size()
		self.relative_origin = ((screen_w - w) // 2, (screen_h - h) // 2)
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
			parent=self.panel,
			callback=self.remove_me
		)

def superevent_from_json(file: str, event_key: str):
	"""
	Given a file and key, creates a superevent from a JSON file.
	"""

	json_f = open(file, 'r', encoding='utf-8')
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

class ShowSupereventEvent(Event):
	"""
	Publish this event to show a superevent. We support two interfaces... you
	can either give it a JSON file and an ID, or a use the Superevent
	initialization signature (title, img path, body, dismiss text).
	"""

	def __init__(
			self,
			# Read a superevent from a (file, id).
			json_file=None,
			json_id=None,
			# Alternatively, pass the Superevent initialization signature.
			title=None,
			image_path=None,
			body=None,
			dismiss_text=None,
	):
		has_file_interface = json_file is not None and json_id is not None
		has_superevent_interface = all([
			title is not None,
			image_path is not None,
			body is not None,
			dismiss_text is not None,
		])
		if not has_file_interface and not has_superevent_interface:
			raise ValueError("You must use one of the two interfaces.")
		super().__init__(event_type="gui.superevent.show")
		self.json_file = json_file
		self.json_id = json_id
		self.title = title
		self.image_path = image_path
		self.body = body
		self.dismiss_text = dismiss_text

	def make_superevent(self):
		"""
		Creates a superevent and mounts it to the GUI.
		"""
		if self.json_file and self.json_id:
			return superevent_from_json(self.json_file, self.json_id)
		else:
			return Superevent(
				title=self.title,
				image_path=self.image_path,
				body=self.body,
				dismiss_text=self.dismiss_text
			)
