"""
Constants and functions related to temperature.

All calculations are done in Kelvin, and conversions should only be done for
display purposes. 80deg F is not "twice as hot" as 40deg F, but 300K is twice
as hot as 150K.

Note - temperature is to be abbreviated as 'tpr' in this codebase, not as
'temp' since that can be confused with 'temporary'.
"""

# These temperatures are equal to 74deg - 84deg F. The ideal climate for human
# habitation is somewhere between the Southern United States and the Carribean.
# (Source: independent research by me)
MIN_OPTIMAL_TPR = 296.483
MAX_OPTIMAL_TPR = 302.039

# The minimum habitable temperature is the freezing point of water. Although
# humans can survive in colder temperatures, you can't have agriculture without
# liquid surface water.
MIN_HABITABLE_TPR = 273.15

# The maximum recorded temperature on Earth was 134deg F in Death Valley,
# California on 1913-July-10.
MAX_HABITABLE_TPR = 329.817

def temperature_habitability(tpr):
	"""
	Returns the habitability score of a given temperature.
	"""
	if tpr < MIN_HABITABLE_TPR:
		return 0
	elif tpr > MAX_HABITABLE_TPR:
		return 0
	elif tpr < MIN_OPTIMAL_TPR:
		low_range = MIN_OPTIMAL_TPR - MIN_HABITABLE_TPR
		return (tpr - MIN_HABITABLE_TPR) / low_range
	elif tpr > MAX_OPTIMAL_TPR:
		hi_range = MAX_HABITABLE_TPR - MAX_OPTIMAL_TPR
		return (MAX_HABITABLE_TPR - tpr) / hi_range
	return 1

def kelvin_to_fahrenheit(kelvin):
	"""
	Converts a temperature in Kelvin to Fahrenheit.
	"""
	return (kelvin - 273.15) * 9/5 + 32

def fahrenheit_to_kelvin(fahrenheit):
	"""
	Converts a temperature in Fahrenheit to Kelvin.
	"""
	return (fahrenheit - 32) * 5/9 + 273.15

def centigrade_to_kelvin(centigrade):
	"""
	Converts a temperature in Centigrade to Kelvin.
	"""
	return centigrade + 273.15

def kelvin_to_centigrade(kelvin):
	"""
	Converts a temperature in Kelvin to Centigrade.
	"""
	return kelvin - 273.15

def fahrenheit_to_centigrade(fahrenheit):
	"""
	Converts a temperature in Fahrenheit to Centigrade.
	"""
	return (fahrenheit - 32) * 5/9

def centigrade_to_fahrenheit(centigrade):
	"""
	Converts a temperature in Centigrade to Fahrenheit.
	"""
	return centigrade * 9/5 + 32
