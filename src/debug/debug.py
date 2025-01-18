from src.mgmt.event import Event

from src.debug.world import interpret_atmosphere_command


def command_to_event(command: str) -> Event:
	"""
	Converts a command to an event.
	"""
	words = command.split()
	if atm_event := interpret_atmosphere_command(words):
		return atm_event
	else:
		return None
