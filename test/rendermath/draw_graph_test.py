import unittest

from src.math.direction import Direction

from src.rendermath.box import Box, compare_boxes

from src.rendermath.draw_graph import DrawGraph

class DrawGraphTest(unittest.TestCase):
	def setUp(self):
		self.boxes_in_row = {
			'alpha': Box(
				p=(0,0,0),
				q=(1,1,1),
			),
			'bravo': Box(
				p=(1,0,0),
				q=(2,1,1),
			),
			'charlie': Box(
				p=(2,0,0),
				q=(3,1,1)
			)
		}
		self.boxes_far_apart = {
			'delta': Box(
				p=(0,0,0),
				q=(1,1,1),
			),
			'echo': Box(
				p=(9,9,0),
				size=(1,1,1)
			)
		}
		self.boxes_complex = {
			'foxtrot': Box(
				p=(0,0,0),
				size=(2,2,2),
			),
			'golf': Box(
				p=(2,0,0),
				size=(1,1,1),
			),
			'hotel': Box(
				p=(2,1,0),
				size=(1,1,1)
			),
			'india': Box(
				p=(2,0,1),
				size=(1,1,1)
			),
		}

	def test__sanity__boxes_in_right_draw_order(self):
		self.assertEqual(
			compare_boxes(
				self.boxes_in_row['alpha'],
				self.boxes_in_row['bravo'],
				Direction.NORTHWEST
			),
			1
		)
		self.assertEqual(
			compare_boxes(
				self.boxes_in_row['bravo'],
				self.boxes_in_row['charlie'],
				Direction.NORTHWEST
			),
			1
		)
		self.assertEqual(
			compare_boxes(
				self.boxes_in_row['alpha'],
				self.boxes_in_row['charlie'],
				Direction.NORTHWEST
			),
			1
		)

	def test__get_draws__right_order(self):
		dg = DrawGraph(key_vals=self.boxes_in_row)
		self.assertEqual(dg.get_draws('alpha'), ['alpha'])
		self.assertEqual(dg.get_draws('bravo'), ['alpha', 'bravo'])
		self.assertEqual(dg.get_draws('charlie'), ['alpha', 'bravo', 'charlie'])

	def test__get_draws__independent(self):
		dg = DrawGraph(key_vals=self.boxes_far_apart)
		self.assertEqual(dg.get_draws('delta'), ['delta'])
		self.assertEqual(dg.get_draws('echo'), ['echo'])

	def test__get_draws__complex(self):
		dg = DrawGraph(key_vals=self.boxes_complex)
		self.assertEqual(dg.get_draws('foxtrot'), ['foxtrot'])
		self.assertEqual(dg.get_draws('golf'), ['foxtrot', 'golf'])
		self.assertEqual(
			dg.get_draws('hotel'), ['foxtrot', 'golf', 'india', 'hotel']
		)
		self.assertEqual(dg.get_draws('india'), ['foxtrot', 'golf', 'india'])

	def test__mark_drawn(self):
		dg = DrawGraph(key_vals=self.boxes_in_row)
		self.assertEqual(dg.get_draws('charlie'), ['alpha', 'bravo', 'charlie'])
		dg.mark_drawn('alpha')
		self.assertEqual(dg.get_draws('charlie'), ['bravo', 'charlie'])
		dg.mark_drawn('bravo')
		self.assertEqual(dg.get_draws('charlie'), ['charlie'])
		dg.mark_drawn('charlie')
		self.assertEqual(dg.get_draws('charlie'), [])

	def test__mark_drawn__evil(self):
		"""Don't try this at home!"""
		dg = DrawGraph(key_vals=self.boxes_in_row)
		self.assertEqual(dg.get_draws('charlie'), ['alpha', 'bravo', 'charlie'])
		dg.mark_drawn('bravo')
		self.assertEqual(dg.get_draws('charlie'), ['alpha', 'charlie'])

if __name__ == '__main__':
	unittest.main()
