class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.hands = [[]]
        self.current_hand_index = 0
        self.stake = 0

    def reset_hand(self):
        self.hands = [[]]
        self.current_hand_index = 0

    def deal_initial_cards(self, deck):
        self.hands[0] = [deck.draw_card(), deck.draw_card()]

    def get_hand_value(self, hand):  # Calculate the value of a hand
        value = 0
        ace_count = 0
        for card in hand:
            if card.rank in ['J', 'Q', 'K']:
                value += 10
            elif card.rank == 'A':
                ace_count += 1
                value += 11
            else:
                value += int(card.rank)

        while value > 21 and ace_count:
            value -= 10
            ace_count -= 1

        return value

    def is_bust(self, hand):
        return self.get_hand_value(hand) > 21

    def hit(self, deck):
        self.hands[self.current_hand_index].append(deck.draw_card())

    def stand(self):
        pass

    def double_down(self, deck):
        if not self.can_double_down():
            raise ValueError("Cannot double down.")
        self.stake *= 2
        self.hit(deck)

    def split(self, deck):
        if not self.can_split():
            raise ValueError("Can only split pairs.")
        hand = self.hands[self.current_hand_index]
        new_hand = [hand.pop()]
        self.hands.append(new_hand)
        self.hands[self.current_hand_index].append(deck.draw_card())
        self.hands[-1].append(deck.draw_card())

    def can_double_down(self):
        hand = self.hands[self.current_hand_index]
        return len(hand) == 2 and self.balance >= self.stake * 2

    def can_split(self):
        hand = self.hands[self.current_hand_index]
        return len(hand) == 2 and hand[0].rank == hand[1].rank and self.balance >= self.stake * 2

    def place_bet(self, amount):
        if amount > self.balance or amount <= 0:
            raise ValueError("Invalid bet amount.")
        self.stake = amount
        self.balance -= amount

    def win_bet(self):
        self.balance += self.stake * 2

    def push_bet(self):
        self.balance += self.stake

    def lose_bet(self):
        self.stake = 0

    def basic_strategy_action(self, dealer_up_card):  # Basic strategy action
        hand_value = self.get_hand_value(self.hands[self.current_hand_index])
        dealer_value = dealer_up_card.get_value()

        if len(self.hands[self.current_hand_index]) == 2 and self.hands[self.current_hand_index][0].rank == self.hands[self.current_hand_index][1].rank:
            # Pair
            return self.get_pair_action(self.hands[self.current_hand_index][0].rank, dealer_value)
        elif 'A' in [card.rank for card in self.hands[self.current_hand_index]] and hand_value <= 21:
            # Soft total
            return self.get_soft_total_action(hand_value, dealer_value)
        else:
            # Hard total
            return self.get_hard_total_action(hand_value, dealer_value)

    def get_pair_action(self, pair_rank, dealer_value):  # Get pair action
        pair_actions = {
            'A': 'SP', '10': 'S', '9': 'SP' if dealer_value not in [7, 10, 11] else 'S',
            '8': 'SP', '7': 'SP' if dealer_value < 8 else 'H', '6': 'SP' if dealer_value < 7 else 'H',
            '5': 'Dh' if dealer_value < 10 else 'H', '4': 'SP' if dealer_value in [5, 6] else 'H',
            '3': 'SP' if dealer_value < 8 else 'H', '2': 'SP' if dealer_value < 8 else 'H'
        }
        return pair_actions.get(pair_rank, 'H')

    def get_soft_total_action(self, hand_value, dealer_value):  # Get soft total action
        soft_actions = {
            20: 'S', 19: 'S', 18: 'Ds' if dealer_value in [2, 7, 8] else 'S' if dealer_value in [9, 10, 11] else 'Dh',
            17: 'Dh' if dealer_value in [3, 4, 5, 6] else 'H',
            16: 'Dh' if dealer_value in [4, 5, 6] else 'H', 15: 'Dh' if dealer_value in [4, 5, 6] else 'H',
            14: 'Dh' if dealer_value in [5, 6] else 'H', 13: 'Dh' if dealer_value in [5, 6] else 'H'
        }
        return soft_actions.get(hand_value, 'H')

    def get_hard_total_action(self, hand_value, dealer_value):  # Get hard total action
        hard_actions = {
            17: 'S', 16: 'S' if dealer_value < 7 else 'H', 15: 'S' if dealer_value < 7 else 'H',
            14: 'S' if dealer_value < 7 else 'H', 13: 'S' if dealer_value < 7 else 'H',
            12: 'S' if dealer_value in [4, 5, 6] else 'H',
            11: 'Dh', 10: 'Dh' if dealer_value < 10 else 'H', 9: 'Dh' if dealer_value in [3, 4, 5, 6] else 'H',
            8: 'H', 7: 'H', 6: 'H', 5: 'H', 4: 'H', 3: 'H', 2: 'H'
        }
        return hard_actions.get(hand_value, 'H')

    def cheat_action(self, deck, dealer_up_card):  # Cheat action
        next_card = deck.peek_next_card()
        current_hand = self.hands[self.current_hand_index]
        if self.is_bust(current_hand + [next_card]):
            return 'S'  # Stand to avoid busting
        return 'H'  # Hit because it won't bust

    def has_ace(self, player_hand):
        return any(card.rank == 'A' for card in player_hand)

class EasyAIPlayer(Player):  # Easy AI player
    def __init__(self, name, balance):
        super().__init__(name, balance)

    def play_turn(self, deck, dealer_up_card):  # Play turn
        while True:
            action = self.basic_strategy_action(dealer_up_card)
            if action == 'H':
                self.hit(deck)
            elif action == 'S':
                break  # Stand
            elif action == 'Dh' or action == 'Ds':
                self.double_down(deck)
                break
            elif action == 'SP':
                self.split(deck)
            if self.is_bust(self.hands[self.current_hand_index]):
                break  # End turn if bust

class HardAIPlayer(Player):  # Hard AI player
    def __init__(self, name, balance):
        super().__init__(name, balance)

    def play_turn(self, deck, dealer_up_card):  # Play turn
        while True:
            action = self.cheat_action(deck, dealer_up_card)
            if action == 'H':
                self.hit(deck)
            elif action == 'S':
                break  # Stand
            if self.is_bust(self.hands[self.current_hand_index]):
                break  # End turn if bust
