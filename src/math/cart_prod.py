"""
Utility functions for computing cartesian products.
"""

from src.math.direction import Direction

def spatial_cart_prod(x_range, y_range, origin=Direction.NORTHWEST):
	"""
	Return the spatial cartesian product of two arrays.

	When doing a cartesian product of an x-range and y-range, we typically
	want to start from the top-left corner and enumerate to the bottom-right
	corner.

	Important note - assumes that both ranges are continuous integers (though
	not nec. in increasing order).

	Input: ( (1,2), (3,4) )
	Output: [
		(1,3),
		(2,3),
		(1,4),
		(2,4),
	]
	"""
	xs = list(x_range)
	ys = list(y_range)
	
	if origin == Direction.NORTHWEST:
		pass
	elif origin == Direction.NORTHEAST:
		xs = xs[::-1]
	elif origin == Direction.SOUTHEAST:
		xs = xs[::-1]
		ys = ys[::-1]
	elif origin == Direction.SOUTHWEST:
		ys = ys[::-1]
	else:
		raise ValueError("Invalid origin.")
	
	# Generate the cartesian product of the ranges
	prod = []
	for y in ys:
		for x in xs:
			prod.append((x,y))
	return prod
