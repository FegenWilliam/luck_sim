import random


class Player:
    def __init__(self, name, starting_balance=500):
        self.name = name
        self.balance = starting_balance
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


class ScratchTicket:
    """Represents a single scratch ticket with a predetermined prize"""
    def __init__(self, tier, cost, prize):
        self.tier = tier
        self.cost = cost
        self.prize = prize
        self.scratched = False


class Distributor(Player):
    """Distributor manages and sells scratch tickets to other players"""
    def __init__(self, name):
        super().__init__(name, starting_balance=50000)
        self.tickets_tier1 = []
        self.tickets_tier2 = []
        self.tickets_tier3 = []
        self.tickets_sold = 0
        self.revenue = 0

    def allocate_tickets(self, tier, cost, prize_distribution, count, creation_cost_per_ticket):
        """Allocate tickets for a specific tier with given prize distribution"""
        tickets = []
        for prize, num_tickets in prize_distribution.items():
            for _ in range(num_tickets):
                tickets.append(ScratchTicket(tier, cost, prize))

        # Charge the distributor for creating these tickets
        total_creation_cost = len(tickets) * creation_cost_per_ticket
        self.adjust_balance(-total_creation_cost)

        # Shuffle to randomize ticket order
        random.shuffle(tickets)

        if tier == 1:
            self.tickets_tier1.extend(tickets)
        elif tier == 2:
            self.tickets_tier2.extend(tickets)
        elif tier == 3:
            self.tickets_tier3.extend(tickets)

        return len(tickets), total_creation_cost

    def get_ticket_inventory(self, tier):
        """Get available tickets for a tier"""
        if tier == 1:
            return [t for t in self.tickets_tier1 if not t.scratched]
        elif tier == 2:
            return [t for t in self.tickets_tier2 if not t.scratched]
        elif tier == 3:
            return [t for t in self.tickets_tier3 if not t.scratched]
        return []

    def sell_ticket(self, tier, cost):
        """Sell a ticket to a player and return it"""
        available = self.get_ticket_inventory(tier)
        if not available:
            return None

        ticket = available[0]
        ticket.scratched = True
        self.tickets_sold += 1
        self.revenue += cost
        # Distributor receives the cost of the ticket
        self.adjust_balance(cost)
        # Distributor pays out the winnings
        self.adjust_balance(-ticket.prize)
        return ticket

    def __str__(self):
        return f"{self.name} (DISTRIBUTOR): ${self.balance:.2f}"


