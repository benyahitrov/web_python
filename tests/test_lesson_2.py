import random
from Lesson_2.main import Player, Bag, Card


random.seed(123)


class TestPlayer:
    def test_str(self):
        p = Player('human', 1)
        res = p.__str__()
        assert res == 'Player № 1 (human)'


class TestBag:
    def test_get_unique_number(self):
        b = Bag()
        res = b.get_unique_number()
        assert res == 7


class TestCard:
    def test_str(self):
        c = Card()
        res = c.__str__()
        template = '----------------------\n  35 12 53       14 5\n49   69   72 43   44  '\
            '\n  7 21 18     90   32\n----------------------'
        assert res == template

    def test_get_unique_number(self):
        c = Card()
        res = c.get_unique_number()
        assert res == 38

    def test_has_number(self):
        c = Card()
        res = c.has_number(41)
        assert res

    def test_is_filled(self):
        c = Card()
        numbers = [2, 51, 83, 66, 56, 88, 69, 82, 86, 77, 63, 67, 54, 48, 5]
        for number in numbers:
            c.strike_out_number(number)
        print(c)
        res = c.is_filled()
        assert res


