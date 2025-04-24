from typing import List, Tuple
from .card import Card, Rank

class HandEvaluator:
    @staticmethod
    def evaluate_hand(hole_cards: List[Card], community_cards: List[Card]) -> Tuple[int, str]:
        """
        Evaluate a poker hand and return its strength and description.
        Returns a tuple of (hand_rank, hand_description)
        """
        all_cards = hole_cards + community_cards
        if len(all_cards) < 5:
            return 0, "Incomplete hand"

        # TODO: Implement hand evaluation logic
        # This will include checking for:
        # - Royal Flush
        # - Straight Flush
        # - Four of a Kind
        # - Full House
        # - Flush
        # - Straight
        # - Three of a Kind
        # - Two Pair
        # - One Pair
        # - High Card

        return 0, "High Card"  # Placeholder

    @staticmethod
    def compare_hands(hand1: List[Card], hand2: List[Card], community_cards: List[Card]) -> int:
        """
        Compare two hands and return:
        -1 if hand1 is worse than hand2
        0 if hands are equal
        1 if hand1 is better than hand2
        """
        rank1, _ = HandEvaluator.evaluate_hand(hand1, community_cards)
        rank2, _ = HandEvaluator.evaluate_hand(hand2, community_cards)
        return (rank1 > rank2) - (rank1 < rank2) 