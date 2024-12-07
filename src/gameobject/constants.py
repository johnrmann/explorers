"""
Constants relating to GameObjects.
"""

from src.gameobject.actor_motives import ActorMotiveVector

# Use zero to indicate that something has no owner, can be interacted with
# by any player.
NO_OWNER = 0

# Useful for the action EVs. Don't modify!
FILL_OXYGEN = ActorMotiveVector()
FILL_OXYGEN.oxygen = 100
FILL_HUNGER = ActorMotiveVector()
FILL_HUNGER.hunger = 100
FILL_ENERGY = ActorMotiveVector()
FILL_ENERGY.energy = 100
