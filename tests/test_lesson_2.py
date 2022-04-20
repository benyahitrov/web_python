import random
from pytest import fixture
from Lesson_2.main import Player, Bag, Card


random.seed(123)


class TestPlayer:
    def test_str(self):
        player = Player('human', 1)
        res = str(player)
        assert res == 'Player № 1 (human)'


class TestBag:
    def test_get_unique_number(self):
        bag = Bag()
        res = bag.get_unique_number()
        assert res == 7


@fixture
def card() -> Card:
    card = Card()
    return card


class TestCard:
    def test_str(self, card):
        res = str(card)
        template = '----------------------\n  35 12 53       14 5\n49   69   72 43   44  '\
            '\n  7 21 18     90   32\n----------------------'
        assert res == template

    def test_get_unique_number(self, card):
        res = card.get_unique_number()
        assert res == 38

    def test_has_number(self, card):
        res = card.has_number(41)
        assert res

    def test_is_filled(self, card):
        numbers = [2, 51, 83, 66, 56, 88, 69, 82, 86, 77, 63, 67, 54, 48, 5]
        for number in numbers:
            card.strike_out_number(number)
        res = card.is_filled()
        assert res


