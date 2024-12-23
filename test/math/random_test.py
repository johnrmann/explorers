import unittest
from src.math.random import vary_value_percent, vary_value_nominal

class TestRandomFunctions(unittest.TestCase):

	def test__vary_value_percent__within_range(self):
		value = 100
		p_variation = 0.1
		result = vary_value_percent(value, p_variation)
		self.assertTrue(90 <= result <= 110)

	def test__vary_value_nominal__within_range(self):
		value = 100
		variation = 100
		result = vary_value_nominal(value, variation)
		self.assertTrue(0 <= result <= 200)

if __name__ == '__main__':
	unittest.main()
