from src.game import Game
from src.player import Player

def test_quick_match_with_ai_only(monkeypatch):
    g = Game(players=[Player("A", is_ai=True), Player("B", is_ai=True)],
             target_score=1000,
             hot_dice_enabled=False)
    monkeypatch.setattr(g, "calculate_score", lambda dice: (500, 1))
    g.dice_pool.remaining_dice = 6
    monkeypatch.setattr(g, "get_player_choice", lambda p: "b")

    ran = g.run()
    assert ran is True
    assert any(p.points >= 1000 for p in g.players)
