from .calculate_score import CalculateScore
from .game import Game
from .player import Player
import os

class Setup:
    def __init__(self, load_on_init = True):
        self.scoring_methods = {
            "default": CalculateScore.doubling,
            "adding": CalculateScore.adding
        }
        self.calculate_score = self.scoring_methods["default"]
        self.hot_dice_enabled = True
        self.running = True
        self.players = []
        self.target_score = 10000
        self.num_dice = 6

        if load_on_init:
            self.load()

        if len(self.players) < 2:
            self.add_player("BOT")
            self.toggle_ai("BOT")
            self.add_player("P1")

    def run(self): # configure game using cli. tokenize user input to parse input commands
        while self.running:
            user_in = input("> ").split()
            if len(user_in) > 0:
                if user_in[0] == "help":
                    self.help()

                elif user_in[0] == "scoring":
                    if len(user_in) == 3:
                        if user_in[1] == "method":
                            if user_in[2] in self.scoring_methods:
                                self.calculate_score = self.scoring_methods[user_in[2]]
                                print(f"Scoring method '{user_in[2]}' enabled")
                            else:
                                print(f"'{user_in[2]}' not a scoring method")
                        elif user_in[1] == "target":
                            try:
                                self.target_score = int(user_in[2])
                                print(f"Set target score to {self.target_score} points")
                            except ValueError:
                                print(f"'{user_in[2]}' is not an integer")

                elif user_in[0] == "toggle-ai":
                    if len(user_in) != 2:
                        print("Bad input")
                    else:
                        player = self.toggle_ai(user_in[1])
                        if player is None:
                            print(f"Player '{user_in[1]}' not a player")
                        else:
                            print(f"'{player.username}' AI {'enabled' if player.is_ai else 'disabled'}")

                elif user_in[0] == "rename":
                    if len(user_in) != 3:
                        print("Bad input")
                    else:
                        player = self.rename(user_in[1], user_in[2])
                        if player is None:
                            print(f"Player '{user_in[1]}' not a player or '{user_in[2]}' already exists'")
                        else:
                            print(f"Player '{user_in[1]}' renamed to '{player.username}'")

                elif user_in[0] == "add":
                    if len(user_in) != 2:
                        print("Bad input")
                    else:
                        player = self.add_player(user_in[1])
                        if player is None:
                            print(f"Player '{user_in[1]}' already exists")
                        else:
                            print(f"Player '{player.username}' added")

                elif user_in[0] == "remove":
                    if len(user_in) != 2:
                        print("Bad input")
                    else:
                        player = self.remove_player(user_in[1])
                        if player is None:
                            print(f"Player '{user_in[1]}' not a player or '{user_in[1]}' is one of two players (there must be at least two players)")
                        else:
                            print(f"Player '{player.username}' removed")

                elif user_in[0] == "list":
                    if len(user_in) == 1:
                        for player in self.players:
                            print(f"{player.username}", end=" ")
                        print()
                    elif len(user_in) != 2:
                        print("Bad input")
                    elif user_in[1] == "scores":
                        print("Player     Score\n"
                              "-----------------")
                        for player in self.players:
                            print(f"{player.username: <10} {player.points:0>6}")
                    elif user_in[1] == "stats":
                        # list wins, total games, total points
                        print("Player     Wins/Games Lifetime\n"
                              "------------------------------")
                        for player in self.players:
                            print(f"{player.username: <10} {player.wins:0>3}/{player.games:0>3}    {player.lifetime_score:0>8}")
                    else:
                        print("Bad input")

                elif user_in[0] == "save":
                    if len(user_in) == 1:
                        for player in self.players:
                            if not player.is_ai:
                                self.save(player)
                                print(f"Player '{player.username}' saved")
                    elif len(user_in) == 2:
                        self.save(user_in[1])
                        print(f"Player '{user_in[1]}' saved")
                    else:
                        print("Bad input")

                elif user_in[0] == "load":
                    loaded: tuple = ()
                    if len(user_in) == 1:
                        loaded = self.load()
                    elif len(user_in) == 2:
                        loaded = self.load(user_in[1])

                    if loaded is None:
                        print("No players loaded")
                    else:
                        for player in loaded:
                            print(f"Player '{player.username}' loaded")

                elif user_in[0] == "swap":
                    if len(user_in) != 3:
                        print("Bad input")
                    else:
                        swapped = self.swap(user_in[1], user_in[2])
                        if swapped is None:
                            print(f"Player '{user_in[1]}' and/or '{user_in[2]}' not (a) player(s)")
                        else:
                            print(f"Players '{user_in[1]}' and '{user_in[2]}' swapped")

                elif user_in[0] == "dice":
                    if len(user_in) == 2 and user_in[1] == "toggle-hot":
                        self.hot_dice_enabled = not self.hot_dice_enabled
                        print(f"Hot dice {'enabled' if self.hot_dice_enabled else 'disabled'}")
                    elif len(user_in) == 3 and user_in[1] == "set":
                        try:
                            self.num_dice = int(user_in[2])
                            print(f"Set roll to {self.num_dice} dice")
                        except ValueError:
                            print(f"'{user_in[2]}' is not an integer")
                    else:
                        print("Bad input")

                elif user_in[0] == "start":
                    if len(user_in) != 1:
                        print("Bad input")
                    else:
                        game_ran = self.create_game()
                        if not game_ran:
                            print("Not enough players")

                elif user_in[0] == "exit":
                    if len(user_in) != 1:
                        print("Bad input")
                    else:
                        self.running = False
                        print("Byee :)")
                else:
                    print("Bad input")

    def help(self):
        print("all the commands here")

    def save(self, player: str | Player) -> bool:
        if isinstance(player, str):
            for player_obj in self.players:
                if player_obj.username == player.upper():
                    player_obj.save()
                    return True
        elif isinstance(player, Player):
            player.save()
            return True
        return False

    def load(self, username: str | None = None) -> tuple[Player, ...] | None:
        if not os.path.exists("players"):
            return None

        if username is None:
            # load data to existing players, create new player objs for nonexisting
            loaded: list[Player] = []
            with os.scandir("players") as entries:
                for entry in entries:
                    if entry.is_file():
                        json_username = entry.name[:-5].upper()
                        player_exists = False
                        for player in self.players:
                            if json_username == player.username:
                                player_exists = True
                                player.load()
                                loaded.append(player)
                        if not player_exists:
                            player = Player(json_username)
                            player.load()
                            loaded.append(player)
                            self.players.append(player)
            return tuple(loaded) if loaded else None
        else:
            for player in self.players:
                if player.username == username.upper():
                    player.load()
                    return (player,)
        return None

    def toggle_ai(self, username: str) -> Player | None:
        for player in self.players:
            if player.username == username.upper():
                player.is_ai = not player.is_ai
                return player
        return None

    def rename(self, username: str, new: str) -> Player | None:
        rename: Player | None = None
        for player in self.players:
            if player.username == new.upper(): # only rename uniquely
                return None
            if player.username == username.upper():
                rename = player
        if rename is not None:
            rename.username = new.upper()
        return rename

    def swap(self, username: str, other: str) -> tuple[Player, Player] | None:
        first_index: int = -1
        second_index: int = -1
        for i in range(len(self.players)):
            player: Player = self.players[i]
            if player.username == username.upper():
                first_index = i
            if player.username == other.upper():
                second_index = i
        if first_index == -1 or second_index == -1:
            return None
        swap: Player = self.players[first_index]
        self.players[first_index] = self.players[second_index]
        self.players[second_index] = swap
        return self.players[first_index], self.players[second_index]

    def add_player(self, username: str) -> Player | None:
        for player in self.players:
            if player.username == username.upper():
                return None
        player = Player(username.upper())
        self.players.append(player)
        return player


    def remove_player(self, username: str) -> Player | None:
        if len(self.players) <= 2:
            return None
        for player in self.players:
            if player.username == username.upper():
                self.players.remove(player)
                return player
        return None

    def create_game(self) -> bool:
        if len(self.players) < 2:
            return False
        game = Game(self.calculate_score, self.players, self.target_score, self.num_dice)
        game.run()
        return True
