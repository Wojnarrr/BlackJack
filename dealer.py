from player import Player

class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer", 0)
        self.hand = []  # Single hand for the dealer
        self.up_card = None

    def deal_initial_cards(self, deck):  # Deal the dealer's initial cards
        self.hand = [deck.draw_card(), deck.draw_card()]
        self.up_card = self.hand[1]

    def should_hit(self):
        hand_value = self.get_hand_value(self.hand)
        soft_hand = any(card.rank == 'A' for card in self.hand)

        # Hit on soft 17 rule
        if hand_value < 17 or (hand_value == 17 and soft_hand):
            return True
        return False

    def play_turn(self, deck):  # Play the dealer's turn
        while self.should_hit():
            self.hit(deck)
            print(f"Dealer hits: {self.hand}")

    def hit(self, deck):
        self.hand.append(deck.draw_card())
