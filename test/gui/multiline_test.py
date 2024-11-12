import unittest

from src.gui.multiline import text_render_width, wrap_text

class MockFont:
	def size(self, text):
		return (10 * len(text), 18)

class TestWrapText(unittest.TestCase):
	def setUp(self):
		self.font = MockFont()

	def test__text_render_width(self):
		self.assertEqual(text_render_width("racecar", self.font), 70)

	def test__wrap_text__single_line(self):
		text = "This is a single line of text."
		max_width = 400
		result = wrap_text(text, self.font, max_width)
		self.assertEqual(result, [text])

	def test__wrap_text__multiple_lines(self):
		text = "This is a line of text that should wrap into multiple lines."
		max_width = 150
		result = wrap_text(text, self.font, max_width)
		self.assertTrue(len(result) > 1)

	def test__wrap_text__exact_width(self):
		text = "Exact width line."
		max_width = self.font.size(text)[0]
		result = wrap_text(text, self.font, max_width)
		self.assertEqual(result, [text])

	def test__wrap_text__empty_string(self):
		text = ""
		max_width = 150
		result = wrap_text(text, self.font, max_width)
		self.assertEqual(result, [])

	def test__wrap_text__newline_characters(self):
		text = "Line one.\nLine two.\nLine three."
		max_width = 300
		result = wrap_text(text, self.font, max_width)
		self.assertEqual(result, ["Line one.", "Line two.", "Line three."])

if __name__ == '__main__':
	unittest.main()
