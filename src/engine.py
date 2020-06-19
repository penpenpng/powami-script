import re

from enums import Token


class Env:
    vars = {}
    err = False

    @classmethod
    def init(cls, arg):
        cls.err = False
        cls.vars = {
            "ぽ～わ": arg,
            "わ～ぽ": "",
            "わわわ": "わ",
            "わわぽ": "",
            "わぽわ": "",
            "わぽぽ": "",
            "ぽわわ": "",
            "ぽわぽ": "",
            "ぽぽわ": "",
            "ぽぽぽ": "ぽ",
        }

    @classmethod
    def out(cls):
        return cls.vars["わ～ぽ"]


class Script:
    def __init__(self, *scripts):
        self.scripts = scripts

    def run(self):
        for s in self.scripts:
            if Env.err:
                return
            s.run()


class Assignment:
    def __init__(self, var, literal):
        self.var = var
        self.literal = literal

    def run(self):
        if Env.err:
            return

        Env.vars[self.var] = self.literal


class ControlStatement:
    def __init__(self, keyword, var, pattern, script):
        self.keyword = keyword
        self.var = var
        self.pattern = pattern
        self.script = script

    def run(self):
        if Env.err:
            return

        negated = self.keyword in (Token.NOT_IF, Token.NOT_WHILE)

        if self.pattern == "～":
            regex = None
        else:
            regex = re.sub(r"！？", "@1", self.pattern)
            regex = re.sub(r"！～", "@2", regex)
            regex = re.sub(r"！ー", "@3", regex)
            regex = re.sub(r"！！", "@4", regex)
            regex = re.sub(r"ー", "[ぽわ@1@2@3@4]", regex)
            regex = re.sub(r"？", "?", regex)
            regex = re.sub(r"～", "*", regex)
            regex = re.sub(r"@1", "？", regex)
            regex = re.sub(r"@2", "～", regex)
            regex = re.sub(r"@3", "ー", regex)
            regex = re.sub(r"@4", "！", regex)

        def condition():
            if regex is not None:
                try:
                    bl = bool(re.fullmatch(regex, Env.vars[self.var]))
                except Exception:
                    Env.err = True
                    return False
            else:
                bl = Env.vars[self.var] == ""

            if negated:
                bl = not bl

            return bl

        if self.keyword in (Token.IF, Token.NOT_IF):
            if condition():
                self.script.run()
        elif self.keyword in (Token.WHILE, Token.NOT_WHILE):
            step = 0
            while condition():
                step += 1
                if step > 1000:
                    Env.err = True
                    return
                self.script.run()
        else:
            raise Exception


class FunctionCall(Script):
    def __init__(self, symbol, *args):
        self.symbol = symbol
        self.args = args

    def run(self):
        if Env.err:
            return

        if len(self.args) == 1:
            x = self.args[0]
            xv = Env.vars[x]
        elif len(self.args) == 2:
            x, y = self.args
            xv = Env.vars[x]
            yv = Env.vars[y]
        else:
            raise Exception

        if self.symbol is Token.PUSH_LEFT:
            Env.vars[x] = yv + xv
        elif self.symbol is Token.PUSH_RIGHT:
            Env.vars[x] = xv + yv
        elif self.symbol is Token.POP_LEFT:
            if len(xv) <= 0:
                Env.vars[x] = ""
                Env.vars[y] = ""
            else:
                h, *s = xv
                Env.vars[x] = "".join(s)
                Env.vars[y] = h
        elif self.symbol is Token.POP_RIGHT:
            if len(xv) <= 0:
                Env.vars[x] = ""
                Env.vars[y] = ""
            else:
                *s, t = xv
                Env.vars[x] = "".join(s)
                Env.vars[y] = t
        elif self.symbol is Token.POP_LEFT_DISCARD:
            if len(xv) <= 0:
                Env.vars[x] = ""
            else:
                _, *s = xv
                Env.vars[x] = "".join(s)
        elif self.symbol is Token.POP_RIGHT_DISCARD:
            if len(xv) <= 0:
                Env.vars[x] = ""
            else:
                *s, _ = xv
                Env.vars[x] = "".join(s)
        elif self.symbol is Token.NEGATE:
            res = ""
            for c in xv:
                t = typeof(c)
                res += t[(valueof(c) + 1) % 2]
            Env.vars[x] = res
        elif self.symbol is Token.CWISE_AND:
            res = ""
            for c, d in zip(xv, yv):
                if typeof(c) != typeof(d):
                    continue
                t = typeof(c)
                cv = valueof(c)
                dv = valueof(d)
                res += t[min(cv, dv)]
            Env.vars[x] = res
        elif self.symbol is Token.CWISE_OR:
            res = ""
            for c, d in zip(xv, yv):
                if typeof(c) != typeof(d):
                    continue
                t = typeof(c)
                cv = valueof(c)
                dv = valueof(d)
                res += t[max(cv, dv)]
            Env.vars[x] = res
        elif self.symbol is Token.COPY:
            Env.vars[x] = yv
        else:
            raise Exception


def typeof(c):
    if c in "わぽ":
        return "わぽ"
    if c in "？！":
        return "？！"
    if c in "ー～":
        return "ー～"
    raise Exception


def valueof(c):
    if c in "わ？ー":
        return 0
    if c in "ぽ！～":
        return 1
    raise Exception
