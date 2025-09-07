import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)

    def __str__(self):
        return f"{self.rank}{self.suit[0]}"

class Deck:
    def __init__(self):
        self.cards = self.generate_deck()
        self.shuffle_deck()

    def generate_deck(self):     # Generate a deck of 52 cards
        suits = ['H', 'D', 'C', 'S']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [Card(rank, suit) for suit in suits for rank in ranks]

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw_card(self):  # Draw a single card from the deck
        if len(self.cards) == 0:
            self.reset_deck()
        return self.cards.pop()

    def reset_deck(self):  # Reset the deck by generating a new deck and shuffling it
        self.cards = self.generate_deck()
        self.shuffle_deck()

    def peek_next_card(self):  # Peek the next card in the deck
        if self.cards:
            return self.cards[-1]
        else:
            raise ValueError("The deck is empty, cannot peek the next card.")
