"""
For fitting rectangles on a tile.
"""

def fit_img_rect_on_tile_base(img_dims, tile):
	"""
	Given an image rectangle and a square tile base, returns the
	screen origin and dimensions to draw the image on.
	"""
	tile_leftmost = tile[3][0]
	tile_rightmost = tile[1][0]
	tile_bottommost = tile[2][1]

	img_width, img_height = img_dims
	draw_width = (tile_rightmost - tile_leftmost)
	scale_factor = draw_width / img_width
	draw_height = img_height * scale_factor

	return (
		(tile_leftmost, tile_bottommost - draw_height),
		(draw_width, draw_height)
	)
