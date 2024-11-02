class Terrain(object):
	def __init__(self, map):
		self.map = map

	@property
	def width(self):
		return len(self.map[0])
	
	@property
	def height(self):
		return len(self.map)

	@property
	def center(self):
		w = len(self.map[0])
		h = len(self.map)
		return (w // 2, h // 2)
	
	def lat_long(self, p):
		x,y = p
		cent_x, cent_y = self.center
		dy = cent_y - y
		dx = x - cent_x
		return (dy / self.height, (dx / self.width) * 2)
