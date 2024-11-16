import ctypes

lib = ctypes.CDLL("./bin/compiled.so")

lib.make_voronoi.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int)
lib.make_voronoi.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))

lib.free_voronoi.argtypes = (ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.c_int)

def make_voronoi(dimensions, density):
	"""
	Creates a voronoi matrix with dimensions = (width * height). The x-axis is
	looped, as is the case on a planet. The density is the average area of the
	voronoi regions. (width * height) / density points will be created.
	"""
	width, height = dimensions
	c_matrix = lib.make_voronoi(width, height, density)

	# Convert to python lists.
	result = []
	for y in range(height):
		row = [c_matrix[y][x] for x in range(width)]
		result.append(row)

	lib.free_voronoi(c_matrix, height)

	return result
