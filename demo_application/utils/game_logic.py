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
        return f"{self.value.value}{self._get_suit_symbol()}"

    def __str__(self):
        return f"{self.value.value}{self._get_suit_symbol()}"

    def _get_suit_symbol(self):
        return {
            Suit.SPADES: "♠️",
            Suit.HEARTS: "♥️",
            Suit.DIAMONDS: "♦️",
            Suit.CLUBS: "♣️",
        }[self.suit]


class EndHand:
    def __init__(self, cards, points, game_mode, has_last_hand=False, bonuses_points=0):
        self.cards = cards
        self.points = points

        self.has_last_hand = has_last_hand
        self.bonuses_points = bonuses_points
        self.game_mode = game_mode

        self.belotscore = self.convert_points_to_belotscore() + bonuses_points

    def convert_points_to_belotscore(self):
        total_points = self.points
        if self.game_mode == GameMode.NO_TRUMPS:
            total_points *= 2

        last_digit = total_points % 10
        belotscore = total_points // 10

        if self.game_mode == GameMode.ALL_TRUMPS:
            print("All trumps")
            if last_digit >= 4:
                belotscore += 1
        elif self.game_mode == GameMode.NO_TRUMPS:
            print("No trumps")
            if last_digit >= 5:
                belotscore += 1
        else:
            print("Specific suit")
            if last_digit >= 6:
                belotscore += 1

        return belotscore


class TeamScore:
    def __init__(self):
        self.total_belotscore = 0
        self.belotscore_history = [0]
        self.hands = []

    def update_round(self, end_hand):
        self.total_belotscore += end_hand.belotscore
        self.belotscore_history.append(self.total_belotscore)
        self.hands.append(end_hand)

    def get_total_rounds(self):
        return len(self.hands)

    def get_last_hand(self):
        return self.hands[-1].cards if self.hands else []


class Game:

    def __init__(self, game_mode=None):
        self.cards = []
        self.game_mode = None
        self.generate_all_cards()
        self.last_take_points = 10

        self.team_scores = [TeamScore(), TeamScore()]
        game_mode_argument = GameMode.ALL_TRUMPS if game_mode is None else game_mode
        self.change_gamemode(game_mode_argument)

    def change_gamemode(self, game_mode):
        self.game_mode = game_mode
        self.cards = self.sort_cards(self.cards)

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

    def sort_by_gamevalue(self, cards_to_sort):
        cards_to_sort.sort(key=self.get_card_gamevalue, reverse=True)
        return cards_to_sort

    def sort_by_ordervalue(self, cards_to_sort):
        cards_to_sort.sort(key=lambda x: self.get_card_gamevalue(x, CardTrumpOrder, CardNonTrumpOrder))
        return cards_to_sort

    def sort_by_suit(self, cards_to_sort):
        suit_order = [Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS]

        def suit_sort_key(card):
            if card.suit.value == self.game_mode.value:
                return (0, suit_order.index(card.suit))
            else:
                return (1, suit_order.index(card.suit))

        cards_to_sort.sort(key=suit_sort_key)
        return self.cards

    def sort_cards(self, cards_to_sort):
        self.sort_by_ordervalue(cards_to_sort)
        self.sort_by_suit(cards_to_sort)

        return cards_to_sort

    def get_max_points(self):
        return sum([self.get_card_gamevalue(card) for card in self.cards]) + self.last_take_points

    def get_points(self, taken_cards, has_taken_last=False):
        return sum([self.get_card_gamevalue(card) for card in taken_cards]) + (
            self.last_take_points if has_taken_last else 0
        )

    def get_other_cards(self, taken_cards):
        return [card for card in self.cards if str(card) not in [str(taken_card) for taken_card in taken_cards]]

    def add_current_round_points(
        self, taken_cards, team_index=0, has_taken_last=False, bonuses_points=0, enemy_bonuses_points=0
    ):
        current_team_points = self.get_points(taken_cards, has_taken_last)
        current_team_hand = EndHand(taken_cards, current_team_points, self.game_mode, has_taken_last, bonuses_points)
        self.team_scores[team_index].update_round(current_team_hand)

        enemy_team_points = self.get_max_points() - current_team_points
        enemy_cards = [card for card in self.cards if card not in taken_cards]
        enemy_team_hand = EndHand(
            enemy_cards, enemy_team_points, self.game_mode, not has_taken_last, enemy_bonuses_points
        )

        self.team_scores[1 - team_index].update_round(enemy_team_hand)

    def get_team_belotscore(self, team_index=0):
        return self.team_scores[team_index].total_belotscore

    def get_team_belotscore_history(self, team_index=0):
        return self.team_scores[team_index].belotscore_history

    def get_round(self):
        return self.team_scores[0].get_total_rounds()

    def start_new_game(self):
        self.team_scores = [TeamScore(), TeamScore()]

    def revert_last_round(self):
        if self.get_round() <= 0:
            return

        for team in self.team_scores:
            team.hands.pop()
            team.belotscore_history.pop()
            team.total_belotscore = team.belotscore_history[-1] if team.belotscore_history else 0
