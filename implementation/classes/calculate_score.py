import math
from collections import Counter
from .dice import Die

class CalculateScore:

    # house more static functions that calculate score

    @staticmethod
    def doubling(selection: list[Die]) -> tuple[int, int]:
        """Compute the score for a set of dice according to this variant.

        The algorithm:
          1) Score triples or higher first (with 4/5/6-kind multipliers).
          2) Score leftover single 1s and 5s.
          3) Track how many dice were *consumed* in scoring.

        :param selection: Dice to score (typically the full roll).
        :type selection: list[Die]
        :return: A pair ``(score, used)``, where ``score`` is the awarded points
                 and ``used`` is the number of dice consumed by scoring.
        :rtype: tuple[int, int]
        """
        counts = Counter(d.value for d in selection)
        score = 0
        used = 0

        # Triples and above
        for face in range(1, 7):
            n = counts[face]
            if n >= 3:
                base = 1000 if face == 1 else face * 100
                # 3 -> x1, 4 -> x2, 5 -> x3, 6 -> x4
                mult = (n - 2)
                score += base * mult
                used += n
                counts[face] = 0  # consumed
                print(f"Found {face} rolled {n} times → adding +{base * mult}")

        # Leftover singles of 1s and 5s
        if counts[1] > 0:
            base = 100
            score += base * counts[1]
            used += counts[1]
            print(f"Found 1 rolled {counts[1]} times → adding +{base * counts[1]}")
        if counts[5] > 0:
            base = 50
            score += base * counts[5]
            used += counts[5]
            print(f"Found 5 rolled {counts[5]} times → adding +{base * counts[5]}")

        return score, used

    @staticmethod
    def adding(selection: list[Die]) -> tuple[int, int]:
        """Compute the score for a set of dice according to this variant.

        The algorithm:
          1) Score triples.
          2) Score leftover single 1s and 5s.
          3) Track how many dice were *consumed* in scoring.

        :param selection: Dice to score (typically the full roll).
        :type selection: list[Die]
        :return: A pair ``(score, used)``, where ``score`` is the awarded points
                 and ``used`` is the number of dice consumed by scoring.
        :rtype: tuple[int, int]
        """
        counts = Counter(d.value for d in selection)
        score = 0
        used = 0

        # Triples and above
        for face in range(1, 7):
            n = counts[face]

            triple = 1000 if face == 1 else face * 100
            single = 100 if face == 1 else 50 if face == 5 else 0

            num_triples = math.floor(n/3)
            num_singles = n % 3

            base = (num_triples * triple) + (num_singles * single)

            score += base
            used += (num_triples * 3) + (num_singles if face == 1 or face == 5 else 0)

            print(f"Found {face} rolled {n} times → adding +{base}") if base > 0 else None


        return score, used
