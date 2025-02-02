"""
The various types of resources that players can spend.
"""

from enum import Enum

class Resource(Enum):
	ENERGY = 1
	WATER = 2
	FOOD = 3
	FUEL = 4
	WASTE_WATER = 5
