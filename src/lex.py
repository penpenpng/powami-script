from typing import List

import ply.lex as lex
from ply.lex import Lexer

from enums import Context, Token


def define_token(
    token: Token,
    regex: str,
    contexts: List[Context] = [Context.INITIAL],
    pushed_contexts: List[Context] = [],
    pop_contexts: bool = False,
    const_symbol: bool = True,
    delegate=None,
):
    def t_rule(t: Lexer):
        for context in reversed(pushed_contexts):
            t.lexer.push_state(str(context))
        if pop_contexts:
            t.lexer.pop_state()
        if const_symbol:
            t.value = token
        if delegate:
            return delegate(t)
        return t

    for context in contexts:
        name = f"t_{context}_{token}"
        globals()[name] = lex.TOKEN(regex)(t_rule)


tokens = list(map(str, Token))
states = [
    (str(s), "exclusive") for s in Context
    if s is not Context.INITIAL
]


define_token(
    Token.LITERAL,
    r"[ぽわ！？ー～]+",
    contexts=[Context.LITERAL],
    const_symbol=False,
)

define_token(
    Token.VAR,
    r"([ぽわ]{3}|ぽ～わ|わ～ぽ)",
    contexts=[Context.VAR],
    pop_contexts=True,
    const_symbol=False,
)

define_token(
    Token.PATTERN,
    r"[ぽわ！？ー～]+",
    contexts=[Context.PATTERN],
    const_symbol=False,
)

define_token(
    Token.IF,
    r"ぽ？",
    contexts=[Context.INITIAL, Context.BLOCK],
    pushed_contexts=[Context.VAR, Context.PATTERN, Context.BLOCK],
)

define_token(
    Token.NOT_IF,
    r"ぽ！？",
    contexts=[Context.INITIAL, Context.BLOCK],
    pushed_contexts=[Context.VAR, Context.PATTERN, Context.BLOCK],
)

define_token(
    Token.WHILE,
    r"わ？",
    contexts=[Context.INITIAL, Context.BLOCK],
    pushed_contexts=[Context.VAR, Context.PATTERN, Context.BLOCK],
)

define_token(
    Token.NOT_WHILE,
    r"わ！？",
    contexts=[Context.INITIAL, Context.BLOCK],
    pushed_contexts=[Context.VAR, Context.PATTERN, Context.BLOCK],
)

define_token(
    Token.PUSH_RIGHT,
    r"ぽ～～",
    contexts=[Context.INITIAL, Context.BLOCK],
    pushed_contexts=[Context.VAR, Context.VAR],
)

define_token(
    Token.PUSH_LEFT,
    r"わ～～",
    contexts=[Context.INITIAL, Context.BLOCK],
    pushed_contexts=[Context.VAR, Context.VAR],
)

define_token(
    Token.POP_RIGHT,
    r"ぽーー",
    contexts=[Context.INITIAL, Context.BLOCK],
    pushed_contexts=[Context.VAR, Context.VAR],
)

define_token(
    Token.POP_LEFT,
    r"わーー",
    contexts=[Context.INITIAL, Context.BLOCK],
    pushed_contexts=[Context.VAR, Context.VAR],
)

define_token(
    Token.POP_RIGHT_DISCARD,
    r"ぽー！",
    contexts=[Context.INITIAL, Context.BLOCK],
    pushed_contexts=[Context.VAR],
)

define_token(
    Token.POP_LEFT_DISCARD,
    r"わー！",
    contexts=[Context.INITIAL, Context.BLOCK],
    pushed_contexts=[Context.VAR],
)

define_token(
    Token.NEGATE,
    r"ぽーわわ",
    contexts=[Context.INITIAL, Context.BLOCK],
    pushed_contexts=[Context.VAR],
)

define_token(
    Token.CWISE_AND,
    r"ぽぽ",
    contexts=[Context.INITIAL, Context.BLOCK],
    pushed_contexts=[Context.VAR, Context.VAR],
)

define_token(
    Token.CWISE_OR,
    r"わわ",
    contexts=[Context.INITIAL, Context.BLOCK],
    pushed_contexts=[Context.VAR, Context.VAR],
)

define_token(
    Token.ASSIGN,
    r"ぽわ～",
    contexts=[Context.INITIAL, Context.BLOCK],
    pushed_contexts=[Context.VAR, Context.LITERAL],
)

define_token(
    Token.COPY,
    r"わぽ～",
    contexts=[Context.INITIAL, Context.BLOCK],
    pushed_contexts=[Context.VAR, Context.VAR],
)

define_token(
    Token.DELIMITER,
    r"っ",
    contexts=[Context.BLOCK, Context.LITERAL, Context.PATTERN],
    pop_contexts=True
)


lexer = lex.lex()
