"""
Simple GUI for Poker OCR Analyzer using tkinter.

This provides a visual interface for capturing and analyzing poker cards
at different phases of the game.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.game.game import Game
from card_images_manager import CardImageManager


class PokerOCRGui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Poker OCR Analyzer")
        self.window.geometry("750x1000")
        self.window.resizable(False, False)

        self.game = Game()
        self.card_manager = CardImageManager()

        self.phases = [
            ("Pre-flop", "preflop"),
            ("Flop", "flop"),
            ("Turn", "turn"),
            ("River", "river"),
        ]
        self.current_phase_index = 0

        # Storage for detected cards
        self.hand_cards = ""
        self.flop_cards = ""
        self.turn_card = ""
        self.river_card = ""

        # Storage for PhotoImage objects (must keep references)
        self.photo_images = {}

        self._setup_ui()
        self._update_phase()

    def _setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Poker OCR Analyzer",
            font=("Arial", 20, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Current phase
        self.phase_label = ttk.Label(
            main_frame,
            text="",
            font=("Arial", 16, "bold"),
            foreground="#0066cc"
        )
        self.phase_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Cards display frame
        cards_frame = ttk.LabelFrame(main_frame, text="Detected Cards", padding="15")
        cards_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))

        # Hand cards
        ttk.Label(cards_frame, text="Your Hand:", font=("Arial", 11, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        hand_container = ttk.Frame(cards_frame)
        hand_container.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)

        # Card images container
        self.hand_images_frame = tk.Frame(hand_container, bg='white')
        self.hand_images_frame.pack()
        self.hand_card1_label = tk.Label(self.hand_images_frame, bg='white')
        self.hand_card1_label.pack(side=tk.LEFT, padx=2)
        self.hand_card2_label = tk.Label(self.hand_images_frame, bg='white')
        self.hand_card2_label.pack(side=tk.LEFT, padx=2)

        # Text label below
        self.hand_text_label = ttk.Label(
            hand_container,
            text="",
            font=("Arial", 10),
            foreground="#666666"
        )
        self.hand_text_label.pack()

        # Flop cards
        ttk.Label(cards_frame, text="Flop:", font=("Arial", 11, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        flop_container = ttk.Frame(cards_frame)
        flop_container.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)

        # Flop images container
        self.flop_images_frame = tk.Frame(flop_container, bg='white')
        self.flop_images_frame.pack()
        self.flop_card1_label = tk.Label(self.flop_images_frame, bg='white')
        self.flop_card1_label.pack(side=tk.LEFT, padx=2)
        self.flop_card2_label = tk.Label(self.flop_images_frame, bg='white')
        self.flop_card2_label.pack(side=tk.LEFT, padx=2)
        self.flop_card3_label = tk.Label(self.flop_images_frame, bg='white')
        self.flop_card3_label.pack(side=tk.LEFT, padx=2)

        # Text label below
        self.flop_text_label = ttk.Label(
            flop_container,
            text="",
            font=("Arial", 10),
            foreground="#666666"
        )
        self.flop_text_label.pack()

        # Turn card
        ttk.Label(cards_frame, text="Turn:", font=("Arial", 11, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        turn_container = ttk.Frame(cards_frame)
        turn_container.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)

        # Turn image container
        self.turn_images_frame = tk.Frame(turn_container, bg='white')
        self.turn_images_frame.pack()
        self.turn_card_label = tk.Label(self.turn_images_frame, bg='white')
        self.turn_card_label.pack(side=tk.LEFT, padx=2)

        # Text label below
        self.turn_text_label = ttk.Label(
            turn_container,
            text="",
            font=("Arial", 10),
            foreground="#666666"
        )
        self.turn_text_label.pack()

        # River card
        ttk.Label(cards_frame, text="River:", font=("Arial", 11, "bold")).grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        river_container = ttk.Frame(cards_frame)
        river_container.grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)

        # River image container
        self.river_images_frame = tk.Frame(river_container, bg='white')
        self.river_images_frame.pack()
        self.river_card_label = tk.Label(self.river_images_frame, bg='white')
        self.river_card_label.pack(side=tk.LEFT, padx=2)

        # Text label below
        self.river_text_label = ttk.Label(
            river_container,
            text="",
            font=("Arial", 10),
            foreground="#666666"
        )
        self.river_text_label.pack()

        # Status message
        self.status_label = ttk.Label(
            main_frame,
            text="Click 'Capture Cards' when ready",
            font=("Arial", 10),
            foreground="#666666"
        )
        self.status_label.grid(row=3, column=0, columnspan=2, pady=(0, 15))

        # Capture button
        self.capture_button = ttk.Button(
            main_frame,
            text="Capture Cards",
            command=self._capture_cards,
            width=20
        )
        self.capture_button.grid(row=4, column=0, pady=(0, 10))

        # Reset button
        reset_button = ttk.Button(
            main_frame,
            text="Reset",
            command=self._reset_game,
            width=20
        )
        reset_button.grid(row=4, column=1, pady=(0, 10))

        # Progress bar
        self.progress_label = ttk.Label(
            main_frame,
            text="Phase 1 of 4",
            font=("Arial", 9)
        )
        self.progress_label.grid(row=5, column=0, columnspan=2)

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def _update_phase(self):
        """Update the UI to show the current phase."""
        if self.current_phase_index < len(self.phases):
            display_name, round_name = self.phases[self.current_phase_index]
            self.game.set_betting_round(round_name)
            self.phase_label.config(text=f"--- {display_name} ---")
            self.progress_label.config(text=f"Phase {self.current_phase_index + 1} of {len(self.phases)}")
            self.status_label.config(text="Click 'Capture Cards' when ready", foreground="#666666")
        else:
            # All phases complete
            self.phase_label.config(text="Game Complete!")
            self.capture_button.config(state=tk.DISABLED)
            self.status_label.config(text="All phases captured. Click Reset to start over.", foreground="#006600")

    def _update_display(self):
        """Update the card display with actual card images."""
        card_size = (100, 140)  # Width x Height for card images

        # Update hand cards
        if self.hand_cards:
            cards = self.hand_cards.split()
            if len(cards) >= 2:
                img1 = self.card_manager.get_tk_image(cards[0], card_size)
                img2 = self.card_manager.get_tk_image(cards[1], card_size)
                if img1:
                    self.photo_images['hand1'] = img1
                    self.hand_card1_label.config(image=img1)
                if img2:
                    self.photo_images['hand2'] = img2
                    self.hand_card2_label.config(image=img2)
        else:
            # Show card backs
            back_img = self.card_manager.get_tk_image("--", card_size)
            if back_img:
                self.photo_images['hand1'] = back_img
                self.photo_images['hand2'] = back_img
                self.hand_card1_label.config(image=back_img)
                self.hand_card2_label.config(image=back_img)

        # Update flop cards
        if self.flop_cards:
            cards = self.flop_cards.split()
            if len(cards) >= 3:
                img1 = self.card_manager.get_tk_image(cards[0], card_size)
                img2 = self.card_manager.get_tk_image(cards[1], card_size)
                img3 = self.card_manager.get_tk_image(cards[2], card_size)
                if img1:
                    self.photo_images['flop1'] = img1
                    self.flop_card1_label.config(image=img1)
                if img2:
                    self.photo_images['flop2'] = img2
                    self.flop_card2_label.config(image=img2)
                if img3:
                    self.photo_images['flop3'] = img3
                    self.flop_card3_label.config(image=img3)
        else:
            # Show card backs
            back_img = self.card_manager.get_tk_image("--", card_size)
            if back_img:
                self.photo_images['flop1'] = back_img
                self.photo_images['flop2'] = back_img
                self.photo_images['flop3'] = back_img
                self.flop_card1_label.config(image=back_img)
                self.flop_card2_label.config(image=back_img)
                self.flop_card3_label.config(image=back_img)

        # Update turn card
        if self.turn_card:
            img = self.card_manager.get_tk_image(self.turn_card, card_size)
            if img:
                self.photo_images['turn'] = img
                self.turn_card_label.config(image=img)
        else:
            back_img = self.card_manager.get_tk_image("--", card_size)
            if back_img:
                self.photo_images['turn'] = back_img
                self.turn_card_label.config(image=back_img)

        # Update river card
        if self.river_card:
            img = self.card_manager.get_tk_image(self.river_card, card_size)
            if img:
                self.photo_images['river'] = img
                self.river_card_label.config(image=img)
        else:
            back_img = self.card_manager.get_tk_image("--", card_size)
            if back_img:
                self.photo_images['river'] = back_img
                self.river_card_label.config(image=back_img)

        # Update text labels
        self.hand_text_label.config(text=self.hand_cards if self.hand_cards else "")
        self.flop_text_label.config(text=self.flop_cards if self.flop_cards else "")
        self.turn_text_label.config(text=self.turn_card if self.turn_card else "")
        self.river_text_label.config(text=self.river_card if self.river_card else "")

    def _capture_cards(self):
        """Capture cards for the current phase."""
        if self.current_phase_index >= len(self.phases):
            return

        # Disable button during capture
        self.capture_button.config(state=tk.DISABLED)
        self.status_label.config(text="Capturing screenshot and detecting cards...", foreground="#0066cc")
        self.window.update()

        try:
            # Use the game's detect_hand_from_screen method
            # We need to capture the output, so we'll call it and parse results
            from ocr_reader import (
                detect_hand_from_image,
                read_flop_from_image,
                read_turn_from_image,
                read_river_from_image
            )
            import pyautogui
            import os
            from datetime import datetime

            # Take screenshot
            images_dir = "images"
            os.makedirs(images_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = os.path.join(images_dir, f'screenshot_{self.game.betting_round}_{timestamp}.png')
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)

            # Detect cards based on phase
            round_name = self.game.betting_round

            if round_name == 'preflop':
                hand, hand_str = detect_hand_from_image(screenshot_path)
                self.hand_cards = hand_str

            elif round_name == 'flop':
                hand, hand_str = detect_hand_from_image(screenshot_path)
                flop, flop_str = read_flop_from_image(screenshot_path)
                self.hand_cards = hand_str
                self.flop_cards = flop_str

            elif round_name == 'turn':
                turn, turn_str = read_turn_from_image(screenshot_path)
                self.turn_card = turn_str

            elif round_name == 'river':
                river, river_str = read_river_from_image(screenshot_path)
                self.river_card = river_str

            # Update display
            self._update_display()

            # Move to next phase
            self.current_phase_index += 1
            self._update_phase()

            # Re-enable button if not done
            if self.current_phase_index < len(self.phases):
                self.capture_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture cards:\n{str(e)}")
            self.status_label.config(text="Error during capture. Try again.", foreground="#cc0000")
            self.capture_button.config(state=tk.NORMAL)

    def _reset_game(self):
        """Reset the game to start over."""
        self.current_phase_index = 0
        self.hand_cards = ""
        self.flop_cards = ""
        self.turn_card = ""
        self.river_card = ""

        self._update_display()
        self._update_phase()
        self.capture_button.config(state=tk.NORMAL)

    def run(self):
        """Start the GUI event loop."""
        self.window.mainloop()


def main():
    """Entry point for the GUI application."""
    app = PokerOCRGui()
    app.run()


if __name__ == "__main__":
    main()
