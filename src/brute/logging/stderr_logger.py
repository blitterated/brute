import sys

from .loggable import Loggable
from ..ansi import ansi


class StdErrLogger(Loggable):
    def log(self, message: str) -> None:
        print(message, file=sys.stderr)

    def debug(self, message: str) -> None:
        #self.log(ansi.style.bold + ansi.bg.bright.cyan + ansi.fg.bright.white + message + ansi.reset)
        self.log(ansi.fg.magenta + message + ansi.reset)

    def info(self, message: str) -> None:
        self.log(ansi.fg.cyan + message + ansi.reset)

    def warn(self, message: str) -> None:
        self.log(ansi.fg.yellow + message + ansi.reset)

    def error(self, message: str) -> None:
        self.log(ansi.fg.red + message + ansi.reset)
