import random


class Player:
    def __init__(self, name):
        self.name = name
        self.balance = 100  # Starting balance
        self.games_played = 0
        self.total_won = 0
        self.total_spent = 0

    def adjust_balance(self, amount):
        self.balance += amount

    def record_game(self, cost, winnings):
        self.games_played += 1
        self.total_spent += cost
        self.total_won += winnings

    def __str__(self):
        return f"{self.name}: ${self.balance:.2f}"


class LuckSimulator:
    def __init__(self):
        self.players = []
        self.current_player_index = 0

        # Scratch card configuration (easy to adjust)
        self.scratch_card_cost = 5
        self.scratch_card_prizes = {
            0: 0.70,      # 70% chance to win nothing
            2: 0.15,      # 15% chance to win $2
            10: 0.10,     # 10% chance to win $10
            25: 0.04,     # 4% chance to win $25
            100: 0.01,    # 1% chance to win $100
        }

    def setup_players(self):
        """Set up 1-4 players for the game"""
        while True:
            try:
                num_players = int(input("\nHow many players? (1-4): "))
                if 1 <= num_players <= 4:
                    break
                print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")

        for i in range(num_players):
            name = input(f"Enter name for Player {i+1}: ").strip()
            if not name:
                name = f"Player {i+1}"
            self.players.append(Player(name))

        print(f"\n{'='*50}")
        print("Players created!")
        for player in self.players:
            print(f"  {player}")
        print(f"{'='*50}\n")

    def get_current_player(self):
        """Get the current player whose turn it is"""
        return self.players[self.current_player_index]

    def next_player(self):
        """Move to the next player's turn"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def play_scratch_card(self):
        """Simulate a scratch card game"""
        player = self.get_current_player()

        print(f"\n{'-'*50}")
        print(f"SCRATCH CARD - Cost: ${self.scratch_card_cost}")
        print(f"{player.name}'s balance: ${player.balance:.2f}")
        print(f"{'-'*50}")

        if player.balance < self.scratch_card_cost:
            print(f"Sorry {player.name}, you don't have enough money!")
            input("\nPress Enter to continue...")
            return

        confirm = input(f"Buy a scratch card for ${self.scratch_card_cost}? (y/n): ").lower()
        if confirm != 'y':
            print("Cancelled.")
            input("\nPress Enter to continue...")
            return

        # Deduct cost
        player.adjust_balance(-self.scratch_card_cost)

        # Determine winnings
        rand = random.random()
        cumulative_prob = 0
        winnings = 0

        for prize, probability in self.scratch_card_prizes.items():
            cumulative_prob += probability
            if rand < cumulative_prob:
                winnings = prize
                break

        # Award winnings
        player.adjust_balance(winnings)
        player.record_game(self.scratch_card_cost, winnings)

        # Show result with some flair
        print("\nScratching...")
        print("." * 20)

        if winnings == 0:
            print("💔 Better luck next time! You won $0")
        elif winnings < self.scratch_card_cost:
            print(f"🎫 You won ${winnings}! (Net: -${self.scratch_card_cost - winnings})")
        elif winnings == self.scratch_card_cost:
            print(f"🎫 You won ${winnings}! (Break even!)")
        else:
            print(f"🎉 WINNER! You won ${winnings}! (Net: +${winnings - self.scratch_card_cost})")

        print(f"\nNew balance: ${player.balance:.2f}")
        input("\nPress Enter to continue...")

    def show_stats(self):
        """Show statistics for all players"""
        print(f"\n{'='*50}")
        print("PLAYER STATISTICS")
        print(f"{'='*50}")

        for player in self.players:
            print(f"\n{player.name}:")
            print(f"  Balance: ${player.balance:.2f}")
            print(f"  Games Played: {player.games_played}")
            print(f"  Total Spent: ${player.total_spent:.2f}")
            print(f"  Total Won: ${player.total_won:.2f}")
            if player.total_spent > 0:
                roi = ((player.total_won - player.total_spent) / player.total_spent) * 100
                print(f"  ROI: {roi:.1f}%")

        print(f"\n{'='*50}")
        input("\nPress Enter to continue...")

    def show_menu(self):
        """Display the game menu for the current player"""
        player = self.get_current_player()

        print(f"\n{'='*50}")
        print(f"{player.name}'s Turn")
        print(f"Balance: ${player.balance:.2f}")
        print(f"{'='*50}")
        print("\nWhat would you like to do?")
        print("1. Play Scratch Card")
        print("2. View Stats")
        print("3. End Turn")
        print("4. Quit Game")
        print(f"{'-'*50}")

        choice = input("Choose an option (1-4): ").strip()
        return choice

    def run(self):
        """Main game loop"""
        print("="*50)
        print("WELCOME TO LUCK SIMULATOR!")
        print("="*50)

        self.setup_players()

        game_running = True
        while game_running:
            choice = self.show_menu()

            if choice == '1':
                self.play_scratch_card()
            elif choice == '2':
                self.show_stats()
            elif choice == '3':
                print(f"\n{self.get_current_player().name} ended their turn.")
                self.next_player()
                input("Press Enter to continue...")
            elif choice == '4':
                print("\nThanks for playing!")
                self.show_stats()
                game_running = False
            else:
                print("\nInvalid choice. Please try again.")
                input("Press Enter to continue...")


if __name__ == "__main__":
    game = LuckSimulator()
    game.run()
