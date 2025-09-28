from src.dice import Die, DicePool

def test_die_roll_range(monkeypatch):
    seq = iter([6, 1, 3])
    monkeypatch.setattr("random.randint", lambda a, b: next(seq))

    d = Die()
    assert d.roll() == 6
    assert d.roll() == 1
    assert d.roll() == 3

def test_dicepool_roll_and_reset(monkeypatch):
    monkeypatch.setattr("random.randint", lambda a, b: 4)

    pool = DicePool(length=6)
    rolled = pool.roll()
    assert len(rolled) == 6
    assert all(d.value == 4 for d in rolled)

    pool.remaining_dice = 3
    rolled2 = pool.roll()
    assert len(rolled2) == 3
    assert all(d.value == 4 for d in rolled2)

    pool.reset()
    assert pool.remaining_dice == 6
