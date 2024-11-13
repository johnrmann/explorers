from src.gameobject.gameobject import GameObject
from src.gameobject.constants import NO_OWNER

class Interactable(GameObject):
	"""
	This is an interface for objects that the player can interact with.
	"""

	# Set of player IDs that this object is shared with. Owner is implicitly
	# included.
	shared_with = set()

	def is_interactable_by_player(self, player_id: int):
		if self.owner == NO_OWNER:
			return True
		if player_id == self.owner:
			return True
		return player_id in self.shared_with
