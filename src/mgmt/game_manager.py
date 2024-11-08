from src.gameobject.gameobject import GameObject
from src.gameobject.actor import Actor
from src.world.world import World

TICKS_PER_SECOND = 25

class GameManager:
	"""
	Primarily responsible for managing game state and the passage of time.
	"""

	game_objects: list[GameObject]
	ticks: int
	world: World

	def __init__(self, world: World):
		self.ticks = 0
		self.game_objects = []
		self.world = world
	
	@property
	def utc(self) -> float:
		"""
		Seconds since game start.
		"""
		return self.ticks / TICKS_PER_SECOND
	
	def tick(self, n_ticks=1):
		"""
		Send an event to listeners about the passage of time.
		"""
		if n_ticks <= 0:
			raise ValueError("Time travel not allowed")
		self.ticks += n_ticks
		dt = n_ticks / TICKS_PER_SECOND
		for obj in self.game_objects:
			obj.tick(dt, self.utc)

	@property
	def player_character(self):
		"""
		Returns the currently selected player character.
		"""
		for go in self.game_objects:
			if isinstance(go, Actor):
				if go._is_played: # TODO(jm) - evil private access
					return go
		raise ValueError("No player character - should never happen!")
	
	def new_player_character(self, position):
		self.game_objects.append(Actor(pos=position))

	def add_game_object(self, go: GameObject):
		self.game_objects.append(go)
