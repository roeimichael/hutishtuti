"""Card, Suit, and Rank definitions for poker game."""
from dataclasses import dataclass
from enum import Enum

RANK_ORDER = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

class Suit(Enum):
    HEARTS = "H"
    DIAMONDS = "D"
    CLUBS = "C"
    SPADES = "S"

class Rank(Enum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

@dataclass
class Card:
    rank: Rank
    suit: Suit

    def __str__(self) -> str:
        return f"{self.rank.value}{self.suit.value}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit

def hand_str(card1: 'Card', card2: 'Card') -> str:
    if card1.rank == card2.rank:
        return f"{card1.rank.value}{card2.rank.value}"
    elif card1.suit == card2.suit:
        high, low = sorted([card1, card2], key=lambda c: RANK_ORDER[c.rank.value], reverse=True)
        return f"{high.rank.value}{low.rank.value}s"
    else:
        high, low = sorted([card1, card2], key=lambda c: RANK_ORDER[c.rank.value], reverse=True)
        return f"{high.rank.value}{low.rank.value}O"
