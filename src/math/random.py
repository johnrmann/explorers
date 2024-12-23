"""
Functions for dealing with random numbers.
"""

import random

def vary_value_percent(value, p_variation):
	"""
	Vary a value by a percentage of itself. For example, if value is 100 and
	p_variation is 0.1, the result will be between 90 and 110.
	"""
	p_value = value * p_variation
	return value + random.uniform(-p_value, p_value)

def vary_value_nominal(value, variation):
	"""
	Vary a value by an amount. For example, if value is 100 and variation is
	100, the result will be between 0 and 200.
	"""
	return value + random.uniform(-variation, variation)
