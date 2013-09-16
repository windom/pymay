from utils import PrettyPrinter

class Expression:
    def __str__(self):
        pp = PrettyPrinter()
        self.prettyPrint(pp)
        return str(pp)


class Variable(Expression):
    def __init__(self, name):
        self.name = name
    
    def prettyPrint(self, pp, **args):
        pp += self.name


class Abstraction(Expression):
    def __init__(self, variables, body):
        self.variables = variables
        self.body = body
        
    def prettyPrint(self, pp, **args):
        pp += "(\\"
        pp.join(self.variables)
        pp += " -> "
        pp += self.body
        pp += ")"

        
class Application(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def prettyPrint(self, pp, parens=False, **args):
        if parens:
            pp += "("
        pp += self.left
        pp += " "
        self.right.prettyPrint(pp, parens=True)
        if parens:
            pp += ")"


class Definition:
    def __init__(self, variable, parameters, body):
        self.variable = variable
        self.parameters = parameters
        self.body = body
        
    def prettyPrint(self, pp, **args):
        pp.join([self.variable] + self.parameters)
        pp += " = "
        pp += self.body


class LetExpression(Expression):
    def __init__(self, definitions, expression):
        self.definitions = definitions
        self.expression = expression
    
    def prettyPrint(self, pp, **args):
        pp.addTab()
        pp += "let "
        pp.addTab()
        pp += self.definitions[0]
        for definition in self.definitions[1:]:
            pp += ","
            pp.newLine()
            pp += definition
        pp.delTab()
        pp.newLine()
        pp += "in  "
        pp += self.expression
        pp.delTab()