class LuckSimulator:
    def __init__(self):
        self.players = []
        self.distributor = None
        self.current_player_index = 0

        # Ticket creation cost (what distributor pays to make tickets)
        self.ticket_creation_cost = 0.10  # $0.10 per ticket

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
        """Set up 4 players for the game (1 distributor + 3 regular players)"""
        print("\nSetting up 4 players (1 distributor + 3 regular players)")
        print("The distributor manages tickets and starts with $50,000")
        print("Regular players start with $500\n")

        # Setup distributor
        name = input("Enter name for Distributor: ").strip()
        if not name:
            name = "Distributor"
        self.distributor = Distributor(name)
        self.players.append(self.distributor)

        # Setup 3 regular players
        for i in range(3):
            name = input(f"Enter name for Player {i+1}: ").strip()
            if not name:
                name = f"Player {i+1}"
            self.players.append(Player(name))

        print(f"\n{'='*50}")
        print("Players created!")
        for player in self.players:
            print(f"  {player}")
        print(f"{'='*50}\n")

        # Distributor allocates tickets
        self.distributor_allocate_tickets()

    def distributor_allocate_tickets(self, is_initial=True):
        """Allow distributor to allocate ticket prizes for each tier"""
        print(f"\n{'='*50}")
        print("DISTRIBUTOR TICKET ALLOCATION")
        print(f"{'='*50}")
        print(f"{self.distributor.name}, you will now allocate scratch tickets.")
        print(f"Cost to create tickets: ${self.ticket_creation_cost:.2f} per ticket")
        print(f"Current balance: ${self.distributor.balance:.2f}")
        print("Specify how many tickets of each prize amount you want to create.\n")

        # Tier 1 allocation
        print(f"\n{'-'*50}")
        print(f"TIER 1: LUCKY PENNY (Cost: ${self.tier1_cost})")
        print(f"{'-'*50}")
        tier1_allocation = {}
        tier1_allocation[0] = int(input("How many $0 prize tickets? "))
        tier1_allocation[2] = int(input("How many $2 prize tickets? "))
        tier1_allocation[3] = int(input("How many $3 prize tickets? "))
        tier1_allocation[5] = int(input("How many $5 prize tickets? "))
        tier1_allocation[10] = int(input("How many $10 prize tickets? "))

        # Tier 2 allocation
        print(f"\n{'-'*50}")
        print(f"TIER 2: HIGH ROLLER (Cost: ${self.tier2_cost})")
        print(f"{'-'*50}")
        tier2_allocation = {}
        tier2_allocation[0] = int(input("How many $0 prize tickets? "))
        tier2_allocation[2] = int(input("How many $2 prize tickets? "))
        tier2_allocation[5] = int(input("How many $5 prize tickets? "))
        tier2_allocation[10] = int(input("How many $10 prize tickets? "))
        tier2_allocation[25] = int(input("How many $25 prize tickets? "))
        tier2_allocation[100] = int(input("How many $100 prize tickets? "))

        # Tier 3 allocation
        print(f"\n{'-'*50}")
        print(f"TIER 3: YOLO SPECIAL (Cost: ${self.tier3_cost})")
        print(f"{'-'*50}")
        tier3_allocation = {}
        tier3_allocation[0] = int(input("How many $0 prize tickets? "))
        tier3_allocation[10] = int(input("How many $10 prize tickets? "))
        tier3_allocation[50] = int(input("How many $50 prize tickets? "))
        tier3_allocation[100] = int(input("How many $100 prize tickets? "))
        tier3_allocation[500] = int(input("How many $500 prize tickets? "))

        # Create tickets
        count1, cost1 = self.distributor.allocate_tickets(1, self.tier1_cost, tier1_allocation,
                                                           sum(tier1_allocation.values()), self.ticket_creation_cost)
        count2, cost2 = self.distributor.allocate_tickets(2, self.tier2_cost, tier2_allocation,
                                                           sum(tier2_allocation.values()), self.ticket_creation_cost)
        count3, cost3 = self.distributor.allocate_tickets(3, self.tier3_cost, tier3_allocation,
                                                           sum(tier3_allocation.values()), self.ticket_creation_cost)

        total_cost = cost1 + cost2 + cost3
        total_tickets = count1 + count2 + count3

        print(f"\n{'='*50}")
        print("TICKETS ALLOCATED!")
        print(f"Tier 1 (LUCKY PENNY): {count1} tickets (Cost: ${cost1:.2f})")
        print(f"Tier 2 (HIGH ROLLER): {count2} tickets (Cost: ${cost2:.2f})")
        print(f"Tier 3 (YOLO SPECIAL): {count3} tickets (Cost: ${cost3:.2f})")
        print(f"Total: {total_tickets} tickets for ${total_cost:.2f}")
        print(f"New balance: ${self.distributor.balance:.2f}")
        print(f"{'='*50}")

        if is_initial:
            input("\nPress Enter to start the game...")
        else:
            input("\nPress Enter to continue...")

    def get_current_player(self):
        """Get the current player whose turn it is"""
        return self.players[self.current_player_index]

    def next_player(self):
        """Move to the next player's turn"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def play_scratch_card(self):
        """Simulate a scratch card game - buy from distributor's inventory"""
        player = self.get_current_player()

        # Distributor cannot buy their own tickets
        if player == self.distributor:
            print(f"\n{self.distributor.name}, you are the distributor and cannot buy tickets!")
            print("You can view your sales stats instead.")
            input("\nPress Enter to continue...")
            return

        print(f"\n{'-'*50}")
        print(f"SCRATCH CARD TIERS")
        print(f"{player.name}'s balance: ${player.balance:.2f}")
        print(f"{'-'*50}")

        # Show available inventory
        tier1_available = len(self.distributor.get_ticket_inventory(1))
        tier2_available = len(self.distributor.get_ticket_inventory(2))
        tier3_available = len(self.distributor.get_ticket_inventory(3))

        print("\nChoose a tier:")
        print(f"1. LUCKY PENNY     - ${self.tier1_cost} ({tier1_available} available)")
        print(f"2. HIGH ROLLER     - ${self.tier2_cost} ({tier2_available} available)")
        print(f"3. YOLO SPECIAL    - ${self.tier3_cost} ({tier3_available} available)")
        print("4. Cancel")
        print(f"{'-'*50}")

        tier_choice = input("Choose tier (1-4): ").strip()

        if tier_choice == '1':
            tier = 1
            cost = self.tier1_cost
            tier_name = "LUCKY PENNY"
        elif tier_choice == '2':
            tier = 2
            cost = self.tier2_cost
            tier_name = "HIGH ROLLER"
        elif tier_choice == '3':
            tier = 3
            cost = self.tier3_cost
            tier_name = "YOLO SPECIAL"
        elif tier_choice == '4':
            print("Cancelled.")
            input("\nPress Enter to continue...")
            return
        else:
            print("Invalid choice.")
            input("\nPress Enter to continue...")
            return

        # Check if tickets are available
        if len(self.distributor.get_ticket_inventory(tier)) == 0:
            print(f"\nSorry, no {tier_name} tickets available!")
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

        # Deduct cost from player
        player.adjust_balance(-cost)

        # Buy ticket from distributor
        ticket = self.distributor.sell_ticket(tier, cost)

        if ticket is None:
            print("Error: Ticket unavailable!")
            player.adjust_balance(cost)  # Refund
            input("\nPress Enter to continue...")
            return

        winnings = ticket.prize

        # Award winnings to player
        player.adjust_balance(winnings)
        player.record_game(cost, winnings)

        # Show result with some flair
        print(f"\nScratching {tier_name} card...")
        print("." * 20)

        if winnings == 0:
            print("Better luck next time! You won $0")
        elif winnings < cost:
            print(f"You won ${winnings}! (Net: -${cost - winnings})")
        elif winnings == cost:
            print(f"You won ${winnings}! (Break even!)")
        else:
            print(f"WINNER! You won ${winnings}! (Net: +${winnings - cost})")

        print(f"\nYour new balance: ${player.balance:.2f}")
        print(f"{self.distributor.name}'s new balance: ${self.distributor.balance:.2f}")
        input("\nPress Enter to continue...")

    def show_stats(self):
        """Show statistics for all players"""
        print(f"\n{'='*50}")
        print("PLAYER STATISTICS")
        print(f"{'='*50}")

        for player in self.players:
            if player == self.distributor:
                print(f"\n{player.name} (DISTRIBUTOR):")
                print(f"  Balance: ${player.balance:.2f}")
                print(f"  Tickets Sold: {self.distributor.tickets_sold}")
                print(f"  Revenue: ${self.distributor.revenue:.2f}")
                print(f"  Profit: ${player.balance - 50000:.2f}")

                # Show remaining inventory
                tier1_remaining = len(self.distributor.get_ticket_inventory(1))
                tier2_remaining = len(self.distributor.get_ticket_inventory(2))
                tier3_remaining = len(self.distributor.get_ticket_inventory(3))
                print(f"  Remaining Inventory:")
                print(f"    Tier 1: {tier1_remaining}")
                print(f"    Tier 2: {tier2_remaining}")
                print(f"    Tier 3: {tier3_remaining}")
            else:
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

        if player == self.distributor:
            # Distributor-specific menu
            print("1. Create More Tickets (costs money)")
            print("2. View Stats")
            print("3. End Turn")
            print("4. Quit Game")
            print(f"{'-'*50}")
            choice = input("Choose an option (1-4): ").strip()
        else:
            # Regular player menu
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
            current_player = self.get_current_player()

            if choice == '1':
                if current_player == self.distributor:
                    # Distributor creates more tickets
                    self.distributor_allocate_tickets(is_initial=False)
                else:
                    # Regular player plays scratch card
                    self.play_scratch_card()
            elif choice == '2':
                self.show_stats()
            elif choice == '3':
                print(f"\n{current_player.name} ended their turn.")
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
