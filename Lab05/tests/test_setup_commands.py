from src.setup import Setup
from src.player import Player

def test_help_prints(mock_print):
    s = Setup()
    s.cmd_help([])
    out = "\n".join(mock_print)
    assert "Farkle CLI" in out

def test_scoring_target_and_hotdice(mock_print):
    s = Setup()
    s.cmd_scoring_target(["7500"])
    assert s.target_score == 7500
    s.cmd_scoring_hotdice(["off"])
    assert s.hot_dice_enabled is False
    s.cmd_scoring_hotdice(["on"])
    assert s.hot_dice_enabled is True

def test_player_rename_and_new():
    s = Setup()
    s.cmd_player_rename(["ALI"])
    assert s.players[0].username == "ALI"

    s.cmd_player_new(["SAM"])
    assert isinstance(s.players[0], Player)
    assert s.players[0].username == "SAM"

def test_player_show_and_score_tables(mock_print):
    s = Setup()
    s.players[0].points = 123
    s.players[1].points = 45
    s.cmd_player_show_scores([])
    text = "\n".join(mock_print)
    assert "Player" in text

def test_player_save_and_load(temp_cwd, mock_print):
    s = Setup()
    s.players[0].username = "ALI"
    s.cmd_player_save([])
    s.cmd_player_load(["ALI"])
    text = "\n".join(mock_print)
    assert "doesn't exist" in text or "loaded" in text
