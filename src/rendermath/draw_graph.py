"""
Contains classes and functions for computing a draw graph of isometric boxes.

A box is a rectangular prism between two points.

The draw graph is represented as a directed adj. matrix. If there is an edge
from box A to box B, then that means that B should be drawn before A.
"""

from src.math.direction import Direction

from src.rendermath.box import Box, compare_boxes

class DrawGraph:
	def __init__(self, key_vals=None, cam_dir=Direction.NORTHWEST):
		"""
		key_vals is a dict that maps keys to boxes of the type Box.
		"""
		self.key_vals = key_vals
		self.cam_dir = cam_dir
		self._make()

	def _make(self):
		"""Constructs the adjacency matrix for the draw graph."""
		self.adj_matrix = {}
		for key, box in self.key_vals.items():
			self.adj_matrix[key] = []
			for other_key, other_box in self.key_vals.items():
				if key == other_key:
					continue
				if compare_boxes(box, other_box, self.cam_dir) == -1:
					self.adj_matrix[key].append(other_key)

	def _dfs(self, key, visited, draws):
		"""Depth-first search to get the draw order."""
		if key in visited:
			return
		visited.add(key)
		for neighbor in self.adj_matrix.get(key, []):
			self._dfs(neighbor, visited, draws)
		draws.append(key)

	def get_draws(self, key):
		"""
		Gets a list of things to draw before drawing the box with the given
		key.
		
		If the box can be drawn indep. of everything else, it just returns
		a single-elem list with the key in it. If there's one thing that must
		be drawn before the box, it returns [thing's key, key].

		The given key is guaranteed to be the last element in the returned
		list (if it hasn't been drawn yet).
		"""
		if key not in self.adj_matrix:
			return []
		draws = []
		visited = set()
		self._dfs(key, visited, draws)
		return draws

	def mark_drawn(self, drawn_key):
		"""
		Marks the key as drawn.

		Note that this carries the assumption that we've also drawn everything
		that needs to be drawn before key. Not drawing things in the correct
		draw order could lead to undefined behavior!
		"""
		if drawn_key in self.adj_matrix:
			del self.adj_matrix[drawn_key]
		for k in self.adj_matrix:
			if drawn_key in self.adj_matrix[k]:
				self.adj_matrix[k].remove(drawn_key)
