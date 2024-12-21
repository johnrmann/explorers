from typing import Callable

from src.gameobject.actor_motives import ActorMotive, ActorMotiveVector

from src.gui.gui import GuiElement
from src.gui.layout import VerticalLayout
from src.gui.primitives import Label, Panel, Spacer
from src.gui.rangebar import Rangebar

LABEL_HEIGHT = 20
LABEL_WIDTH = 100

SPACER_WIDTH = 5
SPACER_HEIGHT = 5

ACTOR_MOTIVES_HEIGHT = (LABEL_HEIGHT * 4) + (SPACER_HEIGHT * 5)
ACTOR_MOTIVES_WIDTH = (LABEL_WIDTH * 2) + (SPACER_WIDTH * 3)

LABELS = ["Oxygen", "Hunger", "Energy", "Sanity"]

class ActorMotivesGui(GuiElement):
	motives: ActorMotiveVector
	_get_motives: Callable[[], ActorMotiveVector]

	def __init__(
		self,
		motives: ActorMotiveVector = None,
		get_motives: Callable[[], ActorMotiveVector] = None,
		**kwargs
	):
		if motives is None and get_motives is None:
			raise ValueError("Need motives")
		elif motives is None:
			self._get_motives = get_motives
		else:
			self.motives = motives
		w, h = ACTOR_MOTIVES_WIDTH, ACTOR_MOTIVES_HEIGHT
		super().__init__(dimensions=(w, h), **kwargs)
		self.panel = Panel(
			rect=((0,0), (w, h)),
			parent=self,
		)
		self._init_labels()
		self._init_bars()

	def _init_labels(self):
		self.labels = VerticalLayout(
			origin=(0, 0),
			parent=self.panel
		)
		Spacer(
			parent=self.labels,
			rect=((0, 0), (LABEL_WIDTH, SPACER_HEIGHT))
		)
		for label in LABELS:
			Label(
				parent=self.labels,
				rect=((0, 0), (LABEL_WIDTH, LABEL_HEIGHT)),
				text=label
			)
			Spacer(
				parent=self.labels,
				rect=((0, 0), (LABEL_WIDTH, SPACER_HEIGHT))
			)

	def _init_bars(self):
		w2 = ACTOR_MOTIVES_WIDTH // 2
		self.bars_layout = VerticalLayout(
			origin=(w2, 0),
			parent=self.panel
		)
		Spacer(
			parent=self.bars_layout,
			rect=((0, 0), (LABEL_WIDTH, SPACER_HEIGHT))
		)
		self.bars = {}
		for mkey in ActorMotive:
			self.bars[mkey] = Rangebar(
				rect=((0, 0), (LABEL_WIDTH, LABEL_HEIGHT)),
				parent=self.bars_layout,
				values=[100]
			)
			Spacer(
				parent=self.bars_layout,
				rect=((0, 0), (LABEL_WIDTH, SPACER_HEIGHT))
			)

	def my_update(self, dt: float):
		if self._get_motives:
			self.motives = self._get_motives()
		for mkey in ActorMotive:
			self.bars[mkey].values = [self.motives.get(mkey)]
