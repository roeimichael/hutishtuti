from typing import List, Optional
from .core.card import Card

class Player:
    def __init__(self, player_id: str, chips: int = 1000):
        self.player_id = player_id
        self.chips = chips
        self.hole_cards: List[Card] = []
        self.current_bet = 0
        self.is_active = True
        self.is_all_in = False

    def receive_cards(self, cards: List[Card]) -> None:
        """Receive hole cards at the start of a hand."""
        self.hole_cards = cards

    def place_bet(self, amount: int) -> bool:
        """Place a bet and return whether the player is all-in."""
        if amount > self.chips:
            return False
        
        self.chips -= amount
        self.current_bet += amount
        
        if self.chips == 0:
            self.is_all_in = True
            
        return True

    def fold(self) -> None:
        """Fold the current hand."""
        self.is_active = False
        self.hole_cards = []

    def reset_for_new_hand(self) -> None:
        """Reset player state for a new hand."""
        self.hole_cards = []
        self.current_bet = 0
        self.is_active = True
        self.is_all_in = False 