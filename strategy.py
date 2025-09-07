import random

class Strategy:
    def __init__(self):
        self.actions = ['H', 'S', 'Dh', 'Ds', 'SP']  # Hit, Stand, Double, Double/Stand, Split
        self.strategy_matrix = self.initialize_strategy()

    def initialize_strategy(self):  # Initialize the strategy matrix
        strategy_matrix = {}
        for hand_value in range(2, 22):  # Hard totals 2-21
            strategy_matrix[hand_value] = {}
            for dealer_card in range(2, 12):  # Dealer's face-up card 2-11 (Ace is 11)
                strategy_matrix[hand_value][dealer_card] = 'S'  # Default to Stand
        return strategy_matrix

    def random_modify(self):  # Randomly modify the strategy matrix
        hand_value = random.choice(list(self.strategy_matrix.keys()))
        dealer_card = random.choice(list(self.strategy_matrix[hand_value].keys()))
        current_action = self.strategy_matrix[hand_value][dealer_card]
        new_action = random.choice([action for action in self.actions if action != current_action])
        self.strategy_matrix[hand_value][dealer_card] = new_action

    def get_action(self, hand_value, dealer_card):  # Get the action for a given hand value and dealer card
        return self.strategy_matrix[hand_value][dealer_card]

    def print_strategy(self):  # Print the strategy matrix
        for hand_value in range(2, 22):
            print(f"{hand_value}: {self.strategy_matrix[hand_value]}")

# Example usage:
strategy = Strategy()
strategy.print_strategy()
