import time
from src.game.game import Game

def main():
    game = Game()
    print("Poker OCR Analyzer started.")
    print("Press Enter to capture your hand at each phase (or Ctrl+C to quit).")

    # Map display names to betting round names
    phases = [
        ("Pre-flop", "preflop"),
        ("Flop", "flop"),
        ("Turn", "turn"),
        ("River", "river"),
    ]

    for display_name, round_name in phases:
        # Set the betting round
        game.set_betting_round(round_name)
        input(f"\n--- {display_name} ---\nPress Enter to capture cards...")
        print(f"Capturing for betting round: {round_name}")
        game.detect_hand_from_screen()

    print("\nGame phase analysis complete.")

if __name__ == "__main__":
    main() 