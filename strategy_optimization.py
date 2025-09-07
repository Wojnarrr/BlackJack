import random
from deck import Deck
from player import Player
from dealer import Dealer

class Strategy:
    def __init__(self):
        self.actions = {}
        for hand_value in range(2, 22):
            self.actions[hand_value] = {}
            for dealer_card in range(2, 12):
                self.actions[hand_value][dealer_card] = random.choice(['H', 'S', 'Dh', 'Ds', 'SP'])

    def get_action(self, hand_value, dealer_card):  # Get the action for a given hand value and dealer card
        return self.actions[hand_value].get(dealer_card, 'S')

    def set_action(self, hand_value, dealer_card, action):  # Set the action for a given hand value and dealer card
        self.actions[hand_value][dealer_card] = action

    def mutate(self):  # Mutate the strategy
        hand_value = random.choice(list(self.actions.keys()))
        dealer_card = random.choice(list(self.actions[hand_value].keys()))
        new_action = random.choice(['H', 'S', 'Dh', 'Ds', 'SP'])
        self.set_action(hand_value, dealer_card, new_action)

    def crossover(self, other_strategy):  # Crossover with another strategy
        new_strategy = Strategy()
        for hand_value in self.actions:
            for dealer_card in self.actions[hand_value]:
                if random.random() > 0.5:
                    new_strategy.set_action(hand_value, dealer_card, self.get_action(hand_value, dealer_card))
                else:
                    new_strategy.set_action(hand_value, dealer_card, other_strategy.get_action(hand_value, dealer_card))
        return new_strategy

class GeneticAlgorithm:  # Genetic algorithm for evolving strategies
    def __init__(self, population_size, mutation_rate, elitism_count):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elitism_count = elitism_count
        self.population = [Strategy() for _ in range(population_size)]

    def evolve(self, evaluate_function):  # Evolve the population
        scores = [evaluate_function(strategy) for strategy in self.population]
        best_score = min(scores)
        best_strategy = self.population[scores.index(best_score)]

        new_population = self._select_elites(scores)

        while len(new_population) < self.population_size:  # Generate new population
            parent1, parent2 = self._select_parents_tournament(scores)
            child = parent1.crossover(parent2)
            if random.random() < self.mutation_rate:
                child.mutate()
            new_population.append(child)

        self.population = new_population
        return best_strategy, best_score

    def _select_elites(self, scores):  # Select the elite strategies
        elite_indices = sorted(range(len(scores)), key=lambda k: scores[k])[:self.elitism_count]
        return [self.population[i] for i in elite_indices]

    def _select_parents_tournament(self, scores, k=3):  # Select parents using tournament selection
        selected = random.sample(list(zip(self.population, scores)), k)
        parent1 = min(selected, key=lambda x: x[1])[0]
        parent2 = min([p for p in selected if p[0] != parent1], key=lambda x: x[1])[0]
        return parent1, parent2

def evaluate_strategy(strategy, rounds=1000):  # Evaluate a strategy by playing rounds of blackjack
    deck = Deck()
    player = Player("Test Player", 1000)
    dealer = Dealer()

    total_score = 0

    for round_number in range(rounds):  # Play rounds of blackjack
        deck.reset_deck()
        player.reset_hand()
        dealer.reset_hand()

        player.deal_initial_cards(deck)
        dealer.deal_initial_cards(deck)

        while not player.is_bust(player.hands[player.current_hand_index]):  # Player's turn
            action = strategy.get_action(player.get_hand_value(player.hands[player.current_hand_index]), dealer.up_card.get_value())
            if action == 'H':
                player.hit(deck)
            elif action == 'S':
                break
            elif action == 'Dh':
                if player.can_double_down():
                    player.double_down(deck)
                    break
                else:
                    player.hit(deck)
            elif action == 'Ds':
                if player.can_double_down():
                    player.double_down(deck)
                    break
                else:
                    break
            elif action == 'SP':
                if player.can_split():
                    player.split(deck)
                else:
                    player.hit(deck)

        dealer_draws = 0
        while dealer.get_hand_value(dealer.hand) < 17 and dealer_draws < 10:
            dealer.hit(deck)
            dealer_draws += 1

        player_value = player.get_hand_value(player.hands[0])
        dealer_value = dealer.get_hand_value(dealer.hand)

        if player_value > 21:
            total_score -= 1
        elif dealer_value > 21 or player_value > dealer_value:
            total_score += 1
        elif player_value == dealer_value:
            total_score += 0
        else:
            total_score -= 1

    return -total_score
