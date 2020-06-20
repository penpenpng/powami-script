import re

import ply.yacc as yacc

from .engine import Assignment, ControlStatement, FunctionCall, Script
from .enums import Token
from .error import PwsSyntaxError
from .lex import lexer, tokens

last_eval = None


def parse(script):
    parser = yacc.yacc()

    # parser.restart() is broken, so
    sym = yacc.YaccSymbol()
    sym.type = '$end'
    parser.symstack = [sym]
    parser.statestack = [0]
    parser.state = None
    parser.token = None

    parser.parse(script, lexer=lexer)
    return last_eval


def p_error(t):
    raise PwsSyntaxError(t)


def define_grammar(clause: str, grammar: str, delegate):
    def p_rule(p):
        global last_eval
        last_eval = p[0] = delegate(p)

    grammar = "\n|".join(
        map(
            lambda s: s.replace("\n", " "),
            grammar.split("|")
        )
    )

    p_rule.co_firstlineno = delegate.__code__.co_firstlineno
    p_rule.__doc__ = f"{clause} : {grammar}"

    P_RULE_COUNTS = "prule_counts"
    if P_RULE_COUNTS not in globals():
        c = 0
    else:
        c = globals()[P_RULE_COUNTS]

    c += 1
    name = f"p_{clause}_{c}"

    globals()[name] = p_rule
    globals()[P_RULE_COUNTS] = c + 1


define_grammar(
    "script",
    f"""
    statement
    """,
    lambda p: p[1],
)

define_grammar(
    "script",
    f"""
    script statement
    """,
    lambda p: Script(p[1], p[2]),
)

define_grammar(
    "statement",
    f"""
    assignment
    | control_statement
    | uniop_function_call
    | biop_function_call
    """,
    lambda p: p[1],
)

define_grammar(
    "control_keyword",
    f"""
    {Token.IF}
    | {Token.NOT_IF}
    | {Token.WHILE}
    | {Token.NOT_WHILE}
    """,
    lambda p: p[1],
)

define_grammar(
    "uniop_function",
    f"""
    {Token.NEGATE}
    | {Token.POP_LEFT_DISCARD}
    | {Token.POP_RIGHT_DISCARD}
    """,
    lambda p: p[1],
)

define_grammar(
    "biop_function",
    f"""
    {Token.PUSH_LEFT}
    | {Token.PUSH_RIGHT}
    | {Token.POP_LEFT}
    | {Token.POP_RIGHT}
    | {Token.CWISE_AND}
    | {Token.CWISE_OR}
    | {Token.COPY}
    """,
    lambda p: p[1],
)

define_grammar(
    "assignment",
    f"""
    {Token.ASSIGN} {Token.VAR} {Token.LITERAL} {Token.DELIMITER}
    """,
    lambda p: Assignment(p[2], p[3])
)

define_grammar(
    "control_statement",
    f"""
    control_keyword {Token.VAR} {Token.PATTERN} {Token.DELIMITER}
        script
    {Token.DELIMITER}
    """,
    lambda p: ControlStatement(p[1], p[2], p[3], p[5]),
)

define_grammar(
    "uniop_function_call",
    f"""
    uniop_function {Token.VAR}
    """,
    lambda p: FunctionCall(p[1], p[2]),
)

define_grammar(
    "biop_function_call",
    f"""
    biop_function {Token.VAR} {Token.VAR}
    """,
    lambda p: FunctionCall(p[1], p[2], p[3]),
)

yacc.yacc()
