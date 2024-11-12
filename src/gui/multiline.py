"""
Functions for rendering lines.
"""

EST_PIXELS_PER_CHARACTER = 8

def text_render_width(text, font):
	"""Returns the width of the text when rendered with the given pygame
	font."""
	return font.size(text)[0]

def wrap_text(text, font, max_width):
	"""Splits `text` into lines (returned) such that each line can fit in
	`max_width` pixels when rendered with the pygame `font`."""
	read_lines = text.split('\n')
	word_lines = [line.split(' ') for line in read_lines]
	lines = []
	cur_line = ""

	for word_line in word_lines:
		cur_line = ""
		if len(word_line) == 0:
			lines.append('')
			continue
		for word in word_line:
			test_line = f"{cur_line} {word}".strip()
			if text_render_width(test_line, font) <= max_width:
				cur_line = test_line
			else:
				lines.append(cur_line)
				cur_line = word
		if cur_line:
			lines.append(cur_line)

	return lines
