from typing import List
import random


class Card:
    def __init__(self):
        self.numbers = []
        self.template = [
            [0, 1, 1, 1, 0, 0, 0, 1, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 0],
            [0, 1, 1, 1, 0, 0, 1, 0, 1],
        ]
        self.used_numbers = []
        for row in self.template:
            row_numbers = []
            for column in row:
                if column:
                    row_numbers.append(self.get_unique_number())
                else:
                    row_numbers.append(' ')
            self.numbers.append(row_numbers)

    def print(self):
        print('-' * 22)
        for row in self.numbers:
            print(*row)
        print('-' * 22)

    def get_unique_number(self) -> int:
        unique_number = random.randint(1, 90)
        while unique_number in self.used_numbers:
            unique_number = random.randint(1, 90)
        self.used_numbers.append(unique_number)
        return unique_number

    def strike_out_number(self, number: int):
        for row_index, row in enumerate(self.numbers):
            for column_index, column in enumerate(row):
                if column == number:
                    self.numbers[row_index][column_index] = '()'

    def is_filled(self) -> bool:
        for row in self.numbers:
            for column in row:
                if isinstance(column, int):
                    return False
        return True

    def has_number(self, number: int):
        for row in self.numbers:
            for column in row:
                if column == number:
                    return True
        return False



class Player:
    def __init__(self, kind, number):
        self.kind = kind
        self.number = number

    def __str__(self):
        return f'Player № {self.number} ({self.kind})'

    def __repr__(self):
        return self.__str__()


class Bag:
    def __init__(self):
        self.used_numbers = []

    def get_unique_number(self) -> int:
        unique_number = random.randint(1, 90)
        while unique_number in self.used_numbers:
            unique_number = random.randint(1, 90)
        self.used_numbers.append(unique_number)
        return unique_number


def players_init() -> List:
    players = []
    players_number = input('Введите количество игроков (2-8)')
    while not players_number.isdigit() or int(players_number) < 2 or int(players_number) > 8:
        players_number = input('Значение должно быть числом в диапазоне 2-8 ')
    for number in range(1, int(players_number) + 1):
        player_kind = input(f'Введите тип для игрока №{number} (1-человек, 2-компьютер) ')
        while not players_number.isdigit() or 1 > int(player_kind) or int(player_kind) > 2:
            player_kind = input(f'Введите корректное значение (1-человек, 2-компьютер) ')
        player = Player('human'if int(player_kind) == 1 else 'comp', number)
        players.append(player)
    return players


def cards_init(players: List) -> List:
    cards = []
    for index in range(len(players)):
        card = Card()
        cards.append(card)
    return cards


def print_cards(cards: List):
    for index, card in enumerate(cards):
        print(f'Карточка игрока {index + 1}:')
        cards[index].print()


def game_loop():
    players = players_init()
    cards = cards_init(players)
    bag = Bag()
    game_over = False
    while not game_over:
        print_cards(cards)
        barrel_number = bag.get_unique_number()
        print('Номер бочёнка: ', barrel_number)
        for index, player in enumerate(players):
            if player.kind == 'human':
                answer = input(f'{player}, зачеркнуть число? (y/n)')
                while answer not in 'yn':
                    answer = input(f'{player}, введите корректный ответ (y/n)')
                if answer == 'y':
                    if cards[index].has_number(barrel_number):
                        cards[index].strike_out_number(barrel_number)
                        if cards[index].is_filled():
                            game_over = True
                            print(f'Игрок {player} выиграл')
                            break
                    else:
                        game_over = True
                        print(f'Игрок {player} проиграл')
                        break
                elif answer == 'n':
                    if cards[index].has_number(barrel_number):
                        game_over = True
                        print(f'Игрок {player} проиграл')
                        break
            else:
                cards[index].strike_out_number(barrel_number)
                if cards[index].is_filled():
                    game_over = True
                    print(f'Игрок {player} выиграл')
                    break



    #
    #     # card.strike_out_number(n)
    #     # card.print()
    #     # if card.is_filled():
    #     #     break
    # print('Game over')


if __name__ == '__main__':
    game_loop()
