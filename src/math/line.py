"""
Functions for working with lines, line segments, and rays.
"""

from src.math.vector2 import vector2_bounding_rect

def is_line_segment_vertical(lineseg):
	"""Returns true if the line segment is parallel to the y-axis."""
	p, q = lineseg
	px, _ = p
	qx, _ = q
	return px == qx

def is_line_segment_horizontal(lineseg):
	"""Returns true if the line segment is parallel to the x-axis."""
	p, q = lineseg
	_, py = p
	_, qy = q
	return py == qy

def extrude_line_segment_y(lineseg, dy):
	"""
	Returns a polygon point array such that the top and bottom edges are
	parallel to each other, and are separated by dy units.
	"""
	if is_line_segment_vertical(lineseg):
		raise ValueError("Cannot vertically extrude a vertical line")
	p, q = lineseg
	px, py = p
	qx, qy = q
	r = (qx, qy + dy)
	s = (px, py + dy)
	return [p, q, r, s]

def extrude_line_segment_x(lineseg, dx):
	"""
	Returns a polygon point array such that the left and right edges are
	parallel to each other, and are separated by dx units.
	"""
	if is_line_segment_horizontal(lineseg):
		raise ValueError("Cannot horizontally extrude a horizontal line")
	p, q = lineseg
	px, py = p
	qx, qy = q
	r = (qx + dx, qy)
	s = (px + dx, py)
	return [p, q, r, s]

def line_segment_bounding_rect(linesegs):
	"""
	Returns the (origin, dimensions) of the smallest rect that contains all
	points in the given line segments.
	"""
	ps = [p for p, _ in linesegs]
	qs = [q for _, q in linesegs]
	ps_and_qs = ps + qs
	return vector2_bounding_rect(ps_and_qs)
