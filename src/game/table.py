from typing import List, Optional
from .core.card import Card

class Table:
    def __init__(self):
        self.pot_size = 0.0
        self.board_cards: List[Optional[Card]] = [None] * 5
        self.current_bet = 0.0
        self.betting_round = 'preflop'  # 'preflop', 'flop', 'turn', 'river'
        self._active_players = 0

    @property
    def active_players(self) -> int:
        return self._active_players

    @active_players.setter
    def active_players(self, value: int):
        self._active_players = value

    def reset_for_new_hand(self):
        self.pot_size = 0.0
        self.board_cards = [None] * 5
        self.current_bet = 0.0
        self.betting_round = 'preflop'
        self._active_players = 0

    def add_to_pot(self, amount: float):
        self.pot_size += amount

    def update_board(self, card: Card, position: int):
        if 0 <= position < 5:
            self.board_cards[position] = card

    def set_betting_round(self, round_name: str):
        if round_name in ['preflop', 'flop', 'turn', 'river']:
            self.betting_round = round_name

    def __str__(self):
        board_str = ' '.join(str(card) if card else '??' for card in self.board_cards)
        return (f"Pot: {self.pot_size}, Board: [{board_str}], "
                f"Active Players: {self.active_players}, "
                f"Betting Round: {self.betting_round}") 