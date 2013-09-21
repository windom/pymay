from pyparsing import Forward, Word, alphas, Suppress, OneOrMore, Group
from pyparsing import ZeroOrMore, Keyword, delimitedList, MatchFirst, ParserElement
from ast import Variable, Abstraction, Application, Definition, LetExpression

def SuppressedKeyword(literal):
    return Keyword(literal).suppress()

def makeApplications(toks):
    expr = toks.pop(0)
    for tok in toks:
        expr = Application(expr, tok)
    return expr

LET, IN = map(SuppressedKeyword, ["let", "in"])
LMB, ABSTR, EQ, LPAR, RPAR = map(Suppress, ["\\", "->", "=", "(", ")"])
keyword = MatchFirst([LET, IN])

variable = (~keyword + Word(alphas)).addParseAction(lambda s, loc, toks: Variable(toks[0]))

expression = Forward()

abstraction = (LMB + Group(OneOrMore(variable)) + ABSTR + expression) \
        .addParseAction(lambda s, loc, toks: Abstraction(list(toks[0]), toks[1]))

atom = variable | abstraction | (LPAR + expression + RPAR)

smpexpression = OneOrMore(atom).addParseAction(lambda s, loc, toks: makeApplications(toks))

definition = (variable + Group(ZeroOrMore(variable)) + EQ + expression) \
        .addParseAction(lambda s, loc, toks: Definition(toks[0], list(toks[1]), toks[2]))

letexpression = (LET + Group(delimitedList(definition, delim=",")) + IN + expression) \
        .addParseAction(lambda s, loc, toks: LetExpression(list(toks[0]), toks[1]))

expression << (letexpression | smpexpression)

def parse(s):
    return expression.parseString(s, parseAll=True)[0]
