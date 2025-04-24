from typing import List, Dict
from .core.deck import Deck
from .core.card import Card
from .player import Player
from .core.hand_evaluator import HandEvaluator

class Game:
    def __init__(self, small_blind: int = 5, big_blind: int = 10):
        self.players: List[Player] = []
        self.deck = Deck()
        self.community_cards: List[Card] = []
        self.pot = 0
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.current_bet = 0
        self.dealer_position = 0
        self.current_player_position = 0
        self.round = 0  # 0: Pre-flop, 1: Flop, 2: Turn, 3: River

    def add_player(self, player: Player) -> None:
        """Add a player to the game."""
        self.players.append(player)

    def start_new_hand(self) -> None:
        """Start a new hand of poker."""
        self.deck.reset()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.round = 0
        
        # Reset player states
        for player in self.players:
            player.reset_for_new_hand()
        
        # Deal hole cards
        self._deal_hole_cards()
        
        # Post blinds
        self._post_blinds()

    def _deal_hole_cards(self) -> None:
        """Deal hole cards to all players."""
        for player in self.players:
            player.receive_cards(self.deck.deal(4))  # 4 cards for Omaha

    def _post_blinds(self) -> None:
        """Post small and big blinds."""
        small_blind_pos = (self.dealer_position + 1) % len(self.players)
        big_blind_pos = (self.dealer_position + 2) % len(self.players)
        
        self.players[small_blind_pos].place_bet(self.small_blind)
        self.players[big_blind_pos].place_bet(self.big_blind)
        
        self.current_bet = self.big_blind
        self.current_player_position = (big_blind_pos + 1) % len(self.players)

    def deal_community_cards(self) -> None:
        """Deal the next set of community cards."""
        if self.round == 0:  # Flop
            self.community_cards.extend(self.deck.deal(3))
        elif self.round in [1, 2]:  # Turn and River
            self.community_cards.extend(self.deck.deal(1))
        self.round += 1

    def process_player_action(self, player: Player, action: str, amount: int = 0) -> bool:
        """
        Process a player's action (fold, check, call, raise).
        Returns True if the action was valid, False otherwise.
        """
        if not player.is_active:
            return False

        if action == "fold":
            player.fold()
        elif action == "check":
            if self.current_bet > player.current_bet:
                return False
        elif action == "call":
            call_amount = self.current_bet - player.current_bet
            if not player.place_bet(call_amount):
                return False
        elif action == "raise":
            if amount <= self.current_bet:
                return False
            if not player.place_bet(amount - player.current_bet):
                return False
            self.current_bet = amount

        return True

    def determine_winner(self) -> List[Player]:
        """Determine the winner(s) of the current hand."""
        active_players = [p for p in self.players if p.is_active]
        if len(active_players) == 1:
            return active_players

        # TODO: Implement hand comparison logic
        # This will use HandEvaluator to compare hands and determine winners
        return [] 