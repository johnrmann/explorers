import unittest
from unittest.mock import patch

from src.render.multisurface import MultiSurface

class TestMultiSurface(unittest.TestCase):

	def setUp(self):
		prefix = 'src.render.multisurface.'
		self.patcher_resize = patch(prefix + 'resize_surface')
		self.patcher_alpha_mask = patch(prefix + 'alpha_mask_from_surface')
		self.patcher_relight = patch(prefix + 'relight_surface')

		self.mock_resize = self.patcher_resize.start()
		self.mock_alpha_mask = self.patcher_alpha_mask.start()
		self.mock_relight = self.patcher_relight.start()

		self.mock_resize.side_effect = lambda s, z: f'resized_{s}_{z}'
		self.mock_alpha_mask.side_effect = lambda s, c: f'alpha_{s}_{c}'
		self.mock_relight.side_effect = lambda s, l: f'relit_{s}_{l}'

		self.addCleanup(self.patcher_resize.stop)
		self.addCleanup(self.patcher_alpha_mask.stop)
		self.addCleanup(self.patcher_relight.stop)

	def test__init__from_surface(self):
		surface = 'surface'
		zoom_factors = [1.0, 2.0]
		lights = [0.5, 1.0]
		alpha_color = 'white'

		ms = MultiSurface(
			surface=surface,
			zoom_factors=zoom_factors,
			lights=lights,
			alpha_color=alpha_color
		)

		self.assertEqual(ms.get(1.0, 0.5), 'relit_resized_surface_1.0_0.5')
		self.assertEqual(ms.get(1.0, 1.0), 'relit_resized_surface_1.0_1.0')
		self.assertEqual(ms.get_alpha(1.0), 'alpha_resized_surface_1.0_white')

	def test__init__from_zoomed_surfaces(self):
		zoomed_surfaces = {1.0: 'zoomed_surface_1', 2.0: 'zoomed_surface_2'}
		lights = [0.5, 1.0]
		alpha_color = 'white'

		ms = MultiSurface(
			zoomed_surfaces=zoomed_surfaces,
			lights=lights,
			alpha_color=alpha_color
		)

		self.assertEqual(ms.get(1.0, 0.5), 'relit_zoomed_surface_1_0.5')
		self.assertEqual(ms.get(1.0, 1.0), 'relit_zoomed_surface_1_1.0')
		self.assertEqual(ms.get_alpha(1.0), 'alpha_zoomed_surface_1_white')

	def test__init__invalid_args(self):
		with self.assertRaises(ValueError):
			MultiSurface()

		with self.assertRaises(ValueError):
			MultiSurface(surface='surface')

		with self.assertRaises(ValueError):
			MultiSurface(zoom_factors=[1.0])

	def test__get(self):
		ms = MultiSurface(
			zoomed_surfaces={1.0: 'zoomed_surface_1'},
			lights=[0.5, 1.0]
		)
		self.assertEqual(ms.get(1.0, 0.5), 'relit_zoomed_surface_1_0.5')
		self.assertEqual(ms.get(1.0, 1.0), 'relit_zoomed_surface_1_1.0')

	def test__get__no_light(self):
		ms = MultiSurface(
			zoomed_surfaces={1.0: 'zoomed_surface_1'},
			lights=[0.5, 1.0]
		)
		self.assertEqual(ms.get(zoom=1.0), 'relit_zoomed_surface_1_1.0')

	def test__get__no_zoom(self):
		ms = MultiSurface(
			zoomed_surfaces={1.0: 'zoomed_surface_1'},
			lights=[0.5, 1.0]
		)
		self.assertEqual(ms.get(), 'relit_zoomed_surface_1_1.0')

	def test__get__nearest_light(self):
		ms = MultiSurface(
			zoomed_surfaces={1.0: 'zoomed_surface_1'},
			lights=[0.5, 1.0]
		)
		self.assertEqual(ms.get(1.0, 0.7), 'relit_zoomed_surface_1_0.5')
		self.assertEqual(ms.get(1.0, 0.8), 'relit_zoomed_surface_1_1.0')

	def test__get_alpha(self):
		ms = MultiSurface(
			zoomed_surfaces={1.0: 'zoomed_surface_1'},
			alpha_color='dummy_color'
		)
		self.assertEqual(
			ms.get_alpha(1.0),
			'alpha_zoomed_surface_1_dummy_color'
		)

	def test__get_alpha__no_zoom(self):
		ms = MultiSurface(
			zoomed_surfaces={1.0: 'zoomed_surface_1'},
			alpha_color='dummy_color'
		)
		self.assertEqual(
			ms.get_alpha(),
			'alpha_zoomed_surface_1_dummy_color'
		)

if __name__ == '__main__':
	unittest.main()
