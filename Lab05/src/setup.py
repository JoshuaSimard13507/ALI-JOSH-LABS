from .game import Game
from .player import Player
import textwrap
import os

class Setup:
    """Interactive setup interface for the Farkle game.

    Provides a simple command loop with subcommands for player management,
    scoring configuration, and starting or exiting the game.

    Attributes:
        hot_dice_enabled (bool): Whether the Hot Dice rule is enabled.
        running (bool): Whether the setup screen loop continues running.
        players (list[Player]): Current player roster (index 0 is human).
        target_score (int): Points required to end the game.
        commands (dict[str, callable]): Top-level command dispatch table.
        scoring_commands (dict[str, callable]): Subcommands for ``scoring``.
        player_commands (dict[str, callable]): Subcommands for ``player``.
        player_list_commands (dict[str, callable]):
            Subcommands for ``player show``.
    """
    def __init__(self):
        """Initialize defaults, players, and command tables.

        Behavior:
          1) Enables Hot Dice by default and sets ``running = True``.
          2) Creates a default human player ``P1`` and an AI player ``BOT``.
          3) Sets ``target_score = 10000``.
          4) Registers top-level commands and their subcommand tables.
        """
        self.hot_dice_enabled = True
        self.running = True
        self.players = [Player("P1"), Player("BOT", is_ai=True)]
        self.target_score = 10000

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

    def run(self):
        """Run the interactive setup loop until the user exits.

        The algorithm:
          1) Print the setup header and hint to type ``help``.
          2) Read a line of input, lower-case, and tokenize by whitespace.
          3) If blank, continue; otherwise interpret the first token as a
             top-level command and dispatch to the registered handler.
          4) On unknown commands or bad arity, print ``\"Bad input\"``.
          5) Continue while ``self.running`` is True.

        :return: ``None``. Side effects: prints to console; may modify
                 ``players``, ``hot_dice_enabled``, ``target_score``,
                 or flip ``running`` to False.
        :rtype: None
        """
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
        """Display available commands and usage examples.

        :param args: Must be an empty list; otherwise prints ``\"Bad input\"``.
        :type args: list[str]
        :return: ``None``. Side effects: prints a formatted help screen.
        :rtype: None
        """
        if len(args) != 0:
            print("Bad input")
            return

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
                    Quit the program.""")

        print(help_text)

    def cmd_scoring(self, args: list[str]):
        """Dispatch a scoring subcommand.

        Behavior:
          1) Requires at least one token: the subcommand name.
          2) Looks up the subcommand in ``self.scoring_commands`` and
             forwards ``scoring_args`` to that handler.

        :param args: ``[subcommand, *scoring_args]``; prints ``\"Bad input\"``
                     if empty or unknown subcommand.
        :type args: list[str]
        :return: ``None``. Side effects: prints errors; may modify
                 scoring settings via subhandlers.
        :rtype: None
        """
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
        """Set the game's target score.

        Behavior:
          1) Requires exactly one argument that parses as ``int``.
          2) On success, assigns ``self.target_score`` and confirms.
          3) On parse failure, prints an error message.

        :param args: ``[points]`` where ``points`` is an integer string.
        :type args: list[str]
        :return: ``None``. Side effects: updates ``target_score``; prints.
        :rtype: None
        """
        if len(args) != 1:
            print("Bad input")
            return

        try:
            self.target_score = int(args[0])
            print(f"Set target score to {self.target_score} points")
        except ValueError:
            print(f"'{args[0]}' is not an integer")

    def cmd_scoring_hotdice(self, args: list[str]):
        """Enable or disable the Hot Dice rule.

        Behavior:
          1) Requires exactly one argument: ``\"on\"`` or ``\"off\"``.
          2) Any other value prints a guidance message.
          3) Always prints the resulting state (enabled/disabled).

        :param args: ``[\"on\"]`` to enable or ``[\"off\"]`` to disable.
        :type args: list[str]
        :return: ``None``. Side effects: updates ``hot_dice_enabled``; prints.
        :rtype: None
        """
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
        """Dispatch a player subcommand.

        Behavior:
          1) Requires at least one token: the subcommand name.
          2) Looks up the subcommand in ``self.player_commands`` and
             forwards the remaining args to that handler.

        :param args: ``[subcommand, *player_args]``; prints ``\"Bad input\"``
                     if empty or unknown subcommand.
        :type args: list[str]
        :return: ``None``. Side effects: prints errors; may modify player list.
        :rtype: None
        """
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
        """Rename the player (first in the list is human).

        Behavior:
          1) Requires exactly one argument: the new username.
          2) Prints a confirmation and stores the name in full uppercase.

        :param args: ``[username]`` for the human player.
        :type args: list[str]
        :return: ``None``. Side effects: updates ``players[0].username``; prints.
        :rtype: None
        """
        if len(args) != 1:
            print("Bad input")
            return


        print(f"Player '{self.players[0].username}' renamed to '{args[0].upper()}'")
        self.players[0].username = args[0].upper()

    def cmd_player_new(self, args: list[str]):
        """Replace the first player with a fresh ``Player`` instance (first in the list is human).

        Behavior:
          1) Requires exactly one argument: the new username.
          2) Constructs a new human ``Player`` with that name (uppercased).
          3) Prints a confirmation.

        :param args: ``[username]`` for the new player.
        :type args: list[str]
        :return: ``None``. Side effects: replaces ``players[0]``; prints.
        :rtype: None
        """
        if len(args) != 1:
            print("Bad input")
            return

        player = Player(args[0].upper())
        print(f"Overwrote '{self.players[0].username}' with new player '{player.username}'")
        self.players[0] = player

    def cmd_player_show(self, args: list[str]):
        """Show player information or dispatch list subcommands.

        Behavior:
          1) With no args, prints the first player's username (first in the list is human).
          2) With a subcommand, looks up in ``player_list_commands`` and
             forwards ``list_args`` to that handler.

        :param args: Either ``[]`` or ``[subcommand, *list_args]``.
        :type args: list[str]
        :return: ``None``. Side effects: prints; may delegate to list handlers.
        :rtype: None
        """
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
        """Display all players and their current in-game scores.

        :param args: Must be empty; otherwise prints ``\"Bad input\"``.
        :type args: list[str]
        :return: ``None``. Side effects: prints a small table.
        :rtype: None
        """
        if len(args) != 0:
            print("Bad input")
            return

        print("Player     Score\n"
              "-----------------")
        for player in self.players:
            print(f"{player.username: <10} {player.points:0>6}")

    def cmd_player_show_stats(self, args: list[str]):
        """Display lifetime stats for the player (first in the list is human).

        Columns:
          - Wins/Games
          - Lifetime total score

        :param args: Must be empty; otherwise prints ``\"Bad input\"``.
        :type args: list[str]
        :return: ``None``. Side effects: prints a small table.
        :rtype: None
        """
        if len(args) != 0:
            print("Bad input")
            return

        player = self.players[0]
        print("Player     Wins/Games Lifetime\n"
              "------------------------------")
        print(f"{player.username: <10} {player.wins:0>3}/{player.games:0>3}    {player.lifetime_score:0>8}")

    def cmd_player_save(self, args: list[str]):
        """Save the player's stats to JSON (first in the list is human).

        Behavior:
          1) Requires **no arguments** (current implementation).
          2) Calls ``Player.save()`` on ``players[0]`` and prints confirmation.
          3) Any arguments result in ``\"Bad input\"``.

        :param args: Must be empty.
        :type args: list[str]
        :return: ``None``. Side effects: writes to ``data/players/*.json``; prints.
        :rtype: None
        """
        if len(args) == 0:
            self.players[0].save()
            print(f"Player '{self.players[0].username}' saved")
            return

        print("Bad input")

    def cmd_player_load(self, args: list[str]):
        """Load stats for the player from disk (first Player in the list is human).

        Behavior:
          1) Requires exactly one argument: ``username`` to load.
          2) Calls ``self.players[0].load(username)``.
          3) On **success**, prints a confirmation message and returns early.
          4) On **failure**, prints a message stating the save does not exist.

        :param args: ``[username]`` to load.
        :type args: list[str]
        :return: ``None``. Side effects: may mutate ``players[0]``; prints result.
        :rtype: None
        """
        if len(args) != 1:
            print("Bad input")
            return

        if self.players[0].load(args[0]):
            print(f"Player '{self.players[0].username}' loaded")
            return

        print(f"Save of player {args[0].upper()} doesn't exist")


    def cmd_start(self, args: list[str]):
        """Start a game with current settings and players.

        Behavior:
          1) Requires no arguments; otherwise prints ``\"Bad input\"``.
          2) Instantiates ``Game`` with current players and target score,
             runs it, and prints either ``\"Game ran successfully\"`` or
             ``\"Game quit\"`` based on the boolean return.

        :param args: Must be empty.
        :type args: list[str]
        :return: ``None``. Side effects: constructs and runs a ``Game``; prints.
        :rtype: None
        """
        if len(args) != 0:
            print("Bad input")
            return

        if Game(players=self.players, target_score=self.target_score).run():
            print("Game ran successfully")
            return
        print("Game quit")

    def cmd_exit(self, args: list[str]):
        """Exit the setup loop.

        Behavior:
          1) Requires no arguments; otherwise prints ``\"Bad input\"``.
          2) Sets ``running = False`` and prints a friendly goodbye.

        :param args: Must be empty.
        :type args: list[str]
        :return: ``None``. Side effects: flips ``running`` to False; prints.
        :rtype: None
        """
        if len(args) != 0:
            print("Bad input")
            return

        self.running = False
        print("Byee :)")