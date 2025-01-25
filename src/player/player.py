"""
Represents information about a player playing the game.

Note that player refers to human player, not a character in the game world.
Characters in the game world are referred to as "actors."
"""

class Player:
	uid: int = 0

	def __init__(self, uid: int = None):
		if uid is None or uid == 0:
			raise ValueError("Player must have a unique ID")
		else:
			self.uid = uid


	def __eq__(self, other):
		"""
		Compare Players directly by object pointer (we should never have two
		objects for the same player) or by UID.
		"""
		if isinstance(other, Player):
			return id(self) == id(other)
		elif isinstance(other, int):
			return other == 0 or self.uid == other
		else:
			return False
