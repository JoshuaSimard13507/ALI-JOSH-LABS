from collections import Counter

class CalculateScore:


    @staticmethod
    def default(selection: list[Die]) -> tuple[int, int]:

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