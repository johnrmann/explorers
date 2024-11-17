from enum import Enum

class ActorMotive(Enum):
	"""
	Actors have four needs, sorted from most important to least.
	"""
	OXYGEN = 0
	HUNGER = 1
	ENERGY = 2
	SANITY = 3

BASE = -0.1

BASE_MOTIVE_DELTAS = {
	# In real life, an astronaut's suit can last for 6-8 hours.
	ActorMotive.OXYGEN: BASE,
	ActorMotive.ENERGY: BASE / 2,
	ActorMotive.HUNGER: BASE / 4,
	ActorMotive.SANITY: BASE / 8,
}

MOVEMENT_MOTIVE_DELTAS = {
	# This is in addition to base motives. For now, we double the decline
	# in material motives while moving. Notice that sanity acutally goes _up_
	# while moving since exercise is good for you emotionally.
	ActorMotive.OXYGEN: BASE,
	ActorMotive.ENERGY: BASE / 2,
	ActorMotive.HUNGER: BASE / 4,
	ActorMotive.SANITY: -BASE,
}

DESPERATION_CUTOFFS = {
	# Hunger and oxygen have higher desperation cutoffs since they are fatal.
	ActorMotive.OXYGEN: 20,
	ActorMotive.HUNGER: 20,
	ActorMotive.ENERGY: 10,
	ActorMotive.SANITY: 10,
}

class ActorMotiveVector:
	def __init__(self, values=None):
		if not values:
			self.values = {
				ActorMotive.OXYGEN: 0,
				ActorMotive.ENERGY: 0,
				ActorMotive.HUNGER: 0,
				ActorMotive.SANITY: 0,
			}
		else:
			self.values = values

	@property
	def hunger(self):
		"""Returns the hunger motive."""
		return self.values[ActorMotive.HUNGER]

	@property
	def oxygen(self):
		"""Returns the oxygen motive."""
		return self.values[ActorMotive.OXYGEN]

	@property
	def energy(self):
		"""Returns the energy motive."""
		return self.values[ActorMotive.ENERGY]

	@property
	def sanity(self):
		"""Returns the sanity motive."""
		return self.values[ActorMotive.SANITY]

	@hunger.setter
	def hunger(self, value):
		self.values[ActorMotive.HUNGER] = value

	@oxygen.setter
	def oxygen(self, value):
		self.values[ActorMotive.OXYGEN] = value

	@energy.setter
	def energy(self, value):
		self.values[ActorMotive.ENERGY] = value

	@sanity.setter
	def sanity(self, value):
		self.values[ActorMotive.SANITY] = value

	def __add__(self, other):
		if not isinstance(other, ActorMotiveVector):
			raise ValueError("Can only add another ActorMotiveVector")
		new_values = {
			motive: self.values[motive] + other.values[motive]
			for motive in ActorMotive
		}
		return ActorMotiveVector(new_values)

	def __mul__(self, k: float):
		new_values = {
			motive: self.values[motive] * k
			for motive in ActorMotive
		}
		return ActorMotiveVector(new_values)

	def __iter__(self):
		yield self.values[ActorMotive.OXYGEN]
		yield self.values[ActorMotive.HUNGER]
		yield self.values[ActorMotive.ENERGY]
		yield self.values[ActorMotive.SANITY]

	def get(self, motive: ActorMotive):
		"""This wrapper is very useful when looping through motives."""
		return self.values[motive]

	def is_desperate_for(self, motive: ActorMotive):
		"""
		An actor becomes desperate when their needs are so low that they will
		do anything to survive.

		An example: consider the case where the nearest source of food is a
		kilometer away. The actor would run out of hunger before they would
		reach it. If the actor's hunger motive is high, they won't try to
		get there because they'll run out of food before getting there, and at
		a faster rate if they move as opposed to staying still.

		But if their hunger motive is low, they'll try to make the journey,
		even if it kills them.
		"""
		return self.values[motive] <= DESPERATION_CUTOFFS[motive]

	def is_dead(self):
		"""
		Oxygen and hunger are the only fatal motives, although players really
		should not neglect energy and sanity...
		"""
		oxygen = self.values[ActorMotive.OXYGEN]
		hunger = self.values[ActorMotive.HUNGER]
		return oxygen <= 0 or hunger <= 0

	def mutate(self, other):
		"""
		Mutates this motive vector by other.
		"""
		if not isinstance(other, ActorMotiveVector):
			raise ValueError("Can only mutate by another ActorMotiveVector")
		new_values = {
			motive: self.values[motive] + other.values[motive]
			for motive in ActorMotive
		}
		self.values = new_values

def guess_motive_delta_for_time(dt: float):
	"""
	How much will motives decline by for dt seconds?
	"""
	if dt < 0:
		raise ValueError("Time travel not allowed.")
	return {
		motive: delta * dt
		for motive, delta in BASE_MOTIVE_DELTAS.items()
	}

def guess_motive_delta_for_distance(
		distance=None, # meters
		speed=None, # meters per second
):
	"""
	How much will motives decline if we travel `distance` meters at `speed`
	meters per second?
	"""
	if speed <= 0 or distance <= 0:
		raise ValueError("Speed and distance must be positive numbers.")
	time = distance / speed
	time_cost = ActorMotiveVector(BASE_MOTIVE_DELTAS) * time
	dist_cost = ActorMotiveVector(MOVEMENT_MOTIVE_DELTAS) * distance
	return time_cost + dist_cost
