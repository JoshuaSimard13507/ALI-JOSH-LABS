from .game import Game
from .player import Player
import textwrap
import os

class Setup:
    def __init__(self):
        self.hot_dice_enabled = True
        self.running = True
        self.players = [Player("P1"), Player("BOT", is_ai=True)]
        self.target_score = 10000
        self.num_dice = 6

        self.commands = {
            "help" : self.cmd_help,
            "scoring" : self.cmd_scoring,
            "player" : self.cmd_player,
            "start" : self.cmd_start,
            "exit" : self.cmd_exit
        }
        self.scoring_commands = {
            "target" : self.cmd_scoring_target,
            "hot-dice" : self.cmd_scoring_hotdice
        }
        self.player_commands = {
            "show" : self.cmd_player_show,
            "rename" : self.cmd_player_rename,
            "new": self.cmd_player_new,
            "save" : self.cmd_player_save,
            "load" : self.cmd_player_load
        }
        self.player_list_commands = {
            "scores" : self.cmd_player_show_scores,
            "stats" : self.cmd_player_show_stats
        }

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

    def cmd_scoring_target(self, args: list[str]):
        if len(args) != 1:
            print("Bad input")
            return

        try:
            self.target_score = int(args[0])
            print(f"Set target score to {self.target_score} points")
        except ValueError:
            print(f"'{args[0]}' is not an integer")

    def cmd_scoring_hotdice(self, args: list[str]):
        if len(args) != 1:
            print("Bad input")
            return

        if args[0] == "on":
            self.hot_dice_enabled = True
        elif args[0] == "off":
            self.hot_dice_enabled = False
        else:
            print(f"{args[0]} not an option, must input 'on' or 'off'")
        print(f"Hot dice {'enabled' if self.hot_dice_enabled else 'disabled'}")

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

    def cmd_player_rename(self, args: list[str]):
        if len(args) != 1:
            print("Bad input")
            return


        print(f"Player '{self.players[0].username}' renamed to '{args[0].upper()}'")
        self.players[0].username = args[0].upper()

    def cmd_player_new(self, args: list[str]):
        if len(args) != 1:
            print("Bad input")
            return

        player = Player(args[0].upper())
        print(f"Overwrote '{self.players[0].username}' with new player '{player.username}'")
        self.players[0] = player

    def cmd_player_show(self, args: list[str]):
        if len(args) == 0:
            print(f"{self.players[0].username}")
            return

        cmd, *list_args = args
        handler = self.player_list_commands.get(cmd)
        if handler is None:
            print("Bad input")
            return

        handler(list_args)

    def cmd_player_show_scores(self, args: list[str]):
        if len(args) != 0:
            print("Bad input")
            return

        print("Player     Score\n"
              "-----------------")
        for player in self.players:
            print(f"{player.username: <10} {player.points:0>6}")

    def cmd_player_show_stats(self, args: list[str]):
        if len(args) != 0:
            print("Bad input")
            return

        player = self.players[0]
        print("Player     Wins/Games Lifetime\n"
              "------------------------------")
        print(f"{player.username: <10} {player.wins:0>3}/{player.games:0>3}    {player.lifetime_score:0>8}")

    def cmd_player_save(self, args: list[str]):
        if len(args) == 0:
            self.save(self.players[0])
            print(f"Player '{self.players[0].username}' saved")
            return

        print("Bad input")

    def cmd_player_load(self, args: list[str]):
        if len(args) != 1:
            print("Bad input")
            return

        player = self.load(args[0])
        if player is None:
            print(f"Save of player {args[0].upper()} doesn't exist")
            return

        print(f"Player '{player.username}' loaded")


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


        Player Config
        -------------
        player rename <username>
            Rename player.
        player new <username>
            Overwrite player with new username.
                
        player show
            List player username.
        player show scores
            Show current scores for player and BOT.
        player show stats
            Show player lifetime stats (Wins/Games and Lifetime Score).

        player save
            Save player to JSON.
        player load <username>
            Load a saved player.


        Scoring Config
        --------------
        scoring hot-dice <state>
            Turn hot-dice on or off. Must input 'on' or 'off'.
        scoring target <points>
            Set the target score to end the game (integer).
        

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

    def save(self, player: Player) -> Player:
            player.save()
            return player

    def load(self, username: str) -> Player | None:
        if not os.path.exists("data/players"):
            return None

        if self.players[0].load(username):
            return self.players[0]
        return None

    def create_game(self) -> bool:
        if len(self.players) < 2:
            return False
        game = Game(self.players, self.target_score, self.num_dice)
        success = game.run()
        if not success:
            print("Game quit")
        else:
            print("Game ran successfully")
        return True
