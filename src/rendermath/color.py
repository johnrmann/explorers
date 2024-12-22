"""
Utilities for dealing with color.
"""

def ensure_rgba(color, default_a=255):
	"""
	Converts a 3-tuple to a 4-tuple, adding the given default alpha value.
	"""
	if len(color) == 3:
		return color + (default_a,)
	elif len(color) == 4:
		return color
	else:
		raise ValueError("Color must be a 3-tuple or 4-tuple.")
