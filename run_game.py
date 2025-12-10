"""Terminal-based poker OCR analyzer - captures cards at each betting round."""
from src.game.game import Game
from src.logging_config import setup_logging

def main():
    setup_logging()
    game = Game()
    phases = [
        ("Pre-flop", "preflop"),
        ("Flop", "flop"),
        ("Turn", "turn"),
        ("River", "river"),
    ]
    for display_name, round_name in phases:
        game.set_betting_round(round_name)
        input(f"\n--- {display_name} ---\nPress Enter to capture cards...")
        game.detect_hand_from_screen()

if __name__ == "__main__":
    main()
