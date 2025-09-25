# tests/test_farkle.py
import unittest
from unittest.mock import patch
from io import StringIO
from pathlib import Path
from types import MethodType
import sys

# Ensure project root is importable, then import normally
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import farkle_game as fg  # noqa: E402


# --- Helpers ---
def D(*faces) -> list[fg.Die]:
    """Build a list of Die with specific face values."""
    return [fg.Die(value=f) for f in faces]


def make_roll_sequence(*values):
    """Patch helper: Die.roll sets Die.value deterministically to the next value."""
    seq = list(values)
    def _roll(self):
        v = seq.pop(0)
        self.value = v
        return v
    return _roll


# --- Tests ---
class TestDieAndDicePool(unittest.TestCase):
    def test_die_roll_changes_value_and_in_range(self):
        d = fg.Die()
        for _ in range(12):
            v = d.roll()
            self.assertIn(v, range(1, 7))
            self.assertEqual(v, d.value)

    def test_dicepool_roll_defaults_to_remaining(self):
        pool = fg.DicePool()
        with patch.object(fg.Die, "roll", new=make_roll_sequence(1, 2, 3, 4, 5, 6)):
            rolled = pool.roll()  # defaults to remaining_dice (6)
        self.assertEqual(len(rolled), 6)
        self.assertListEqual([d.value for d in rolled], [1, 2, 3, 4, 5, 6])

    def test_dicepool_roll_specific_count(self):
        pool = fg.DicePool()
        with patch.object(fg.Die, "roll", new=make_roll_sequence(6, 6, 6)):
            rolled = pool.roll(3)
        self.assertEqual(len(rolled), 3)
        self.assertListEqual([d.value for d in rolled], [6, 6, 6])

    def test_dicepool_reset_sets_remaining_to_six(self):
        pool = fg.DicePool()
        pool.remaining_dice = 2
        pool.reset()
        self.assertEqual(pool.remaining_dice, 6)


class TestTurnScoring(unittest.TestCase):
    def setUp(self):
        self.turn = fg.Turn(turn_id="T1")

    def test_score_triple_ones_plus_two_fives(self):
        # 1,1,1 -> 1000 ; 5,5 -> 100 ; total 1100 ; used 5
        with patch("sys.stdout", new_callable=StringIO):
            score, used = self.turn.score_dice(D(1, 1, 1, 5, 5, 2))
        self.assertEqual(score, 1100)
        self.assertEqual(used, 5)

    def test_score_four_of_a_kind(self):
        with patch("sys.stdout", new_callable=StringIO):
            score, used = self.turn.score_dice(D(2, 2, 2, 2, 3, 4))  # 200*(4-2)=400
        self.assertEqual(score, 400)
        self.assertEqual(used, 4)

    def test_score_six_of_a_kind(self):
        with patch("sys.stdout", new_callable=StringIO):
            score, used = self.turn.score_dice(D(4, 4, 4, 4, 4, 4))  # 400*(6-2)=1600
        self.assertEqual(score, 1600)
        self.assertEqual(used, 6)

    def test_score_singles_only_1_and_5(self):
        with patch("sys.stdout", new_callable=StringIO):
            score, used = self.turn.score_dice(D(1, 5, 2, 3, 4, 6))  # 100 + 50
        self.assertEqual(score, 150)
        self.assertEqual(used, 2)

    def test_score_no_scoring_dice(self):
        with patch("sys.stdout", new_callable=StringIO):
            score, used = self.turn.score_dice(D(2, 3, 4, 6, 2, 3))
        self.assertEqual(score, 0)
        self.assertEqual(used, 0)


