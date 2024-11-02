from src.math.distance import min_planet_distance2

def make_voronoi(d, ps):
	w, h = d
	matrix = [[None] * w for i in range(h)]
	
	labels = {}
	label = 0
	for p in ps:
		labels[p] = label
		label += 1
	
	for x in range(w):
		for y in range(h):
			q = (x,y)
			matrix[y][x] = labels[min_planet_distance2(q, ps, d)]
	
	return matrix
