"""
This module contains functions for converting between UTC floats and
player-readable date formats, as well as calulating the dates of "holidays"
(events that are used to give the player a sense of time and performance).

Some implementation notes:

	1)	UTC is a floating point number that starts at 0 and increases by 1
		every second, and is used to keep track of time in the game. One real-
		life second generally equals one UTC day. This can be tweaked with the
		utc_per_day parameter in the various functions.
	
	2)	Epoch is a floating point number on the same time scale as UTC, except
		it starts from Jan 1, 0001. It represents the calendar date that the
		game starts at.

	3)	When converting from floats to tuples, the order is (year, month, day),
		in accordance with ISO.
"""

DEFAULT_EPOCH = 1 * 360 * 2350

def utc_float_to_utc_tuple(
		utc: float,
		utc_per_day: float = 1,
		epoch: float = 0
) -> tuple[int, int, int]:
	"""Converts a UTC float to a tuple."""
	days = (utc + epoch) // utc_per_day
	date = (days % 30) + 1
	month = ((days // 30) % 12) + 1
	year = (days // 30) // 12
	return (int(year + 1), int(month), int(date))

def utc_float_to_mission_tuple(
		utc: float,
		utc_per_day: float = 1,
		days_per_year: float = 360,
):
	"""
	Converts a UTC float to a (day, year) tuple.

	Notice that there's no epoch parameter. Unlike Gregorian UTC, mission time
	always starts at year 1, day 1.
	"""
	days = utc // utc_per_day
	day = (days % days_per_year) + 1
	year = (days // days_per_year) + 1
	return (int(year), int(day))

def utc_float_to_utc_string(
		utc: float,
		utc_per_day: float = 1,
		epoch: float = 0,
) -> str:
	"""
	Converts a UTC float to a YYYY-MM-DD string.
	"""
	year, month, date = utc_float_to_utc_tuple(utc, utc_per_day, epoch)
	return f"{year:04d}-{month:02d}-{date:02d}"

def utc_float_to_mission_string(
		utc: float,
		utc_per_day: float = 1,
		days_per_year: float = 360,
) -> str:
	"""
	Converts a UTC float to a DDD-YYY string.
	"""
	year, day = utc_float_to_mission_tuple(utc, utc_per_day, days_per_year)
	return f"{day:03d}-{year:03d}"

def utc_tuple_to_utc_float(
		date: tuple[int, int, int],
		utc_per_day: float = 1,
		epoch: float = 0,
):
	"""
	Converts a (year, month, day) tuple to a UTC float.
	"""
	year, month, day = date
	utc = 0
	utc += ((day - 1) * utc_per_day)
	utc += ((month - 1) * utc_per_day * 30)
	utc += ((year - 1) * utc_per_day * 360)
	return utc - epoch

def mision_tuple_to_utc_float(
		date: tuple[int, int],
		utc_per_day: float = 1,
		days_per_year: float = 360,
):
	"""
	Converts a (year, day) tuple to a UTC float.
	"""
	year, day = date
	utc = 0
	utc += ((day - 1) * utc_per_day)
	utc += ((year - 1) * utc_per_day * days_per_year)
	return utc

# This section of the file deals with holidays.

def next_christmas(
		utc: float,
		utc_per_day: float = 1,
		epoch: float = 0
) -> float:
	"""
	Finds the first Christmas after landing.
	"""
	year, month, date = utc_float_to_utc_tuple(
		utc, utc_per_day=utc_per_day, epoch=epoch
	)
	if month == 12 and date > 25:
		return utc_tuple_to_utc_float(
			(year + 1, 12, 25),
			epoch=epoch,
		)
	else:
		return utc_tuple_to_utc_float(
			(year, 12, 25),
			epoch=epoch
		)

def moon_landing_anniversary(
		utc: float,
		utc_per_day: float = 1,
		epoch: float = 0
) -> float:
	"""
	Finds the (n * 100)th anniversary of the Apollo 11 mission after Mission
	Start. For convenience, also returns what anniversary it is. For example,
	2400-Jan-01 will output (2469-July-20, 500).
	"""
	year, month, date = utc_float_to_utc_tuple(
		utc, utc_per_day=utc_per_day, epoch=epoch
	)
	century = year // 100
	last_two = year % 100
	if last_two > 69:
		century += 1
	if last_two == 69:
		if month > 7:
			century += 1
		if month == 7 and date >= 20:
			century += 1
	return (
		utc_tuple_to_utc_float(
			((century) * 100 + 69, 7, 20),
			epoch=epoch
		),
		(century - 19) * 100,
	)
