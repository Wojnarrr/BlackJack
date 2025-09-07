import random
import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from deck import Deck
from player import Player, EasyAIPlayer, HardAIPlayer
from dealer import Dealer
from strategy_optimization import Strategy, GeneticAlgorithm, evaluate_strategy
#The main game function
class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Game")
        self.card_images = self.load_card_images()
        self.setup_game()
        self.create_widgets()
        self.center_window(1200, 600)
        self.optimized_strategy = None

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def load_card_images(self):  # Load card images from the images folder
        card_images = {}
        card_images['Gray_back'] = ImageTk.PhotoImage(Image.open("images/Gray_back.png").convert("RGB").resize((72, 96), Image.LANCZOS))
        suits = ['H', 'D', 'C', 'S']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for rank in ranks:
                image_path = f"images/{rank}{suit}.png"
                card_image = Image.open(image_path).convert("RGB").resize((72, 96), Image.LANCZOS)
                card_images[f'{rank}{suit}'] = ImageTk.PhotoImage(card_image)
        return card_images

    def setup_game(self):  # Initialize game objects
        self.deck = Deck()
        self.player1 = Player("Player 1", 100)
        self.player2 = EasyAIPlayer("Easy AI Player", 100)
        self.player3 = HardAIPlayer("Hard AI Player", 100)
        self.dealer = Dealer()
        self.current_player = self.player1
        self.game_active = False
        self.dealer_turn = False

    def create_widgets(self):  # Create the GUI elements
        self.root.configure(bg='green')

        self.mode_frame = tk.Frame(self.root, bg='green')
        self.mode_frame.pack(pady=50)

        self.status_label = tk.Label(self.root, text="Welcome to Blackjack!", font=("Arial", 16), bg='green', fg='white')
        self.status_label.pack(pady=10)

        self.play_mode_button = ttk.Button(self.mode_frame, text="Play Mode", command=self.start_play_mode, style="TButton")
        self.play_mode_button.grid(row=0, column=0, padx=20)

        self.optimization_mode_button = ttk.Button(self.mode_frame, text="Optimization Mode", command=self.start_optimization_mode, style="TButton")
        self.optimization_mode_button.grid(row=0, column=1, padx=20)

        self.controls_frame = tk.Frame(self.root, bg='green')
        self.controls_frame.pack(side=tk.BOTTOM, pady=20)

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.map("TButton", background=[("active", "lightgreen")], foreground=[("active", "black")])

        self.start_button = ttk.Button(self.controls_frame, text="Start Game", command=self.start_game, style="TButton")
        self.start_button.grid(row=0, column=0, padx=5)
        self.start_button.grid_remove()

        self.hit_button = ttk.Button(self.controls_frame, text="Hit", command=self.hit, style="TButton")
        self.hit_button.grid(row=0, column=1, padx=5)
        self.hit_button.grid_remove()

        self.stand_button = ttk.Button(self.controls_frame, text="Stand", command=self.stand, style="TButton")
        self.stand_button.grid(row=0, column=2, padx=5)
        self.stand_button.grid_remove()

        self.double_button = ttk.Button(self.controls_frame, text="Double Down", command=self.double_down, style="TButton")
        self.double_button.grid(row=0, column=3, padx=5)
        self.double_button.grid_remove()

        self.split_button = ttk.Button(self.controls_frame, text="Split", command=self.split, style="TButton")
        self.split_button.grid(row=0, column=4, padx=5)
        self.split_button.grid_remove()

        self.hint_button = ttk.Button(self.controls_frame, text="Hint", command=self.show_hint, style="TButton")
        self.hint_button.grid(row=0, column=5, padx=5)
        self.hint_button.grid_remove()

        self.next_round_button = ttk.Button(self.controls_frame, text="Next Round", command=self.prompt_for_new_round, style="TButton")
        self.next_round_button.grid(row=0, column=6, padx=5)
        self.next_round_button.grid_remove()

        self.dealer_frame = tk.Frame(self.root, bg='green')
        self.dealer_label = tk.Label(self.dealer_frame, text="Dealer's Hand", font=("Arial", 14), bg='green', fg='white')
        self.dealer_label.pack()

        self.players_frame = tk.Frame(self.root, bg='green')

        self.player1_frame = tk.Frame(self.players_frame, bg='green')
        self.player1_hand_frame = tk.Frame(self.player1_frame, bg='green')
        self.player1_hand_frame.pack(pady=(0, 10))
        self.player1_label = tk.Label(self.player1_frame, text="Player 1's Hand", font=("Arial", 14), bg='green', fg='white')
        self.player1_label.pack()
        self.player1_balance_label = tk.Label(self.player1_frame, text=f"Balance: €{self.player1.balance}", font=("Arial", 12), bg='green', fg='white')
        self.player1_balance_label.pack()

        self.player2_frame = tk.Frame(self.players_frame, bg='green')
        self.player2_hand_frame = tk.Frame(self.player2_frame, bg='green')
        self.player2_hand_frame.pack(pady=(0, 10))
        self.player2_label = tk.Label(self.player2_frame, text="Easy AI Player's Hand", font=("Arial", 14), bg='green', fg='white')
        self.player2_label.pack()
        self.player2_balance_label = tk.Label(self.player2_frame, text=f"Balance: €{self.player2.balance}", font=("Arial", 12), bg='green', fg='white')
        self.player2_balance_label.pack()

        self.player3_frame = tk.Frame(self.players_frame, bg='green')
        self.player3_hand_frame = tk.Frame(self.player3_frame, bg='green')
        self.player3_hand_frame.pack(pady=(0, 10))
        self.player3_label = tk.Label(self.player3_frame, text="Hard AI Player's Hand", font=("Arial", 14), bg='green', fg='white')
        self.player3_label.pack()
        self.player3_balance_label = tk.Label(self.player3_frame, text=f"Balance: €{self.player3.balance}", font=("Arial", 12), bg='green', fg='white')
        self.player3_balance_label.pack()

        self.bet_frame = tk.Frame(self.root, bg='green')
        self.bet_label1 = tk.Label(self.bet_frame, text="Player 1 Bet:", font=("Arial", 12), bg='green', fg='white')
        self.bet_label1.grid(row=0, column=0)
        self.bet_entry1 = tk.Entry(self.bet_frame)
        self.bet_entry1.grid(row=0, column=1)

        self.bet_label2 = tk.Label(self.bet_frame, text="Easy AI Player Bet:", font=("Arial", 12), bg='green', fg='white')
        self.bet_label2.grid(row=1, column=0)
        self.bet_entry2 = tk.Entry(self.bet_frame)
        self.bet_entry2.grid(row=1, column=1)

        self.bet_label3 = tk.Label(self.bet_frame, text="Hard AI Player Bet:", font=("Arial", 12), bg='green', fg='white')
        self.bet_label3.grid(row=2, column=0)
        self.bet_entry3 = tk.Entry(self.bet_frame)
        self.bet_entry3.grid(row=2, column=1)

        self.place_bet_button = ttk.Button(self.bet_frame, text="Place Bets", command=self.place_bets, style="TButton")
        self.place_bet_button.grid(row=3, column=0, columnspan=2, pady=10)

    def start_play_mode(self):  # Switch to play mode
        self.mode_frame.pack_forget()
        self.start_button.grid()

    def start_optimization_mode(self):  # Switch to optimization mode
        self.mode_frame.pack_forget()
        self.status_label.config(text="Optimizing strategy, please wait...")
        self.root.after(100, self.optimize_strategy)

    def start_game(self):  # Start a new game
        self.start_button.grid_remove()
        self.show_betting_controls()

    def show_betting_controls(self):  # Show betting controls
        self.bet_frame.pack(pady=10)
        self.status_label.config(text="Place your bets for the next round!")

    def place_bets(self):  # Place bets for the next round
        try:
            bet1 = int(self.bet_entry1.get())
            bet2 = int(self.bet_entry2.get())
            bet3 = int(self.bet_entry3.get())
            self.player1.place_bet(bet1)
            self.player2.place_bet(bet2)
            self.player3.place_bet(bet3)
            self.bet_frame.pack_forget()
            self.begin_round()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid bet amounts.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def begin_round(self):  # Start a new round
        self.clear_display()
        self.hit_button.grid()
        self.stand_button.grid()
        self.double_button.grid()
        self.split_button.grid()
        self.hint_button.grid()

        self.dealer_frame.pack(pady=10)
        self.players_frame.pack(pady=10, expand=True)

        self.player1_frame.pack(side=tk.LEFT, padx=20)
        self.player2_frame.pack(side=tk.LEFT, padx=20)
        self.player3_frame.pack(side=tk.LEFT, padx=20)

        self.dealer_turn = False
        self.deck.reset_deck()
        self.dealer.deal_initial_cards(self.deck)
        self.player1.deal_initial_cards(self.deck)
        self.player2.deal_initial_cards(self.deck)
        self.player3.deal_initial_cards(self.deck)
        self.current_player = self.player1
        self.game_active = True
        self.update_display()

    def hit(self):  # Player hits
        if self.game_active:
            self.current_player.hit(self.deck)
            self.update_display()
            if self.current_player.is_bust(self.current_player.hands[self.current_player.current_hand_index]):
                messagebox.showinfo("Bust!", f"{self.current_player.name} has gone bust!")
                self.end_turn()

    def stand(self):  # Player stands
        if self.game_active:
            self.end_turn()

    def double_down(self):  # Player doubles down
        if self.game_active:
            try:
                doubled_down = self.current_player.double_down(self.deck)
                self.update_display()
                if doubled_down:
                    self.end_turn()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def split(self):  # Player splits
        if self.game_active:
            try:
                self.current_player.split(self.deck)
                self.update_display()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def show_hint(self):
        if self.game_active:
            player_hand = self.current_player.hands[self.current_player.current_hand_index]
            dealer_up_card = self.dealer.up_card
            hint = self.basic_strategy(player_hand, dealer_up_card)
            messagebox.showinfo("Hint", hint)

    def end_turn(self):  # End the current player's turn
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.play_ai_turn(self.player2)
        elif self.current_player == self.player2:
            self.current_player = self.player3
            self.play_ai_turn(self.player3)
        elif self.current_player == self.player3:
            self.dealer_turn = True
            self.dealer.play_turn(self.deck)
            self.determine_outcome()
            self.game_active = False
            self.show_next_round_button()
        else:
            self.current_player = self.player1
        self.update_display()

    def play_ai_turn(self, player):  # Play the AI player's turn
        player.play_turn(self.deck, self.dealer.up_card)
        self.update_display()
        if not self.game_active:  # Prevent infinite loops
            return
        self.end_turn()

    def determine_outcome(self):  # Determine the outcome of the round
        player1_outcomes = self.get_player_outcomes(self.player1)
        player2_outcomes = self.get_player_outcomes(self.player2)
        player3_outcomes = self.get_player_outcomes(self.player3)

        outcomes = player1_outcomes + player2_outcomes + player3_outcomes
        self.status_label.config(text=" ".join(outcomes))

    def get_player_outcomes(self, player):  # Get the outcomes for a player
        outcomes = []
        for hand in player.hands:
            hand_value = player.get_hand_value(hand)
            dealer_value = self.dealer.get_hand_value(self.dealer.hand)

            if hand_value > 21:
                outcomes.append(f"{player.name} busts.")
            elif dealer_value > 21 or hand_value > dealer_value:
                outcomes.append(f"{player.name} wins!")
                player.win_bet()
            elif hand_value == dealer_value:
                outcomes.append(f"{player.name} pushes.")
                player.push_bet()
            else:
                outcomes.append(f"{player.name} loses.")
                player.lose_bet()

        return outcomes

    def show_next_round_button(self):  # Show the next round button
        self.hit_button.grid_remove()
        self.stand_button.grid_remove()
        self.double_button.grid_remove()
        self.split_button.grid_remove()
        self.hint_button.grid_remove()
        self.next_round_button.grid()

    def prompt_for_new_round(self):  # Prompt the user to start a new round
        self.next_round_button.grid_remove()
        self.bet_frame.pack(pady=10)
        self.status_label.config(text="Place your bets for the next round!")
        self.reset_game()

    def reset_game(self):  # Reset the game state
        self.player1.reset_hand()
        self.player2.reset_hand()
        self.player3.reset_hand()
        self.dealer.reset_hand()
        self.clear_display()
        self.update_display()

    def clear_display(self):  # Clear the display
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()
        for widget in self.player1_hand_frame.winfo_children():
            widget.destroy()
        for widget in self.player2_hand_frame.winfo_children():
            widget.destroy()
        for widget in self.player3_hand_frame.winfo_children():
            widget.destroy()

    def update_display(self):  # Update the display
        self.clear_display()

        for i, card in enumerate(self.dealer.hand):
            if self.dealer_turn or i != 0:
                card_text = f"{card.rank}{card.suit[0]}"
            else:
                card_text = "Gray_back"
            card_label = tk.Label(self.dealer_frame, image=self.card_images[card_text], bg='green')
            card_label.pack(side=tk.LEFT, padx=5)

        self.display_player_hands(self.player1, self.player1_hand_frame)
        self.display_player_hands(self.player2, self.player2_hand_frame)
        self.display_player_hands(self.player3, self.player3_hand_frame)

        self.player1_balance_label.config(text=f"Balance: €{self.player1.balance}")
        self.player2_balance_label.config(text=f"Balance: €{self.player2.balance}")
        self.player3_balance_label.config(text=f"Balance: €{self.player3.balance}")

    def display_player_hands(self, player, frame):  # Display the player hands
        for hand in player.hands:
            hand_frame = tk.Frame(frame, bg='green')
            hand_frame.pack()
            for card in hand:
                card_text = f"{card.rank}{card.suit[0]}"
                card_label = tk.Label(hand_frame, image=self.card_images[card_text], bg='green')
                card_label.pack(side=tk.LEFT, padx=5)

    def optimize_strategy(self):  # Optimize the strategy using a genetic algorithm
        population_size = 100
        mutation_rate = 0.1
        elitism_count = 5
        generations = 200

        ga = GeneticAlgorithm(population_size=population_size, mutation_rate=mutation_rate, elitism_count=elitism_count)

        best_strategy, best_cost = None, float('inf')
        for generation in range(generations):  # Evolve the population
            strategy, cost = ga.evolve(evaluate_strategy)  # Evaluate the strategy
            if cost < best_cost:  # Keep track of the best strategy
                best_strategy, best_cost = strategy, cost
            print(f"Generation {generation}: Best Cost {best_cost}, Current Cost {cost}")

        self.optimized_strategy = best_strategy
        self.display_optimized_strategy()

    def display_optimized_strategy(self):  # Display the optimized strategy
        self.clear_display()
        self.status_label.config(text="Optimized Strategy:")
        strategy_frame = tk.Frame(self.root, bg='green')
        strategy_frame.pack(pady=10)

        for hand_value in range(2, 22):
            strategy_row = tk.Frame(strategy_frame, bg='green')
            strategy_row.pack()
            tk.Label(strategy_row, text=f"{hand_value}: ", bg='green', fg='white', font=("Arial", 12)).pack(
                side=tk.LEFT)
            for dealer_card in range(2, 12):
                action = self.optimized_strategy.get_action(hand_value, dealer_card)
                tk.Label(strategy_row, text=action, bg='green', fg='white', font=("Arial", 12), padx=2).pack(
                    side=tk.LEFT)

    def basic_strategy(self, player_hand, dealer_up_card):
        player_value = self.current_player.get_hand_value(player_hand)
        dealer_value = dealer_up_card.get_value()

        # Define the basic strategy table
        strategy_table = {
            'hard': {
                (5, 8): 'H',
                (9, 9): 'Dh',
                (10, 10): 'Dh',
                (11, 11): 'Dh',
                (12, 3): 'H', (12, 4): 'S', (12, 5): 'S', (12, 6): 'S', (12, 2): 'H', (12, 7): 'H', (12, 8): 'H',
                (12, 9): 'H', (12, 10): 'H', (12, 11): 'H',
                (13, 6): 'S', (13, 2): 'S', (13, 3): 'S', (13, 4): 'S', (13, 5): 'S', (13, 7): 'H', (13, 8): 'H',
                (13, 9): 'H', (13, 10): 'H', (13, 11): 'H',
                (14, 6): 'S', (14, 2): 'S', (14, 3): 'S', (14, 4): 'S', (14, 5): 'S', (14, 7): 'H', (14, 8): 'H',
                (14, 9): 'H', (14, 10): 'H', (14, 11): 'H',
                (15, 6): 'S', (15, 2): 'S', (15, 3): 'S', (15, 4): 'S', (15, 5): 'S', (15, 7): 'H', (15, 8): 'H',
                (15, 9): 'H', (15, 10): 'H', (15, 11): 'H',
                (16, 6): 'S', (16, 2): 'S', (16, 3): 'S', (16, 4): 'S', (16, 5): 'S', (16, 7): 'H', (16, 8): 'H',
                (16, 9): 'H', (16, 10): 'H', (16, 11): 'H',
                (17, 17): 'S',
                (18, 18): 'S',
                (19, 19): 'S',
                (20, 20): 'S',
                (21, 21): 'S'
            },
            'soft': {
                (13, 2): 'H', (13, 3): 'H', (13, 4): 'H', (13, 5): 'Dh', (13, 6): 'Dh', (13, 7): 'H', (13, 8): 'H',
                (13, 9): 'H', (13, 10): 'H', (13, 11): 'H',
                (14, 2): 'H', (14, 3): 'H', (14, 4): 'H', (14, 5): 'Dh', (14, 6): 'Dh', (14, 7): 'H', (14, 8): 'H',
                (14, 9): 'H', (14, 10): 'H', (14, 11): 'H',
                (15, 2): 'H', (15, 3): 'H', (15, 4): 'Dh', (15, 5): 'Dh', (15, 6): 'Dh', (15, 7): 'H', (15, 8): 'H',
                (15, 9): 'H', (15, 10): 'H', (15, 11): 'H',
                (16, 2): 'H', (16, 3): 'H', (16, 4): 'Dh', (16, 5): 'Dh', (16, 6): 'Dh', (16, 7): 'H', (16, 8): 'H',
                (16, 9): 'H', (16, 10): 'H', (16, 11): 'H',
                (17, 2): 'H', (17, 3): 'Dh', (17, 4): 'Dh', (17, 5): 'Dh', (17, 6): 'Dh', (17, 7): 'H', (17, 8): 'H',
                (17, 9): 'H', (17, 10): 'H', (17, 11): 'H',
                (18, 2): 'S', (18, 3): 'Dh', (18, 4): 'Dh', (18, 5): 'Dh', (18, 6): 'Dh', (18, 7): 'S', (18, 8): 'S',
                (18, 9): 'H', (18, 10): 'H', (18, 11): 'H',
                (19, 2): 'S', (19, 3): 'S', (19, 4): 'S', (19, 5): 'S', (19, 6): 'Dh', (19, 7): 'S', (19, 8): 'S',
                (19, 9): 'S', (19, 10): 'S', (19, 11): 'S',
                (20, 20): 'S',
                (21, 21): 'S'
            },
            'pair': {
                (2, 2): 'SP', (2, 3): 'SP', (2, 4): 'SP', (2, 5): 'SP', (2, 6): 'SP', (2, 7): 'SP', (2, 8): 'H',
                (2, 9): 'H', (2, 10): 'H', (2, 11): 'H',
                (3, 2): 'SP', (3, 3): 'SP', (3, 4): 'SP', (3, 5): 'SP', (3, 6): 'SP', (3, 7): 'SP', (3, 8): 'H',
                (3, 9): 'H', (3, 10): 'H', (3, 11): 'H',
                (4, 2): 'H', (4, 3): 'H', (4, 4): 'H', (4, 5): 'SP', (4, 6): 'SP', (4, 7): 'H', (4, 8): 'H',
                (4, 9): 'H',
                (4, 10): 'H', (4, 11): 'H',
                (5, 2): 'Dh', (5, 3): 'Dh', (5, 4): 'Dh', (5, 5): 'Dh', (5, 6): 'Dh', (5, 7): 'Dh', (5, 8): 'Dh',
                (5, 9): 'Dh', (5, 10): 'H', (5, 11): 'H',
                (6, 2): 'SP', (6, 3): 'SP', (6, 4): 'SP', (6, 5): 'SP', (6, 6): 'SP', (6, 7): 'SP', (6, 8): 'H',
                (6, 9): 'H', (6, 10): 'H', (6, 11): 'H',
                (7, 2): 'SP', (7, 3): 'SP', (7, 4): 'SP', (7, 5): 'SP', (7, 6): 'SP', (7, 7): 'SP', (7, 8): 'H',
                (7, 9): 'H', (7, 10): 'H', (7, 11): 'H',
                (8, 8): 'SP',
                (9, 2): 'SP', (9, 3): 'SP', (9, 4): 'SP', (9, 5): 'SP', (9, 6): 'SP', (9, 7): 'S', (9, 8): 'SP',
                (9, 9): 'SP', (9, 10): 'S', (9, 11): 'S',
                (10, 10): 'S',
                (11, 11): 'SP'
            }
        }

        # Determine the type of hand (hard, soft, pair)
        hand_type = 'hard'
        if self.current_player.has_ace(player_hand) and player_value <= 11:
            hand_type = 'soft'
        elif len(player_hand) == 2 and player_hand[0].rank == player_hand[1].rank:
            hand_type = 'pair'

        # Get the action from the strategy table
        action = strategy_table[hand_type].get((player_value, dealer_value), 'S')
        return action


if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()
