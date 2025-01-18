import unittest

from src.world.atmosphere import AtmosphereChangeEvent, AtmosphereElement

from src.debug.world import interpret_atmosphere_command


class DebugWorldTest(unittest.TestCase):
	def test__interpret_atmosphere_command__add_units(self):
		"""Test that it interprets an add_units command."""
		result = interpret_atmosphere_command(
			["atm.add_units", "oxygen", "100"]
		)
		self.assertEqual(
			result,
			AtmosphereChangeEvent({
				AtmosphereElement.OXYGEN: 100
			})
		)


	def test__interpret_atmosphere_command__add_units_multiple(self):
		"""Test that it can add multiple types of atmosphere."""
		result = interpret_atmosphere_command(
			["atm.add_units", "oxygen", "100", "nitrogen", "500"]
		)
		self.assertEqual(
			result,
			AtmosphereChangeEvent({
				AtmosphereElement.OXYGEN: 100,
				AtmosphereElement.NITROGEN: 500
			})
		)


	def test__interpret_atmosphere_command__remove_units(self):
		"""Test that it interprets a remove_units command."""
		result = interpret_atmosphere_command(
			["atm.remove_units", "carbon", "100"]
		)
		self.assertEqual(
			result,
			AtmosphereChangeEvent({
				AtmosphereElement.CARBON: -100
			})
		)


	def test__interpret_atmosphere_command__remove_units_multiple(self):
		"""Test that it can remove multiple types of atmosphere."""
		result = interpret_atmosphere_command(
			["atm.remove_units", "carbon", "100", "water", "500"]
		)
		self.assertEqual(
			result,
			AtmosphereChangeEvent({
				AtmosphereElement.CARBON: -100,
				AtmosphereElement.WATER: -500
			})
		)


	def test__interpret_atmosphere_command__unknown_command(self):
		"""Test that it returns None when the command is unknown."""
		result = interpret_atmosphere_command(
			["atm.unknown_command", "carbon", "100"]
		)
		self.assertIsNone(result)



if __name__ == "__main__":
	unittest.main()
