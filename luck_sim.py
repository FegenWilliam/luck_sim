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

        # Scratch card tiers configuration (easy to adjust)
        # Tier 1: Safe - High chance to break even, low reward
        self.tier1_cost = 2
        self.tier1_prizes = {
            0: 0.10,      # 10% chance to win nothing
            2: 0.60,      # 60% chance to break even ($2)
            3: 0.20,      # 20% chance to win $3
            5: 0.08,      # 8% chance to win $5
            10: 0.02,     # 2% chance to win $10
        }

        # Tier 2: Medium - Balanced risk/reward
        self.tier2_cost = 5
        self.tier2_prizes = {
            0: 0.50,      # 50% chance to win nothing
            2: 0.20,      # 20% chance to win $2
            5: 0.15,      # 15% chance to win $5 (break even)
            10: 0.10,     # 10% chance to win $10
            25: 0.04,     # 4% chance to win $25
            100: 0.01,    # 1% chance to win $100
        }

        # Tier 3: Risky - High cost, huge payouts, but very low chance
        self.tier3_cost = 20
        self.tier3_prizes = {
            0: 0.85,      # 85% chance to win nothing
            10: 0.08,     # 8% chance to win $10
            50: 0.04,     # 4% chance to win $50
            100: 0.02,    # 2% chance to win $100
            500: 0.01,    # 1% chance to win $500
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
        print(f"SCRATCH CARD TIERS")
        print(f"{player.name}'s balance: ${player.balance:.2f}")
        print(f"{'-'*50}")
        print("\nChoose a tier:")
        print(f"1. SAFE   - ${self.tier1_cost} (High chance to break even)")
        print(f"2. MEDIUM - ${self.tier2_cost} (Balanced risk/reward)")
        print(f"3. RISKY  - ${self.tier3_cost} (High risk, high reward)")
        print("4. Cancel")
        print(f"{'-'*50}")

        tier_choice = input("Choose tier (1-4): ").strip()

        if tier_choice == '1':
            cost = self.tier1_cost
            prizes = self.tier1_prizes
            tier_name = "SAFE"
        elif tier_choice == '2':
            cost = self.tier2_cost
            prizes = self.tier2_prizes
            tier_name = "MEDIUM"
        elif tier_choice == '3':
            cost = self.tier3_cost
            prizes = self.tier3_prizes
            tier_name = "RISKY"
        elif tier_choice == '4':
            print("Cancelled.")
            input("\nPress Enter to continue...")
            return
        else:
            print("Invalid choice.")
            input("\nPress Enter to continue...")
            return

        if player.balance < cost:
            print(f"\nSorry {player.name}, you don't have enough money!")
            print(f"You need ${cost:.2f} but only have ${player.balance:.2f}")
            input("\nPress Enter to continue...")
            return

        confirm = input(f"\nBuy a {tier_name} scratch card for ${cost}? (y/n): ").lower()
        if confirm != 'y':
            print("Cancelled.")
            input("\nPress Enter to continue...")
            return

        # Deduct cost
        player.adjust_balance(-cost)

        # Determine winnings
        rand = random.random()
        cumulative_prob = 0
        winnings = 0

        for prize, probability in prizes.items():
            cumulative_prob += probability
            if rand < cumulative_prob:
                winnings = prize
                break

        # Award winnings
        player.adjust_balance(winnings)
        player.record_game(cost, winnings)

        # Show result with some flair
        print(f"\nScratching {tier_name} card...")
        print("." * 20)

        if winnings == 0:
            print("💔 Better luck next time! You won $0")
        elif winnings < cost:
            print(f"🎫 You won ${winnings}! (Net: -${cost - winnings})")
        elif winnings == cost:
            print(f"🎫 You won ${winnings}! (Break even!)")
        else:
            print(f"🎉 WINNER! You won ${winnings}! (Net: +${winnings - cost})")

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
