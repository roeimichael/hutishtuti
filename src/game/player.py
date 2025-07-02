from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from .core.card import Card

class PlayerBase(ABC):
    def __init__(self, position: int, stack: float, bet_amount: float = 0.0):
        self.cards: List[Optional[Card]] = [None, None]
        self.stack = stack
        self.bet_amount = bet_amount
        self.position = position  # think how to detrmine a 0 index --- dealer == zero index
        self.is_all_in = False
        self.is_active = True
        self.last_action: Optional[str] = None
        self.history: List[Tuple[str, Optional[float]]] = []  # (action, amount)

    @abstractmethod
    def __str__(self):
        pass

    def bet_to_stack_ratio(self) -> float:
        if self.stack == 0:
            return float('inf')
        return self.bet_amount / self.stack

    def advance_position(self, num_players: int):
        self.position = (self.position + 1) % num_players

    def set_cards(self, card1: Optional[Card], card2: Optional[Card]):
        self.cards = [card1, card2]

    def get_cards_str(self) -> str:
        if self.cards[0] and self.cards[1]:
            from .core.card import hand_str
            return hand_str(self.cards[0], self.cards[1])
        return "Unknown"

class MePlayer(PlayerBase):
    def __init__(self, position: int, stack: float, bet_amount: float = 0.0):
        super().__init__(position, stack, bet_amount)
        self.relative_position: Optional[int] = None  # How many players act before me

    def set_relative_position(self, rel_pos: int):
        self.relative_position = rel_pos

    def __str__(self):
        return (f"MePlayer(pos={self.position}, rel_pos={self.relative_position}, stack={self.stack}, bet={self.bet_amount}, "
                f"cards={self.get_cards_str()}, is_all_in={self.is_all_in}, is_active={self.is_active}, "
                f"last_action={self.last_action})")

    def all_in(self):
        if self.stack > 0:
            self.bet_amount += self.stack
            self.history.append(('all-in', self.stack))
            self.stack = 0
            self.is_all_in = True
            self.last_action = 'all-in'

    def bet(self, amount: float) -> bool:
        if amount > self.stack or amount <= 0:
            return False
        self.stack -= amount
        self.bet_amount += amount
        self.history.append(('bet', amount))
        self.last_action = 'bet'
        if self.stack == 0:
            self.is_all_in = True
        return True

    def fold(self):
        self.is_active = False
        self.last_action = 'fold'
        self.history.append(('fold', None))

    def call(self, amount: float) -> bool:
        if amount > self.stack:
            return False
        self.stack -= amount
        self.bet_amount += amount
        self.history.append(('call', amount))
        self.last_action = 'call'
        if self.stack == 0:
            self.is_all_in = True
        return True

    def check(self):
        self.history.append(('check', None))
        self.last_action = 'check'

    def get_last_action(self) -> Optional[str]:
        return self.last_action

class EnemyPlayer(PlayerBase):
    def __init__(self, player_id: str, position: int, stack: float, bet_amount: float = 0.0):
        super().__init__(position, stack, bet_amount)
        self.player_id = player_id
        self.hand_known = False

    def set_hand_known(self, known: bool, card1: Optional[Card] = None, card2: Optional[Card] = None):
        self.hand_known = known
        if known and card1 and card2:
            self.set_cards(card1, card2)
        elif not known:
            self.cards = [None, None]

    def save_to_history(self):
        # Returns a dict for later CSV export
        return {
            'player_id': self.player_id,
            'position': self.position,
            'stack': self.stack,
            'bet_amount': self.bet_amount,
            'cards': self.get_cards_str() if self.hand_known else 'Unknown',
            'history': self.history
        }

    def __str__(self):
        cards_str = self.get_cards_str() if self.hand_known else "Unknown"
        return (f"EnemyPlayer(id={self.player_id}, pos={self.position}, stack={self.stack}, bet={self.bet_amount}, "
                f"cards={cards_str}, hand_known={self.hand_known}, last_action={self.last_action})") 