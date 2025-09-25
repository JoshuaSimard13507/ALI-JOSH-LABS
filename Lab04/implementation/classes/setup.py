from .game import Game
from .player import Player
import textwrap
import os

class Setup:
    def __init__(self, load_on_init = True):
        self.calculate_score = Game.scoring_methods["default"]
        self.hot_dice_enabled = True
        self.running = True
        self.players = []
        self.target_score = 10000
        self.num_dice = 6

        self.commands = {
            "help" : self.cmd_help,
            "scoring" : self.cmd_scoring,
            "dice" : self.cmd_dice,
            "player" : self.cmd_player,
            "start" : self.cmd_start,
            "exit" : self.cmd_exit
        }
        self.scoring_commands = {
            "method" : self.cmd_scoring_method,
            "target" : self.cmd_scoring_target
        }
        self.dice_commands = {
            "toggle-hot" : self.cmd_dice_togglehot,
            "set" : self.cmd_dice_set
        }
        self.player_commands = {
            "list" : self.cmd_player_list,
            "add" : self.cmd_player_add,
            "remove" : self.cmd_player_remove,
            "rename" : self.cmd_player_rename,
            "toggle-ai" : self.cmd_player_toggleai,
            "swap" : self.cmd_player_swap,
            "save" : self.cmd_player_save,
            "load" : self.cmd_player_load
        }
        self.player_list_commands = {
            "scores" : self.cmd_player_list_scores,
            "stats" : self.cmd_player_list_stats
        }

        if load_on_init:
            self.load()

        if len(self.players) < 2:
            self.add_player("BOT")
            self.toggle_ai("BOT")
            self.add_player("P1")

    def run(self): # configure game using cli. tokenize user input to parse input commands
        print("====  SETUP SCREEN  ====\n"
              "Type 'help' for commands")
        while self.running:
            user_in = input("> ").lower().split()
            if len(user_in) == 0:
                continue

            cmd, *args = user_in
            handler = self.commands.get(cmd)
            if handler is None:
                print("Bad input")
                continue

            handler(args)

    def cmd_help(self, args: list[str]):
        if len(args) != 0:
            print("Bad input")
            return

        self.help()

    def cmd_scoring(self, args: list[str]):
        if len(args) == 0:
            print("Bad input")
            return

        cmd, *scoring_args = args
        handler = self.scoring_commands.get(cmd)
        if handler is None:
            print("Bad input")
            return

        handler(scoring_args)

    def cmd_scoring_method(self, args: list[str]):
        if len(args) != 1:
            print("Bad input")
            return

        if args[0] in Game.scoring_methods:
            self.calculate_score = Game.scoring_methods[args[0]]
            print(f"Scoring method '{args[0]}' enabled")
            return
        print(f"'{args[0]}' not a scoring method")

    def cmd_scoring_target(self, args: list[str]):
        if len(args) != 1:
            print("Bad input")
            return

        try:
            self.target_score = int(args[0])
            print(f"Set target score to {self.target_score} points")
        except ValueError:
            print(f"'{args[0]}' is not an integer")

    def cmd_player(self, args: list[str]):
        if len(args) == 0:
            print("Bad input")
            return

        cmd, *scoring_args = args
        handler = self.player_commands.get(cmd)
        if handler is None:
            print("Bad input")
            return

        handler(scoring_args)

    def cmd_player_toggleai(self, args: list[str]):
        if len(args) != 1:
            print("Bad input")
            return

        player = self.toggle_ai(args[0])
        if player is None:
            print(f"Player '{args[0].upper()}' not a player")
            return

        print(f"'{player.username}' AI {'enabled' if player.is_ai else 'disabled'}")

    def cmd_player_rename(self, args: list[str]):
        if len(args) != 2:
            print("Bad input")
            return

        player = self.rename(args[0], args[1])
        if player is None:
            print(f"Player '{args[0].upper()}' not a player or '{args[1].upper()}' already exists'")
            return

        print(f"Player '{args[0].upper()}' renamed to '{player.username}'")

    def cmd_player_add(self, args: list[str]):
        if len(args) != 1:
            print("Bad input")
            return

        player = self.add_player(args[0])
        if player is None:
            print(f"Player '{args[0].upper()}' already exists")
            return

        print(f"Player '{player.username}' added")

    def cmd_player_remove(self, args: list[str]):
        if len(args) != 1:
            print("Bad input")
            return

        player = self.remove_player(args[0])
        if player is None:
            print(f"Player '{args[0].upper()}' not a player or is one of two players (there must be at least two players)")
            return

        print(f"Player '{player.username}' removed")

    def cmd_player_list(self, args: list[str]):
        if len(args) == 0:
            for player in self.players:
                print(f"{player.username}", end=" ")
            print()
            return

        cmd, *list_args = args
        handler = self.player_list_commands.get(cmd)
        if handler is None:
            print("Bad input")
            return

        handler(list_args)

    def cmd_player_list_scores(self, args: list[str]):
        if len(args) != 0:
            print("Bad input")
            return

        print("Player     Score\n"
              "-----------------")
        for player in self.players:
            print(f"{player.username: <10} {player.points:0>6}")

    def cmd_player_list_stats(self, args: list[str]):
        if len(args) != 0:
            print("Bad input")
            return

        print("Player     Wins/Games Lifetime\n"
              "------------------------------")
        for player in self.players:
            print(f"{player.username: <10} {player.wins:0>3}/{player.games:0>3}    {player.lifetime_score:0>8}")

    def cmd_player_save(self, args: list[str]):
        if len(args) == 0:
            for player in self.players:
                if not player.is_ai:
                    self.save(player)
                    print(f"Player '{player.username}' saved")
            return

        if len(args) == 1:
            self.save(args[0])
            print(f"Player '{args[0].upper()}' saved")
            return

        print("Bad input")

    def cmd_player_load(self, args: list[str]):
        loaded: tuple = ()
        if len(args) == 0:
            loaded = self.load()
        elif len(args) == 1:
            loaded = self.load(args[0])

        if loaded is None:
            print("No players loaded")
            return

        for player in loaded:
            print(f"Player '{player.username}' loaded")

    def cmd_player_swap(self, args: list[str]):
        if len(args) != 2:
            print("Bad input")
            return

        swapped = self.swap(args[0], args[1])
        if swapped is None:
            print(f"Player '{args[0].upper()}' and/or '{args[1].upper()}' not (a) player(s)")
            return

        print(f"Players '{swapped[1].username}' and '{swapped[0].username}' swapped")

    def cmd_dice(self, args: list[str]):
        if len(args) == 0:
            print("Bad input")
            return

        cmd, *dice_args = args
        handler = self.dice_commands.get(cmd)
        if handler is None:
            print("Bad input")
            return

        handler(dice_args)

    def cmd_dice_togglehot(self, args: list[str]):
        if len(args) != 0:
            print("Bad input")
            return

        self.hot_dice_enabled = not self.hot_dice_enabled
        print(f"Hot dice {'enabled' if self.hot_dice_enabled else 'disabled'}")

    def cmd_dice_set(self, args: list[str]):
        if len(args) != 1:
            print("Bad input")
            return

        try:
            self.num_dice = int(args[0])
            print(f"Set roll to {self.num_dice} dice")
        except ValueError:
            print(f"'{args[0]}' is not an integer")

    def cmd_start(self, args: list[str]):
        if len(args) != 0:
            print("Bad input")
            return

        game_ran = self.create_game()
        if not game_ran:
            print("Not enough players")

    def cmd_exit(self, args: list[str]):
        if len(args) != 0:
            print("Bad input")
            return

        self.running = False
        print("Byee :)")

    def help(self):
        help_text = textwrap.dedent(f"""
        Farkle CLI — Commands Reference
        ===============================
        Type a command followed by its arguments. Arguments in <> are required.


        Players
        -------
        player add <username>
            Add a new human player.
        player remove <username>
            Remove a player (requires at least 2 total players to remain).
        player rename <old_username> <new_username>
            Rename an existing player to a new, unused name.
        player toggle-ai <username>
            Toggle AI control for the given player.
        player swap <username1> <username2>
            Swap the turn order of two players.
        
        player list
            List all player usernames on one line.
        player list scores
            Show current scores for each player.
        player list stats
            Show lifetime stats (Wins/Games and Lifetime Score) per player.

        player save
            Save all non-AI players.
        player save <username>
            Save a single player by name.
        player load
            Load all saved players (if supported by your storage).
        player load <username>
            Load a single saved player.


        Scoring Configuration
        ---------------------
        scoring method <name>
            Select a scoring method by name. Available: {', '.join(Game.scoring_methods.keys())}
        scoring target <points>
            Set the target score to end the game (integer).


        Dice Configuration
        ------------------
        dice toggle-hot
            Enable/disable Hot Dice.
        dice set <n>
            Set number of dice rolled each roll to <n> (integer).


        Misc
        ----
        help
            Show this help screen.
        start
            Start a game with the current settings and players.
        exit
            Quit the program.
        """)
        print(help_text, end="")

    def save(self, player: str | Player) -> Player | None:
        if isinstance(player, str):
            for player_obj in self.players:
                if player_obj.username == player.upper():
                    player_obj.save()
                    return player_obj
        elif isinstance(player, Player):
            player.save()
            return player
        return None

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
        success = game.run()
        if not success:
            print("Game quit")
        else:
            print("Game ran successfully")
        return True
