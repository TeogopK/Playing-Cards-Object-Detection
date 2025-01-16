from enum import Enum


class Suit(Enum):
    SPADES = "s"
    HEARTS = "h"
    DIAMONDS = "d"
    CLUBS = "c"


class Value(Enum):
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"


class GameMode(Enum):
    ALL_TRUMPS = "a"
    NO_TRUMPS = "n"
    SPADES = "s"
    HEARTS = "h"
    DIAMONDS = "d"
    CLUBS = "c"


class CardTrumpOrder(Enum):
    JACK = 0
    NINE = 1
    ACE = 2
    TEN = 3
    KING = 4
    QUEEN = 5
    EIGHT = 6
    SEVEN = 7


class CardNonTrumpOrder(Enum):
    ACE = 0
    TEN = 1
    KING = 2
    QUEEN = 3
    JACK = 4
    NINE = 5
    EIGHT = 6
    SEVEN = 7


class CardTrumpValue(Enum):
    SEVEN = 0
    EIGHT = 0
    QUEEN = 3
    KING = 4
    TEN = 10
    ACE = 11
    NINE = 14
    JACK = 20


class CardNonTrumpValue(Enum):
    SEVEN = 0
    EIGHT = 0
    NINE = 0
    JACK = 2
    QUEEN = 3
    KING = 4
    TEN = 10
    ACE = 11


class Card:
    def __init__(self, value: Value, suit: Suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"{self.value.value}{self.suit.value}"


class TeamScore:
    def __init__(self):
        self.total_score = 0
        self.cards_for_all_rounds = []
        self.scores = []

    def update_round(self, card_current_round, score):
        self.cards_for_all_rounds.append(card_current_round)
        self.scores.append(score)
        self.total_score += score


class Game:

    def __init__(self, game_mode=None):
        self.cards = []
        self.game_mode = GameMode.NO_TRUMPS if game_mode is None else game_mode
        self.generate_all_cards()
        self.last_take_points = 10

        self.team_scores = [TeamScore(), TeamScore()]

    def change_gamemode(self, game_mode):
        self.game_mode = game_mode

    def generate_all_cards(self):
        for suit in Suit:
            for value in Value:
                self.cards.append(Card(value, suit))

    def get_card_gamevalue(self, card, trump_value_class=CardTrumpValue, non_trump_value_class=CardNonTrumpValue):
        if self.game_mode == GameMode.ALL_TRUMPS:
            return trump_value_class[card.value.name].value
        elif self.game_mode == GameMode.NO_TRUMPS:
            return non_trump_value_class[card.value.name].value
        elif card.suit.value == self.game_mode.value:
            return trump_value_class[card.value.name].value
        else:
            return non_trump_value_class[card.value.name].value

    def sort_by_gamevalue(self):
        self.cards.sort(key=self.get_card_gamevalue, reverse=True)
        return self.cards

    def sort_by_ordervalue(self):
        self.cards.sort(key=lambda x: self.get_card_gamevalue(x, CardTrumpOrder, CardNonTrumpOrder))
        return self.cards

    def sort_by_suit(self):
        suit_order = [Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS]

        def suit_sort_key(card):
            if card.suit.value == self.game_mode.value:
                return (0, suit_order.index(card.suit))
            else:
                return (1, suit_order.index(card.suit))

        self.cards.sort(key=suit_sort_key)
        return self.cards

    def sort_cards(self):
        self.sort_by_ordervalue()
        self.sort_by_suit()

        return self.cards

    def get_max_score(self):
        return sum([self.get_card_gamevalue(card) for card in self.cards]) + self.last_take_points

    def get_score(self, taken_cards, has_taken_last=False):
        return sum([self.get_card_gamevalue(card) for card in taken_cards]) + (
            self.last_take_points if has_taken_last else 0
        )

    def add_current_round_scores(self, taken_cards, team_index=0, has_taken_last=False):
        score = self.get_score(taken_cards, has_taken_last)
        self.team_scores[team_index].update_round(taken_cards, score)

        enemy_team_score = self.get_max_score() - score
        enemy_cards = [card for card in self.cards if card not in taken_cards]

        self.team_scores[1 - team_index].update_round(enemy_cards, enemy_team_score)

    def get_team_score(self, team_index=0):
        return self.team_scores[team_index].total_score


g = Game(GameMode.NO_TRUMPS)
print(g.sort_cards())
print(g.get_max_score())
