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
	def __init__(
		self,
		origin=None,
		parent=None,
		motives: ActorMotiveVector = None
	):
		if motives is None:
			raise ValueError("Need motives")
		self.motives = motives
		if origin is None:
			origin = (0, 0)
		w, h = ACTOR_MOTIVES_WIDTH, ACTOR_MOTIVES_HEIGHT
		self.relative_origin = origin
		super().__init__(parent=parent)
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

	def update(self, dt: float):
		for mkey in ActorMotive:
			self.bars[mkey].values = [self.motives.get(mkey)]