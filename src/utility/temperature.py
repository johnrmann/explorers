"""
Constants and functions related to temperature.

All calculations are done in Kelvin, and conversions should only be done for
display purposes. 80deg F is not "twice as hot" as 40deg F, but 300K is twice
as hot as 150K.

Note - temperature is to be abbreviated as 'tpr' in this codebase, not as
'temp' since that can be confused with 'temporary'.
"""

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
