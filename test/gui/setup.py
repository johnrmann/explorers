from unittest.mock import MagicMock

from src.mgmt.game_manager import GameManager
from src.mgmt.event_manager import EventManager

from src.gui.gui import _GuiManager

def make_mock_gui_manager():
	game_mgr = MagicMock(spec=GameManager)
	game_mgr.evt_mgr = MagicMock(spec=EventManager)
	game_mgr.utc = 0
	game_mgr.epoch = (2350 * 360)
	game_mgr.viewport = MagicMock()
	game_mgr.viewport.window_dims = (800, 600)
	game_mgr.world = MagicMock()
	game_mgr.world.terrain = MagicMock()
	game_mgr.world.terrain.dimensions = (64, 64)
	game_mgr.renderer.vp.window_dims = (800, 600)
	gui_mgr = _GuiManager(game_mgr=game_mgr, surface=MagicMock())
	gui_mgr.game_mgr = game_mgr
	return gui_mgr
