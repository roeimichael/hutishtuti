from typing import List, Optional, Dict
from .core.card import Card
from src.logging_config import get_logger

logger = get_logger('table')

class SidePot:
    def __init__(self, amount: float, eligible_players: List[str]):
        self.amount = amount
        self.eligible_players = eligible_players

    def __str__(self):
        return f"SidePot(${self.amount:.2f}, {len(self.eligible_players)} players)"

    def to_dict(self) -> dict:
        return {
            'amount': self.amount,
            'eligible_players': self.eligible_players
        }

class Table:
    def __init__(self, max_seats: int = 9):
        self.max_seats = max_seats
        self.seats: Dict[int, Optional['Player']] = {i: None for i in range(max_seats)}
        self.community_cards: List[Optional[Card]] = [None] * 5
        self.main_pot = 0.0
        self.side_pots: List[SidePot] = []
        self.current_bet = 0.0
        self.betting_round = 'preflop'
        self.dealer_seat: Optional[int] = None
        self.small_blind_amount = 0.0
        self.big_blind_amount = 0.0
        self.small_blind_seat: Optional[int] = None
        self.big_blind_seat: Optional[int] = None

    def add_player_to_seat(self, player: 'Player', seat: int) -> bool:
        if seat < 0 or seat >= self.max_seats:
            logger.error(f"Invalid seat {seat}")
            return False
        if self.seats[seat] is not None:
            logger.warning(f"Seat {seat} already occupied")
            return False
        self.seats[seat] = player
        player.seat_position = seat
        logger.info(f"Player {player.player_name} added to seat {seat}")
        return True

    def remove_player_from_seat(self, seat: int) -> Optional['Player']:
        if seat < 0 or seat >= self.max_seats:
            logger.error(f"Invalid seat {seat}")
            return None
        player = self.seats[seat]
        self.seats[seat] = None
        if player:
            logger.info(f"Player {player.player_name} removed from seat {seat}")
        return player

    def get_player_at_seat(self, seat: int) -> Optional['Player']:
        if seat < 0 or seat >= self.max_seats:
            return None
        return self.seats[seat]

    def get_seated_players(self) -> List['Player']:
        return [p for p in self.seats.values() if p is not None]

    def get_active_players(self) -> List['Player']:
        return [p for p in self.seats.values() if p is not None and p.is_active and not p.is_sitting_out]

    def get_player_count(self) -> int:
        return sum(1 for p in self.seats.values() if p is not None and not p.is_sitting_out)

    def set_community_cards(self, cards: List[Card]):
        for i, card in enumerate(cards):
            if i < 5:
                self.community_cards[i] = card

    def set_flop(self, card1: Card, card2: Card, card3: Card):
        self.community_cards[0] = card1
        self.community_cards[1] = card2
        self.community_cards[2] = card3

    def set_turn(self, card: Card):
        self.community_cards[3] = card

    def set_river(self, card: Card):
        self.community_cards[4] = card

    def get_community_cards_str(self) -> str:
        return ' '.join(str(card) if card else '??' for card in self.community_cards)

    def add_to_pot(self, amount: float):
        self.main_pot += amount

    def calculate_total_pot(self) -> float:
        total = self.main_pot
        for side_pot in self.side_pots:
            total += side_pot.amount
        return total

    def calculate_side_pots(self):
        players = self.get_active_players()
        if not players:
            return
        players_with_contributions = [(p.player_name, p.total_pot_contribution) for p in players if p.total_pot_contribution > 0]
        if not players_with_contributions:
            return
        players_with_contributions.sort(key=lambda x: x[1])
        self.side_pots = []
        previous_level = 0.0
        remaining_players = set(name for name, _ in players_with_contributions)
        for i, (player_name, contribution) in enumerate(players_with_contributions):
            if contribution > previous_level:
                pot_size = (contribution - previous_level) * len(remaining_players)
                if pot_size > 0:
                    side_pot = SidePot(pot_size, list(remaining_players))
                    self.side_pots.append(side_pot)
                previous_level = contribution
            remaining_players.discard(player_name)
        logger.info(f"Calculated {len(self.side_pots)} side pots")

    def set_blinds(self, small_blind: float, big_blind: float):
        self.small_blind_amount = small_blind
        self.big_blind_amount = big_blind

    def set_dealer_button(self, seat: int):
        if seat < 0 or seat >= self.max_seats:
            logger.error(f"Invalid dealer seat {seat}")
            return
        self.dealer_seat = seat
        player = self.seats[seat]
        if player:
            player.is_dealer = True

    def advance_dealer_button(self):
        if self.dealer_seat is None:
            active_seats = [s for s in range(self.max_seats) if self.seats[s] is not None]
            if active_seats:
                self.dealer_seat = active_seats[0]
        else:
            current = self.seats[self.dealer_seat]
            if current:
                current.is_dealer = False
            next_seat = (self.dealer_seat + 1) % self.max_seats
            attempts = 0
            while attempts < self.max_seats:
                if self.seats[next_seat] is not None:
                    self.dealer_seat = next_seat
                    self.seats[next_seat].is_dealer = True
                    break
                next_seat = (next_seat + 1) % self.max_seats
                attempts += 1

    def assign_blinds(self):
        if self.dealer_seat is None:
            return
        active_seats = [s for s in range(self.max_seats) if self.seats[s] is not None and not self.seats[s].is_sitting_out]
        if len(active_seats) < 2:
            return
        dealer_idx = active_seats.index(self.dealer_seat) if self.dealer_seat in active_seats else 0
        sb_idx = (dealer_idx + 1) % len(active_seats)
        bb_idx = (dealer_idx + 2) % len(active_seats)
        self.small_blind_seat = active_seats[sb_idx]
        self.big_blind_seat = active_seats[bb_idx]
        sb_player = self.seats[self.small_blind_seat]
        bb_player = self.seats[self.big_blind_seat]
        if sb_player:
            sb_player.is_small_blind = True
        if bb_player:
            bb_player.is_big_blind = True

    def reset_for_new_round(self):
        self.current_bet = 0.0
        for player in self.get_seated_players():
            player.reset_for_new_round()

    def reset_for_new_hand(self):
        self.community_cards = [None] * 5
        self.main_pot = 0.0
        self.side_pots = []
        self.current_bet = 0.0
        self.betting_round = 'preflop'
        self.small_blind_seat = None
        self.big_blind_seat = None
        for player in self.get_seated_players():
            player.reset_for_new_hand()

    def __str__(self):
        total_pot = self.calculate_total_pot()
        board = self.get_community_cards_str()
        active = self.get_player_count()
        dealer_info = f"Dealer@{self.dealer_seat}" if self.dealer_seat is not None else "No Dealer"
        return (f"Table: {self.betting_round.upper()} | Pot=${total_pot:.2f} | Board:[{board}] | "
                f"Players:{active}/{self.max_seats} | {dealer_info}")

    def to_dict(self) -> dict:
        return {
            'max_seats': self.max_seats,
            'community_cards': [str(c) if c else None for c in self.community_cards],
            'main_pot': self.main_pot,
            'side_pots': [sp.to_dict() for sp in self.side_pots],
            'total_pot': self.calculate_total_pot(),
            'current_bet': self.current_bet,
            'betting_round': self.betting_round,
            'dealer_seat': self.dealer_seat,
            'small_blind_amount': self.small_blind_amount,
            'big_blind_amount': self.big_blind_amount,
            'small_blind_seat': self.small_blind_seat,
            'big_blind_seat': self.big_blind_seat,
            'player_count': self.get_player_count()
        }
