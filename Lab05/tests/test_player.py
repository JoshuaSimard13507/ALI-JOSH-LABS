import json
from pathlib import Path
from src.player import Player

def test_bank_and_record_win_loss():
    p = Player("ALI")
    assert p.points == 0
    p.bank_points(450)
    assert p.points == 450

    assert (p.wins, p.games) == (0, 0)
    p.win()
    assert (p.wins, p.games) == (1, 1)

    p.lose()
    assert (p.wins, p.games) == (1, 2)

def test_save_and_load_roundtrip(temp_cwd):
    p = Player("ALI", is_ai=False)
    p.lifetime_score = 12345
    p.wins = 7
    p.games = 11
    p.save()
    save_path = Path("data/players/ali.json")
    assert save_path.exists(), "Expected saved JSON"

    loaded = Player("PLACEHOLDER", is_ai=True)
    ok = loaded.load("ali")
    assert ok is True
    assert loaded.username == "ALI"
    assert loaded.lifetime_score == 12345
    assert loaded.wins == 7
    assert loaded.games == 11
    assert loaded.is_ai is False
