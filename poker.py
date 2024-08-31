# poker_simulation.py

class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.current_bet = 0
        self.folded = False

    def bet(self, amount):
        if amount > self.money:
            raise ValueError(
                f"{self.name} does not have enough money to bet ${amount}.")
        self.current_bet += amount
        self.money -= amount

    def win(self, amount):
        self.money += amount

    def fold(self):
        self.folded = True

    def reset(self):
        self.current_bet = 0
        self.folded = False

    def __str__(self):
        return f"{self.name}: ${self.money} (Current Bet: ${self.current_bet}, Folded: {self.folded})"


class PokerGame:
    def __init__(self, players):
        self.players = players
        self.pot = 0
        self.highest_bet = 0

    def ante(self, amount):
        for player in self.players:
            if not player.folded:
                try:
                    player.bet(amount)
                    print(f"{player.name} antes ${amount}.")
                except ValueError as e:
                    print(f"Cannot ante for {player.name}: {e}")

    def place_bets(self, starting_player):
        starting_index = self.players.index(
            next(player for player in self.players if player.name == starting_player))
        i = 0

        num_playing = self.remaining_players()
        while True:
            player = self.players[(starting_index + i) % len(self.players)]
            if player.folded:
                i += 1
                continue

            # Check if only one player remains
            if self.remaining_players() == 1:
                return True

            while True:
                try:
                    action = input(
                        f"{player.name} (money: ${player.money}, current bet: ${player.current_bet}), enter bet amount, 'call', or 'fold': ").strip().lower()
                    if action == 'fold':
                        player.fold()
                        print(f"{player.name} folds.")
                        break
                    elif action == 'call':
                        bet_amount = self.highest_bet - player.current_bet
                        if bet_amount > player.money:
                            print(
                                f"{player.name} does not have enough money to call.")
                            continue
                        player.bet(bet_amount)
                        print(
                            f"{player.name} calls and bets ${self.highest_bet}.")
                        break
                    else:
                        bet_amount = int(action)
                        if bet_amount < self.highest_bet:
                            print(
                                f"Bet amount must be greater or equal to the current highest bet of ${self.highest_bet}.")
                            continue
                        player.bet(bet_amount - player.current_bet)
                        self.highest_bet = player.current_bet
                        print(f"{player.name} bets ${bet_amount}.")
                        break
                except ValueError as e:
                    print(f"Invalid input: {e}. Please try again.")
                except Exception as e:
                    print(
                        f"An unexpected error occurred: {e}. Please try again.")

            i += 1

            if self.all_bets_equal() and i >= num_playing:
                return False

            if i > 1000:
                raise Exception()

    def all_bets_equal(self):
        active_bets = [
            player.current_bet for player in self.players if not player.folded]
        return len(set(active_bets)) == 1

    def remaining_players(self):
        return len([player for player in self.players if not player.folded])

    def resolve_winner(self, winner_name):
        winner = next(
            player for player in self.players if player.name == winner_name)
        winner.win(self.pot)
        print(f"\n{winner.name} wins the pot of ${self.pot}!\n")
        self.pot = 0

    def collect(self):
        self.pot += sum(player.current_bet for player in self.players)

    def end_round(self):
        self.highest_bet = 0

        for player in self.players:
            player.current_bet = 0

    def show_balances(self):
        for player in self.players:
            print(player)


def main():
    # Initialize players
    players = [
        Player("Harrison", 100),
        Player("Ayush", 100),
        Player("Dillon", 100),
        Player("Dashiell", 100)
    ]

    game = PokerGame(players)

    while True:
        inactive_players = input(
            "Enter the names of players who are not playing, separated by commas (or leave blank if all are playing): ").strip().split(',')
        inactive_players = [name.strip()
                            for name in inactive_players if name.strip()]

        for player in players:
            if player.name in inactive_players:
                player.fold()
        while True:
            try:
                ante_text = input(
                    "Enter the ante amount for this round (default is $1): ")
                if ante_text == "\n":
                    ante_amount = 1
                else:
                    ante_amount = int(ante_text.strip())
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Please try again.")

        game.ante(ante_amount)
        game.collect()
        game.end_round()
        starting_player = input(
            "Enter the name of the player who starts the betting: ").strip()
        if starting_player not in [player.name for player in players]:
            print("Invalid player name. Please try again.")
            continue

        for round_num in range(3):
            round_ended = game.place_bets(starting_player)
            game.collect()
            game.end_round()
            print(f"---------- Round {round_num + 1} End ----------")

            # Check if only one player remains
            if round_ended:
                winner_name = next(
                    player.name for player in players if not player.folded)
                print("One player remaining.")
                game.resolve_winner(winner_name)
                break

        if not round_ended:
            game.show_balances()

            winner_name = input(
                "Enter the name of the winning player: ").strip()
            game.resolve_winner(winner_name)
        game.show_balances()

        [player.reset() for player in players]

        if input("Play another round? (y/n): ").strip().lower() != 'y':
            break


if __name__ == "__main__":
    main()
