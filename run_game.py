import time
from src.game.game import Game

def main():
    game = Game()
    print("Poker OCR Analyzer started.")
    print("Press Enter to capture your hand at each phase (or Ctrl+C to quit).")

    phases = ["Pre-flop", "Flop", "Turn", "River", "Showdown"]
    for phase in phases:
        input(f"\n--- {phase} ---\nPress Enter to capture hand...")
        game.detect_hand_from_screen()

    print("\nGame phase analysis complete.")

if __name__ == "__main__":
    main() 