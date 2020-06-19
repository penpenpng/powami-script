from enum import Enum, auto


class StrEnum(Enum):
    def __str__(self):
        name = str(self.name)
        return name.replace("_", "")


class Token(StrEnum):
    LITERAL = auto()
    VAR = auto()
    PATTERN = auto()

    IF = auto()
    NOT_IF = auto()
    WHILE = auto()
    NOT_WHILE = auto()

    PUSH_LEFT = auto()
    PUSH_RIGHT = auto()
    POP_LEFT = auto()
    POP_RIGHT = auto()
    POP_LEFT_DISCARD = auto()
    POP_RIGHT_DISCARD = auto()

    NEGATE = auto()
    CWISE_AND = auto()
    CWISE_OR = auto()

    ASSIGN = auto()
    COPY = auto()

    DELIMITER = auto()


class Context(StrEnum):
    INITIAL = auto()

    LITERAL = auto()
    VAR = auto()
    PATTERN = auto()

    BLOCK = auto()
