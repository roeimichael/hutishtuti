from typing import List, Optional, Tuple
from .core.card import Card
from src.logging_config import get_logger

logger = get_logger('player')

class Player:
    def __init__(self, player_name: str, seat_position: int, stack: float = 0.0):
        self.player_name = player_name
        self.seat_position = seat_position
        self.stack = stack
        self.current_bet = 0.0
        self.total_pot_contribution = 0.0
        self.cards: List[Optional[Card]] = [None, None]
        self.is_active = True
        self.is_sitting_out = False
        self.is_dealer = False
        self.is_small_blind = False
        self.is_big_blind = False
        self.is_all_in = False
        self.is_hero = False
        self.last_action: Optional[str] = None
        self.action_history: List[Tuple[str, float, str]] = []

    def place_bet(self, amount: float, betting_round: str) -> bool:
        if amount > self.stack or amount < 0:
            logger.warning(f"Invalid bet amount {amount} for player {self.player_name} with stack {self.stack}")
            return False
        self.stack -= amount
        self.current_bet += amount
        self.total_pot_contribution += amount
        if self.stack == 0:
            self.is_all_in = True
        self.action_history.append(('bet', amount, betting_round))
        self.last_action = 'bet'
        return True

    def call(self, amount: float, betting_round: str) -> bool:
        if amount > self.stack:
            logger.warning(f"Call amount {amount} exceeds stack {self.stack} for {self.player_name}")
            return False
        self.stack -= amount
        self.current_bet += amount
        self.total_pot_contribution += amount
        if self.stack == 0:
            self.is_all_in = True
        self.action_history.append(('call', amount, betting_round))
        self.last_action = 'call'
        return True

    def raise_bet(self, amount: float, betting_round: str) -> bool:
        if amount > self.stack:
            logger.warning(f"Raise amount {amount} exceeds stack {self.stack} for {self.player_name}")
            return False
        self.stack -= amount
        self.current_bet += amount
        self.total_pot_contribution += amount
        if self.stack == 0:
            self.is_all_in = True
        self.action_history.append(('raise', amount, betting_round))
        self.last_action = 'raise'
        return True

    def check(self, betting_round: str):
        self.action_history.append(('check', 0.0, betting_round))
        self.last_action = 'check'

    def fold(self, betting_round: str):
        self.is_active = False
        self.action_history.append(('fold', 0.0, betting_round))
        self.last_action = 'fold'

    def all_in(self, betting_round: str):
        amount = self.stack
        self.current_bet += amount
        self.total_pot_contribution += amount
        self.stack = 0
        self.is_all_in = True
        self.action_history.append(('all-in', amount, betting_round))
        self.last_action = 'all-in'

    def set_cards(self, card1: Optional[Card], card2: Optional[Card]):
        self.cards = [card1, card2]

    def get_cards_str(self) -> str:
        if self.cards[0] and self.cards[1]:
            from .core.card import hand_str
            return hand_str(self.cards[0], self.cards[1])
        return "??"

    def reset_for_new_round(self):
        self.current_bet = 0.0

    def reset_for_new_hand(self):
        self.current_bet = 0.0
        self.total_pot_contribution = 0.0
        self.cards = [None, None]
        self.is_active = True
        self.is_dealer = False
        self.is_small_blind = False
        self.is_big_blind = False
        self.is_all_in = False
        self.last_action = None
        self.action_history = []

    def get_position_name(self) -> str:
        if self.is_dealer:
            return "BTN"
        elif self.is_small_blind:
            return "SB"
        elif self.is_big_blind:
            return "BB"
        else:
            return f"Seat {self.seat_position}"

    def __str__(self):
        status = []
        if self.is_dealer:
            status.append("D")
        if self.is_small_blind:
            status.append("SB")
        if self.is_big_blind:
            status.append("BB")
        if self.is_sitting_out:
            status.append("OUT")
        if self.is_all_in:
            status.append("ALL-IN")
        if not self.is_active and not self.is_sitting_out:
            status.append("FOLDED")
        status_str = f"[{','.join(status)}]" if status else ""
        hero_str = "(HERO)" if self.is_hero else ""
        return (f"{self.player_name}{hero_str} @Seat{self.seat_position} {status_str}: "
                f"Stack={self.stack:.2f}, Bet={self.current_bet:.2f}, Cards={self.get_cards_str()}")

    def to_dict(self) -> dict:
        return {
            'player_name': self.player_name,
            'seat_position': self.seat_position,
            'stack': self.stack,
            'current_bet': self.current_bet,
            'total_pot_contribution': self.total_pot_contribution,
            'cards': self.get_cards_str(),
            'is_active': self.is_active,
            'is_sitting_out': self.is_sitting_out,
            'is_dealer': self.is_dealer,
            'is_small_blind': self.is_small_blind,
            'is_big_blind': self.is_big_blind,
            'is_all_in': self.is_all_in,
            'is_hero': self.is_hero,
            'last_action': self.last_action,
            'action_history': self.action_history
        }
