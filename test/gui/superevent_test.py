import unittest

from unittest.mock import patch, mock_open

from src.gui.superevent import superevent_from_json, Superevent
from src.gui.superevent import ShowSupereventEvent

def mock_image():
	def inner_mock(*args, **kwargs):
		return 'Image'
	return inner_mock

SUPEREVENT_JSON = """
{
	"event1": {
		"title": "Test Title",
		"image": "path/to/image.png",
		"body": "Test Body",
		"dismiss": "Dismiss"
	}
}
"""

SUPEREVENT_JSON_NESTED = """
{
	"event": {
		"alpha": {
			"title": "Test Title",
			"image": "path/to/image.png",
			"body": "Test Body",
			"dismiss": "Dismiss"
		}
	}
}
"""

class SupereventTest(unittest.TestCase):

	@patch("builtins.open", new_callable=mock_open, read_data=SUPEREVENT_JSON)
	@patch("src.gui.superevent.Image", new_callable=mock_image)
	def disable_test__superevent_from_json__valid_data(self, mock_file, mimg):
		event_key = "event1"
		file_path = "dummy_path.json"
		superevent = superevent_from_json(file_path, event_key)

		self.assertIsInstance(superevent, Superevent)
		self.assertEqual(superevent.title.text, "Test Title")
		self.assertEqual(superevent.img, 'Image')
		self.assertEqual(superevent.body.text, "Test Body")
		self.assertEqual(superevent.button.text, "Dismiss")

	@patch(
		"builtins.open",
		new_callable=mock_open,
		read_data=SUPEREVENT_JSON_NESTED
	)
	@patch("src.gui.superevent.Image", new_callable=mock_image)
	def disable_test__superevent_from_json__nested_data(self, mock_file, mimg):
		event_key = "event-alpha"
		file_path = "dummy_path.json"
		superevent = superevent_from_json(file_path, event_key)

		self.assertIsInstance(superevent, Superevent)
		self.assertEqual(superevent.title.text, "Test Title")
		self.assertEqual(superevent.img, 'Image')
		self.assertEqual(superevent.body.text, "Test Body")
		self.assertEqual(superevent.button.text, "Dismiss")

	@patch("builtins.open", new_callable=mock_open, read_data=SUPEREVENT_JSON)
	def test__superevent_from_json__invalid_key(self, mock_file):
		event_key = "invalid_key"
		file_path = "dummy_path.json"

		with self.assertRaises(KeyError):
			superevent_from_json(file_path, event_key)

	def test__show_superevent_event__init_with_json(self):
		event = ShowSupereventEvent(
			json_file="dummy_path.json",
			json_id="event1"
		)
		self.assertEqual(event.json_file, "dummy_path.json")
		self.assertEqual(event.json_id, "event1")
		self.assertIsNone(event.title)
		self.assertIsNone(event.image_path)
		self.assertIsNone(event.body)
		self.assertIsNone(event.dismiss_text)

	def test__show_superevent_event__init_with_superevent(self):
		event = ShowSupereventEvent(
			title="Test Title",
			image_path="path/to/image.png",
			body="Test Body",
			dismiss_text="Dismiss"
		)
		self.assertIsNone(event.json_file)
		self.assertIsNone(event.json_id)
		self.assertEqual(event.title, "Test Title")
		self.assertEqual(event.image_path, "path/to/image.png")
		self.assertEqual(event.body, "Test Body")
		self.assertEqual(event.dismiss_text, "Dismiss")

	def test__show_superevent_event__init_invalid(self):
		with self.assertRaises(ValueError):
			ShowSupereventEvent()

	@patch("src.gui.superevent.superevent_from_json")
	def test__show_superevent_event__make_from_json(self, mock_from_json):
		mock_from_json.return_value = "Superevent"
		event = ShowSupereventEvent(
			json_file="dummy_path.json",
			json_id="event1"
		)
		result = event.make_superevent()
		mock_from_json.assert_called_once_with("dummy_path.json", "event1")
		self.assertEqual(result, "Superevent")

	@patch("src.gui.superevent.Image", new_callable=mock_image)
	def disable_test__show_superevent_event__make_direct(self, _):
		event = ShowSupereventEvent(
			title="Test Title",
			image_path="path/to/image.png",
			body="Test Body",
			dismiss_text="Dismiss"
		)
		result = event.make_superevent()
		self.assertIsInstance(result, Superevent)
		self.assertEqual(result.title.text, "Test Title")
		self.assertEqual(result.img, "Image")
		self.assertEqual(result.body.text, "Test Body")
		self.assertEqual(result.button.text, "Dismiss")

if __name__ == "__main__":
	unittest.main()
