from src.game import Game
from src.dice import Die

def _dice(vals):
    dice = [Die() for _ in vals]
    for d, v in zip(dice, vals):
        d.value = v
    return dice

def test_scoring_triple_and_singles():
    g = Game(players=[], hot_dice_enabled=False)
    dice = _dice([2, 2, 2, 1, 5, 3])
    score, used = g.calculate_score(dice)
    assert score == 350
    assert used == 5

def test_scoring_four_kind_multiplier():
    g = Game(players=[])
    dice = _dice([3, 3, 3, 3, 2, 2])
    score, used = g.calculate_score(dice)
    assert score == 600
    assert used == 4

def test_scoring_six_ones_big():
    g = Game(players=[])
    dice = _dice([1, 1, 1, 1, 1, 1])
    score, used = g.calculate_score(dice)
    assert score == 4000
    assert used == 6

def test_record_roll_hot_dice_resets_pool(monkeypatch):
    g = Game(players=[], hot_dice_enabled=True, num_dice=6)
    g.dice_pool.remaining_dice = 3
    g.tentative_score = 0
    g.record_roll(score=300, used=3)
    assert g.tentative_score == 300
    assert g.dice_pool.remaining_dice == 6
