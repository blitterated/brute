from dataclasses import dataclass

@dataclass(frozen=True)
class AnsiStyle:
    bold          = "\033[1m"
    italic        = "\033[3m"
    underline     = "\033[4m"
    strikethrough = "\033[9m"


@dataclass(frozen=True)
class AnsiForegroundColorBright:
    black   = "\033[90m"
    red     = "\033[91m"
    green   = "\033[92m"
    yellow  = "\033[93m"
    blue    = "\033[94m"
    magenta = "\033[95m"
    cyan    = "\033[96m"
    white   = "\033[97m"


@dataclass(frozen=True)
class AnsiForegroundColor:
    black   = "\033[30m"
    red     = "\033[31m"
    green   = "\033[32m"
    yellow  = "\033[33m"
    blue    = "\033[34m"
    magenta = "\033[35m"
    cyan    = "\033[36m"
    white   = "\033[37m"
    bright  = AnsiForegroundColorBright()


@dataclass(frozen=True)
class AnsiBackgroundColorBright:
    black   = "\033[100m"
    red     = "\033[101m"
    green   = "\033[102m"
    yellow  = "\033[103m"
    blue    = "\033[104m"
    magenta = "\033[105m"
    cyan    = "\033[106m"
    white   = "\033[107m"


@dataclass(frozen=True)
class AnsiBackgroundColor:
    black   = "\033[40m"
    red     = "\033[41m"
    green   = "\033[42m"
    yellow  = "\033[43m"
    blue    = "\033[44m"
    magenta = "\033[45m"
    cyan    = "\033[46m"
    white   = "\033[47m"
    bright  = AnsiBackgroundColorBright()


@dataclass(frozen=True)
class Ansi:
    style = AnsiStyle()
    fg    = AnsiForegroundColor()
    bg    = AnsiBackgroundColor()
    reset = "\033[0m"
