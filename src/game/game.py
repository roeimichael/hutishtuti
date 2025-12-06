from typing import List, Union
from .player import MePlayer, EnemyPlayer, PlayerBase
from .table import Table
from .core.card import Card
import os
from datetime import datetime

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
    def __init__(self):
        self.players: List[PlayerBase] = []  # MePlayer and EnemyPlayer objects
        self.betting_round: str = 'preflop'  # 'preflop', 'flop', 'turn', 'river'
        self.table = Table()
        self.dealer_position: int = 0  # Add dealer position tracking

    def add_player(self, player: PlayerBase) -> None:
        self.players.append(player)
        self.table.active_players = self.get_active_players()

    def remove_player(self, player_id: str) -> None:
        self.players = [p for p in self.players if not (hasattr(p, 'player_id') and getattr(p, 'player_id') == player_id)]
        self.table.active_players = self.get_active_players()

    def get_active_players(self) -> int:
        return sum(1 for p in self.players if getattr(p, 'is_active', True))

    def update_me_relative_position(self):
        # Find MePlayer
        me = next((p for p in self.players if p.__class__.__name__ == 'MePlayer'), None)
        if not me:
            return
        # Get all active players in table order
        active_players = [p for p in self.players if getattr(p, 'is_active', True)]
        num_players = len(active_players)
        if num_players == 0:
            me.set_relative_position(None)
            return
        # Find MePlayer's index among active players
        me_index = active_players.index(me)
        # Relative position: how many act before me, starting after dealer
        rel_pos = (me_index - self.dealer_position) % num_players
        me.set_relative_position(rel_pos)

    def start_new_hand(self):
        self.table.reset_for_new_hand()
        for player in self.players:
            if hasattr(player, 'reset_for_new_hand'):
                player.reset_for_new_hand()
        self.betting_round = 'preflop'
        self.table.active_players = self.get_active_players()
        self.update_me_relative_position()

    def process_player_action(self, player_id: str, action: str, amount: float = 0.0):
        player = next((p for p in self.players if getattr(p, 'player_id', None) == player_id or isinstance(p, MePlayer)), None)
        if not player:
            print(f"Player {player_id} not found.")
            return False
        if not getattr(player, 'is_active', True):
            print(f"Player {player_id} is not active.")
            return False
        # Only MePlayer has action methods
        if isinstance(player, MePlayer):
            if action == 'all-in':
                player.all_in()
                self.table.add_to_pot(player.bet_amount)
            elif action == 'bet':
                if player.bet(amount):
                    self.table.add_to_pot(amount)
            elif action == 'fold':
                player.fold()
            elif action == 'call':
                if player.call(amount):
                    self.table.add_to_pot(amount)
            elif action == 'check':
                player.check()
            else:
                print(f"Unknown action: {action}")
                return False
        else:
            # For EnemyPlayer, just update is_active and history
            if action == 'fold':
                player.is_active = False
                player.last_action = 'fold'
                player.history.append(('fold', None))
            elif action in ['bet', 'call', 'all-in']:
                player.last_action = action
                player.history.append((action, amount))
                self.table.add_to_pot(amount)
            elif action == 'check':
                player.last_action = 'check'
                player.history.append(('check', None))
            else:
                print(f"Unknown action: {action}")
                return False
        self.table.active_players = self.get_active_players()
        return True

    def set_betting_round(self, round_name: str):
        if round_name in ['preflop', 'flop', 'turn', 'river']:
            self.betting_round = round_name

    def __str__(self):
        players_str = '\n'.join(str(p) for p in self.players)
        return f"Game State:\nBetting Round: {self.betting_round}\n{self.table}\nPlayers:\n{players_str}"

    def detect_hand_from_screen(self):
        """
        Takes a screenshot, saves it to the images folder, runs OCR based on betting round.
        - Preflop: Detects player's hand cards
        - Flop: Detects flop cards and player's hand
        - Turn: Detects turn card
        - River: Detects river card
        """
        if pyautogui is None:
            print("pyautogui is not installed. Please install it to use screenshot functionality.")
            return
        if not OCR_AVAILABLE:
            print("OCR reader could not be imported from ocr_reader.py.")
            return

        # Create images directory
        images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'images')
        os.makedirs(images_dir, exist_ok=True)

        # Take screenshot
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = os.path.join(images_dir, f'screenshot_{self.betting_round}_{timestamp}.png')
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)

        try:
            # Detect based on betting round
            if self.betting_round == 'preflop':
                hand, hand_str = detect_hand_from_image(screenshot_path)
                print(f"  Your hand: {hand_str}")

            elif self.betting_round == 'flop':
                # Detect both hand and flop
                hand, hand_str = detect_hand_from_image(screenshot_path)
                flop, flop_str = read_flop_from_image(screenshot_path)
                print(f"  Your hand: {hand_str}")
                print(f"  Flop: {flop_str}")

            elif self.betting_round == 'turn':
                turn, turn_str = read_turn_from_image(screenshot_path)
                print(f"  Turn: {turn_str}")

            elif self.betting_round == 'river':
                river, river_str = read_river_from_image(screenshot_path)
                print(f"  River: {river_str}")
            else:
                print(f"Unknown betting round: {self.betting_round}")

        except Exception as e:
            import traceback
            print(f"Error running OCR for {self.betting_round}:", e)
            traceback.print_exc() 