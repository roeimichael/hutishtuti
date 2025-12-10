"""Main game state management, player actions, and OCR screenshot detection."""
from typing import List, Optional, Dict
from .player import Player
from .table import Table
from .core.card import Card
import os
from datetime import datetime
from src.logging_config import get_logger

logger = get_logger('game')

try:
    import pyautogui
except ImportError:
    pyautogui = None

try:
    from ocr_reader import (
        detect_hand_from_image,
        read_flop_from_image,
        read_turn_from_image,
        read_river_from_image
    )
    OCR_AVAILABLE = True
except ImportError:
    detect_hand_from_image = None
    read_flop_from_image = None
    read_turn_from_image = None
    read_river_from_image = None
    OCR_AVAILABLE = False

class Game:
    def __init__(self, max_seats: int = 9):
        self.table = Table(max_seats=max_seats)
        self.small_blind = 0.0
        self.big_blind = 0.0
        self.hand_number = 0
        self.screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'images')
        os.makedirs(self.screenshots_dir, exist_ok=True)

    def add_player(self, player_name: str, seat: int, stack: float = 0.0, is_hero: bool = False) -> bool:
        player = Player(player_name, seat, stack)
        player.is_hero = is_hero
        return self.table.add_player_to_seat(player, seat)

    def remove_player(self, seat: int) -> Optional[Player]:
        return self.table.remove_player_from_seat(seat)

    def find_player_by_name(self, name: str) -> Optional[Player]:
        for player in self.table.get_seated_players():
            if player.player_name == name:
                return player
        return None

    def update_player_stack(self, seat: int, stack: float):
        player = self.table.get_player_at_seat(seat)
        if player:
            player.stack = stack

    def update_player_sitting_out(self, seat: int, sitting_out: bool):
        player = self.table.get_player_at_seat(seat)
        if player:
            player.is_sitting_out = sitting_out

    def set_blinds(self, small_blind: float, big_blind: float):
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.table.set_blinds(small_blind, big_blind)

    def start_new_hand(self):
        self.hand_number += 1
        self.table.reset_for_new_hand()
        self.table.advance_dealer_button()
        self.table.assign_blinds()
        logger.info(f"Starting hand #{self.hand_number}")

    def post_blinds(self):
        if self.table.small_blind_seat is not None:
            sb_player = self.table.get_player_at_seat(self.table.small_blind_seat)
            if sb_player:
                sb_player.place_bet(self.small_blind, self.table.betting_round)
                self.table.add_to_pot(self.small_blind)
                logger.info(f"{sb_player.player_name} posts SB ${self.small_blind}")
        if self.table.big_blind_seat is not None:
            bb_player = self.table.get_player_at_seat(self.table.big_blind_seat)
            if bb_player:
                bb_player.place_bet(self.big_blind, self.table.betting_round)
                self.table.add_to_pot(self.big_blind)
                self.table.current_bet = self.big_blind
                logger.info(f"{bb_player.player_name} posts BB ${self.big_blind}")

    def process_action(self, seat: int, action: str, amount: float = 0.0) -> bool:
        player = self.table.get_player_at_seat(seat)
        if not player:
            logger.warning(f"No player at seat {seat}")
            return False
        if not player.is_active or player.is_sitting_out:
            logger.warning(f"{player.player_name} cannot act (active={player.is_active}, sitting_out={player.is_sitting_out})")
            return False
        if action == 'fold':
            player.fold(self.table.betting_round)
            logger.info(f"{player.player_name} folds")
        elif action == 'check':
            player.check(self.table.betting_round)
            logger.info(f"{player.player_name} checks")
        elif action == 'call':
            call_amount = self.table.current_bet - player.current_bet
            if player.call(call_amount, self.table.betting_round):
                self.table.add_to_pot(call_amount)
                logger.info(f"{player.player_name} calls ${call_amount}")
            else:
                return False
        elif action == 'bet' or action == 'raise':
            if player.raise_bet(amount, self.table.betting_round):
                self.table.current_bet = player.current_bet
                self.table.add_to_pot(amount)
                logger.info(f"{player.player_name} raises to ${player.current_bet}")
            else:
                return False
        elif action == 'all-in':
            player.all_in(self.table.betting_round)
            self.table.add_to_pot(player.total_pot_contribution - (player.total_pot_contribution - player.action_history[-1][1]))
            logger.info(f"{player.player_name} goes all-in for ${player.action_history[-1][1]}")
        else:
            logger.error(f"Unknown action: {action}")
            return False
        return True

    def advance_betting_round(self, round_name: str):
        if round_name not in ['preflop', 'flop', 'turn', 'river', 'showdown']:
            logger.error(f"Invalid betting round: {round_name}")
            return
        self.table.betting_round = round_name
        self.table.reset_for_new_round()
        logger.info(f"Advancing to {round_name}")

    def set_hero_cards(self, card1: Card, card2: Card):
        for player in self.table.get_seated_players():
            if player.is_hero:
                player.set_cards(card1, card2)
                logger.info(f"Hero cards: {player.get_cards_str()}")
                return
        logger.warning("No hero player found")

    def set_player_cards(self, seat: int, card1: Card, card2: Card):
        player = self.table.get_player_at_seat(seat)
        if player:
            player.set_cards(card1, card2)
            logger.info(f"{player.player_name} cards: {player.get_cards_str()}")

    def distribute_pot(self, winners: List[int]):
        self.table.calculate_side_pots()
        if not self.table.side_pots:
            total_pot = self.table.calculate_total_pot()
            share = total_pot / len(winners)
            for seat in winners:
                player = self.table.get_player_at_seat(seat)
                if player:
                    player.stack += share
                    logger.info(f"{player.player_name} wins ${share:.2f}")
        else:
            for side_pot in reversed(self.table.side_pots):
                eligible_winners = [seat for seat in winners if self.table.get_player_at_seat(seat).player_name in side_pot.eligible_players]
                if eligible_winners:
                    share = side_pot.amount / len(eligible_winners)
                    for seat in eligible_winners:
                        player = self.table.get_player_at_seat(seat)
                        if player:
                            player.stack += share
                            logger.info(f"{player.player_name} wins ${share:.2f} from side pot")

    def get_game_state(self) -> dict:
        return {
            'hand_number': self.hand_number,
            'betting_round': self.table.betting_round,
            'small_blind': self.small_blind,
            'big_blind': self.big_blind,
            'table': self.table.to_dict(),
            'players': [p.to_dict() for p in self.table.get_seated_players()]
        }

    def export_hand_to_csv_row(self) -> dict:
        state = self.get_game_state()
        row = {
            'hand_number': self.hand_number,
            'betting_round': self.table.betting_round,
            'total_pot': self.table.calculate_total_pot(),
            'main_pot': self.table.main_pot,
            'community_cards': self.table.get_community_cards_str(),
            'num_players': self.table.get_player_count(),
        }
        for i, player_dict in enumerate(state['players']):
            prefix = f'player_{i}_'
            row[prefix + 'name'] = player_dict['player_name']
            row[prefix + 'seat'] = player_dict['seat_position']
            row[prefix + 'stack'] = player_dict['stack']
            row[prefix + 'bet'] = player_dict['current_bet']
            row[prefix + 'cards'] = player_dict['cards']
            row[prefix + 'is_hero'] = player_dict['is_hero']
            row[prefix + 'is_dealer'] = player_dict['is_dealer']
            row[prefix + 'is_active'] = player_dict['is_active']
            row[prefix + 'last_action'] = player_dict['last_action']
        return row

    def __str__(self):
        players_str = '\n'.join(str(p) for p in self.table.get_seated_players())
        return f"Game Hand #{self.hand_number}\n{self.table}\nPlayers:\n{players_str}"

    def detect_hand_from_screen(self):
        if pyautogui is None:
            logger.error("pyautogui not installed")
            return None, None
        if not OCR_AVAILABLE:
            logger.error("OCR reader not available")
            return None, None
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = os.path.join(self.screenshots_dir, f'screenshot_{self.table.betting_round}_{timestamp}.png')
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        try:
            if self.table.betting_round == 'preflop':
                hand, hand_str = detect_hand_from_image(screenshot_path)
                logger.info(f"Detected hand: {hand_str}")
                return hand, hand_str
            elif self.table.betting_round == 'flop':
                hand, hand_str = detect_hand_from_image(screenshot_path)
                flop, flop_str = read_flop_from_image(screenshot_path)
                logger.info(f"Hand: {hand_str}, Flop: {flop_str}")
                return (hand, flop), f"{hand_str} | {flop_str}"
            elif self.table.betting_round == 'turn':
                turn, turn_str = read_turn_from_image(screenshot_path)
                logger.info(f"Turn: {turn_str}")
                return turn, turn_str
            elif self.table.betting_round == 'river':
                river, river_str = read_river_from_image(screenshot_path)
                logger.info(f"River: {river_str}")
                return river, river_str
            else:
                logger.error(f"Unknown betting round: {self.table.betting_round}")
                return None, None
        except Exception as e:
            logger.exception(f"Error running OCR for {self.table.betting_round}: {e}")
            return None, None
