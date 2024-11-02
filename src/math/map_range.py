def map_range(k, range1, range2):
	a, b = range1
	x, y = range2
	diff = k - a
	spread_1 = b - a
	spread_2 = y - x
	p = diff / spread_1
	p2 = p * spread_2
	return p2 + x
