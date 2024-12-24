import random

# 
TUTORIAL_COLONY_NAME = "Camooweal"

SINGLE_PLAYER_FIRST_COLONY_NAME = "First Landing"

MULTIPLAYER_FIRST_COLONY_NAMES = [
	"Outpost Alpha",
	"Outpost Beta",
	"Outpost Gamma",
	"Outpost Delta",
	"Outpost Epsilon",
	"Outpost Zeta",
	"Outpost Eta",
	"Outpost Theta",
]

COLONY_NAMES = [
	# Pan-Western
	"Olympia",
	"Phoenix",
	"Hope",
	"Elysium",
	"Salem",
	# Anglo-American
	"Hawthorne",
	"Canaveral",
	"Concord",
	"Von Braun",
	"New Jamestown",
	# Russian
	"Novy Baikonur",
	# Chinese
	"Xinjing",
	"Tiantan",
	# Japanese
	# Romance Europe
	"Los Astros",
	"Citta Da Vinci",
]

COLONY_RADIUS = 32

class Colony:
	"""
	A Colony is a settlement that contains structures and units. It is owned by
	a player.
	"""

	# Recall that owner ID starts at one.
	owner: int
	name: str
	structures = None

	center_position: tuple[int, int]
	nw_position: tuple[int, int]
	se_position: tuple[int, int]

	_game_mgr = None

	def __init__(
			self,
			owner: int = None,
			position: tuple[int, int] = None,
			is_first=False,
			game_mgr=None,
			name: str = None
	):
		self.owner = owner
		self._game_mgr = game_mgr
		if owner is None or owner < 1:
			raise ValueError("Owner must be provided.")
		if position is None:
			raise ValueError("Position must be provided.")
		if name is not None:
			self.name = name
		else:
			self.name = self._choose_name(is_first, game_mgr.is_single_player)
		self._set_position(position)
		self.structures = []

	def _set_position(self, position):
		x, y = position
		self.center_position = position
		self.nw_position = (
			x - COLONY_RADIUS,
			y - COLONY_RADIUS
		)
		self.se_position = (
			x + COLONY_RADIUS,
			y + COLONY_RADIUS
		)

	def _choose_name(self, is_first=False, is_single_player=True):
		if is_first:
			if is_single_player:
				return SINGLE_PLAYER_FIRST_COLONY_NAME
			else:
				return MULTIPLAYER_FIRST_COLONY_NAMES[self.owner - 1]
		else:
			return random.choice(COLONY_NAMES)

	def add_structure(self, structure):
		"""
		Assumes that the structure has already been added to the game manager.
		"""
		self.structures.append(structure)

	def is_structure_inside(self, structure):
		"""
		Returns True if the structure is inside the colony.

		TODO(jm) -- need better looped bounding box check.
		"""
		x, y = structure.pos
		nw_x, nw_y = self.nw_position
		se_x, se_y = self.se_position
		if not (nw_x <= x <= se_x):
			return False
		if not (nw_y <= y <= se_y):
			return False
		return True
