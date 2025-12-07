"""
Helper functions for displaying playing cards visually using Unicode symbols.

Unicode provides playing card characters that can be displayed without
needing image files.
"""

# Unicode playing card ranges
# Spades: U+1F0A1 - U+1F0AE
# Hearts: U+1F0B1 - U+1F0BE
# Diamonds: U+1F0C1 - U+1F0CE
# Clubs: U+1F0D1 - U+1F0DE

def card_to_unicode(card_str):
    """
    Convert a card string like "AS" or "10H" to a Unicode card symbol.

    Args:
        card_str: Card string in format "ranksuit" (e.g., "AS", "10H", "KD", "2C")

    Returns:
        Unicode card character (e.g., "🂡" for Ace of Spades)
    """
    if not card_str or card_str == "--":
        return "🂠"  # Card back

    card_str = card_str.strip().upper()

    # Extract rank and suit
    if len(card_str) < 2:
        return "?"

    # Handle 10 specially
    if card_str.startswith("10"):
        rank = "10"
        suit = card_str[2] if len(card_str) > 2 else ""
    else:
        rank = card_str[0]
        suit = card_str[1] if len(card_str) > 1 else ""

    # Map ranks to Unicode offsets (within each suit)
    rank_map = {
        'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 13, 'K': 14  # Note: Q=13, K=14 (12 is knight)
    }

    # Map suits to Unicode base offsets
    suit_map = {
        'S': 0x1F0A0,  # Spades
        'H': 0x1F0B0,  # Hearts
        'D': 0x1F0C0,  # Diamonds
        'C': 0x1F0D0,  # Clubs
    }

    if rank not in rank_map or suit not in suit_map:
        return "?"

    # Calculate Unicode code point
    base = suit_map[suit]
    offset = rank_map[rank]
    code_point = base + offset

    return chr(code_point)


def cards_to_unicode(cards_str):
    """
    Convert a space-separated string of cards to Unicode symbols.

    Args:
        cards_str: Space-separated cards (e.g., "AS KH 10D 2C")

    Returns:
        String with Unicode card symbols (e.g., "🂡 🂾 🃊 🃒")
    """
    if not cards_str or cards_str == "--":
        return "🂠 🂠"

    cards = cards_str.split()
    unicode_cards = [card_to_unicode(card) for card in cards]
    return " ".join(unicode_cards)


def format_hand_display(hand_str):
    """
    Format hand cards with Unicode symbols and text.

    Args:
        hand_str: Hand string like "10S JH"

    Returns:
        Formatted string like "🂪 🂻  (10S JH)"
    """
    if not hand_str or hand_str == "--":
        return "--"

    unicode_str = cards_to_unicode(hand_str)
    return f"{unicode_str}  ({hand_str})"


def format_board_display(board_str):
    """
    Format board cards with Unicode symbols.

    Args:
        board_str: Board string like "QC 9D 3C"

    Returns:
        Formatted string like "🃝 🃉 🃓"
    """
    if not board_str or board_str == "--":
        return "--"

    return cards_to_unicode(board_str)


# Color helpers for suits
def get_suit_color(suit):
    """
    Get the color for a suit (for styling).

    Args:
        suit: Suit character ('S', 'H', 'D', 'C')

    Returns:
        Color string: "red" or "black"
    """
    if suit in ['H', 'D']:
        return "red"
    return "black"
