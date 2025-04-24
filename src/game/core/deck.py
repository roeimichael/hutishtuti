from typing import List
import random
from .card import Card, Suit, Rank

class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self._initialize_deck()

    def _initialize_deck(self) -> None:
        """Initialize a standard 52-card deck."""
        self.cards = [Card(rank, suit) for suit in Suit for rank in Rank]

    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def deal(self, num_cards: int = 1) -> List[Card]:
        """Deal a specified number of cards from the top of the deck."""
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards in the deck")
        return [self.cards.pop() for _ in range(num_cards)]

    def reset(self) -> None:
        """Reset the deck to a full, shuffled state."""
        self._initialize_deck()
        self.shuffle()

    def __len__(self) -> int:
        return len(self.cards) 