class TestTurnFlow(unittest.TestCase):
    def test_select_dice_marks_farkle_on_zero_score(self):
        t = fg.Turn(turn_id="T0")
        game = fg.Game(game_id="G", players=[], allow_hot_dice=True)
        with patch("sys.stdout", new_callable=StringIO):  # silence prints
            gained = t.select_dice(D(2, 3, 4, 6, 2, 3), game)
        self.assertEqual(gained, 0)
        self.assertTrue(t.is_farkle)
        self.assertEqual(t.tentative_score, 0)

    def test_select_updates_tentative_and_remaining(self):
        t = fg.Turn(turn_id="T2")
        game = fg.Game(game_id="G", players=[], allow_hot_dice=True)
        # triple 5s -> 500, used 3 ; remaining goes 6 -> 3
        with patch("sys.stdout", new_callable=StringIO):
            gained = t.select_dice(D(5, 5, 5, 2, 3, 4), game)
        self.assertEqual(gained, 500)
        self.assertFalse(t.is_farkle)
        self.assertEqual(t.tentative_score, 500)
        self.assertEqual(t.dice_pool.remaining_dice, 3)

    def test_hot_dice_resets_pool_when_all_used(self):
        t = fg.Turn(turn_id="T3")
        game = fg.Game(game_id="G", players=[], allow_hot_dice=True)
        # six 1s → 1000*(6-2)=4000; used=6 → pool reset to 6
        with patch("sys.stdout", new_callable=StringIO):
            gained = t.select_dice(D(1, 1, 1, 1, 1, 1), game)
        self.assertEqual(gained, 4000)
        self.assertEqual(t.dice_pool.remaining_dice, 6)

    def test_no_hot_dice_means_no_reset(self):
        t = fg.Turn(turn_id="T4")
        game = fg.Game(game_id="G", players=[], allow_hot_dice=False)
        with patch("sys.stdout", new_callable=StringIO):
            gained = t.select_dice(D(1, 1, 1, 1, 1, 1), game)  # used=6
        self.assertEqual(gained, 4000)
        # Since allow_hot_dice=False, pool should not reset here; your take_turn() later auto-banks.
        self.assertEqual(t.dice_pool.remaining_dice, 0)


class TestPlayerAndGame(unittest.TestCase):
    def test_player_bank_points_adds_total(self):
        p = fg.Player(player_id="P1", name="Tester")
        with patch("sys.stdout", new_callable=StringIO):
            p.bank_points(750)
        self.assertEqual(p.total_score, 750)

    def test_ai_banks_when_threshold_met(self):
        # AI banks when tentative_score >= 500 OR remaining_dice <= 3
        ai = fg.Player(player_id="P2", name="AI", is_ai=True)
        human = fg.Player(player_id="P1", name="You", is_ai=False)
        game = fg.Game(game_id="G1", players=[ai, human], target_score=10000, allow_hot_dice=True)

        with patch.object(fg.Turn, "roll_dice", return_value=D(5, 5, 5, 2, 3, 4)):
            with patch("sys.stdout", new_callable=StringIO):
                ai.take_turn(game)
        self.assertGreaterEqual(ai.total_score, 500)

    def test_game_ends_when_target_reached(self):
        p1 = fg.Player(player_id="P1", name="P1", is_ai=True)
        p2 = fg.Player(player_id="P2", name="P2", is_ai=True)
        game = fg.Game(game_id="GZ", players=[p1, p2], target_score=100, allow_hot_dice=False)

        # Only patch P1's take_turn so it banks and ends game; P2's should never run
        def p1_turn(self, game):
            self.bank_points(120)

        with patch.object(p1, "take_turn", new=MethodType(p1_turn, p1)):
            with patch("sys.stdout", new_callable=StringIO):
                game.start_game()

        self.assertFalse(game.game_in_progress)
        self.assertGreaterEqual(p1.total_score, 100)
        self.assertEqual(game.current_round, 1)

    def test_next_turn_wraps_and_increments_round(self):
        p1 = fg.Player(player_id="P1", name="P1", is_ai=True)
        p2 = fg.Player(player_id="P2", name="P2", is_ai=True)
        game = fg.Game(game_id="GZ", players=[p1, p2], target_score=1000, allow_hot_dice=False)

        self.assertEqual(game.current_player_idx, 0)
        self.assertEqual(game.current_round, 1)

        game.next_turn()
        self.assertEqual(game.current_player_idx, 1)
        self.assertEqual(game.current_round, 1)

        game.next_turn()
        self.assertEqual(game.current_player_idx, 0)
        self.assertEqual(game.current_round, 2)


if __name__ == "__main__":
    unittest.main()
