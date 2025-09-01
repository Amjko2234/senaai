from enum import Enum

from rich.console import Console


class RichHandlerCfg(Enum):
    """Contains config members for `rich.logging.RichHandler`.

    Members:
        console (Console): The console that enables ANSI-styled strings
            to be output to `sys.stdout`
        show_time (bool): `RichHandler`'s automatic formatter for time
        show_level (bool): `RichHandler`'s automatic formatter for level
        show_path (bool): `RichHandler`'s automatic formatter for path
        markup (bool): Whether to allow markup formatting, for example
            '[bold]Bold Text[/bold]'
        rich_tracebacks (bool): Whether to allow (auto) ANSI-styled strings
            of tracebacks
    """

    console = Console(force_terminal=True)
    show_time = False
    show_level = False
    show_path = False
    markup = True
    rich_tracebacks = True
