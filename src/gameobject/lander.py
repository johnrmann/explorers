"""
Contains the class and action IDs for the lander.
"""

from src.mgmt.listener import Listener

from src.gameobject.action import Action
from src.gameobject.actor import Actor
from src.gameobject.actor_motives import ActorMotive
from src.gameobject.constants import FILL_OXYGEN, FILL_ENERGY, FILL_HUNGER
from src.gameobject.interactable import Interactable
from src.gameobject.rabbit_hole import (
	RabbitHole, EnterRabbitHoleEvent, ExitRabbitHoleEvent
)

ACTION_ID__LANDER__REFILL_OXYGEN = "action.lander.refill_oxygen"
ACTION_ID__LANDER__REFILL_HUNGER = "action.lander.refill_hunger"
ACTION_ID__LANDER__REFILL_ENERGY = "action.lander.refill_energy"

LANDER_COOLDOWN = 10
LANDER_PER_ACTOR_COOLDOWN = LANDER_COOLDOWN * 2

class Lander(Interactable, RabbitHole, Listener):
	"""
	At the start of the game, each player starts with a lander that can be
	used as a basic home base.
	"""

	motive_filling: ActorMotive = None
	next_use_for_actor: dict[Actor, float]
	next_use: float

	def __init__(self, game_mgr=None, pos=None):
		if pos is None:
			pos = (0,0)
		Interactable.__init__(
			self,
			game_mgr=game_mgr,
			pos=pos,
			size=(11,11,22)
		)
		RabbitHole.__init__(
			self,
			max_capacity=1
		)
		self.next_use_for_actor = {}
		self.next_use = 0
		self.evt_mgr.sub('rabbit_hole.enter', self)
		self.evt_mgr.sub('rabbit_hole.exit', self)

	def update(self, event):
		if isinstance(event, EnterRabbitHoleEvent):
			is_me = event.rabbit_hole == self
			if is_me:
				self.enter(event.actor)

	def image_path(self):
		return "assets/img/lander.png"

	def tick(self, dt: float, utc: float):
		for actor in self.inside.copy():
			actor_next_time = self.next_use_for_actor.get(actor, 0)
			if utc >= actor_next_time:
				self.exit(actor)

	def enter(self, actor: Actor):
		utc = self.game_mgr.utc
		if not super().enter(actor):
			return False
		self.next_use_for_actor[actor] = utc + LANDER_PER_ACTOR_COOLDOWN
		self.next_use = utc + LANDER_COOLDOWN
		return True

	def exit(self, actor: Actor):
		super().exit(actor)
		self.evt_mgr.pub(
			ExitRabbitHoleEvent(
				actor=actor,
				rabbit_hole=self,
			)
		)

	def _make_refill_action(self, actor: Actor, label: str, ev):
		return Action(
			target=self,
			offset=(5, 11),
			display_label=label,
			expected_value=ev,
			event=EnterRabbitHoleEvent(
				actor=actor,
				rabbit_hole=self,
			)
		)

	def _make_refill_oxygen_action(self, actor: Actor):
		return self._make_refill_action(actor, "Refill Oxygen", FILL_OXYGEN)

	def _make_refill_hunger_action(self, actor: Actor):
		return self._make_refill_action(actor, "Have Meal", FILL_HUNGER)

	def _make_refill_energy_action(self, actor: Actor):
		return self._make_refill_action(actor, "Sleep", FILL_ENERGY)

	def actions(self, actor: Actor):
		# Can't use the lander if it's full.
		if self.is_full():
			return []

		# Check global and per-actor cooldowns.
		utc = self.game_mgr.utc
		if utc < self.next_use:
			return []
		elif utc < self.next_use_for_actor.get(actor, 0):
			return []

		# If ownership checks out, we can refill needs.
		if actor.owner == self.owner:
			return [
				self._make_refill_oxygen_action(actor),
				self._make_refill_hunger_action(actor),
				self._make_refill_energy_action(actor),
			]
		else:
			return []
