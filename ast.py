from collections import defaultdict
from utils import PrettyPrinter


class Expression:
    def identifyVars(self):
        return self.identifyVariables(VariableContext())

    def __str__(self):
        pp = PrettyPrinter()
        self.prettyPrint(pp)
        return str(pp)


class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def identifyVariables(self, context):
        return context.get(self)

    def prettyPrint(self, pp, **args):
        pp += (self.name + str(hash(self) % 100))


class Abstraction(Expression):
    def __init__(self, variables, body):
        self.variables = variables
        self.body = body

    def identifyVariables(self, context):
        (self.variables, self.body) = context.using(
            self.variables,
            lambda: self.body.identifyVariables(context)
        )
        return self

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

    def identifyVariables(self, context):
        self.left = self.left.identifyVariables(context)
        self.right = self.right.identifyVariables(context)
        return self

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

    def identifyVariables(self, context):
        self.variable = context.new(self.variable)
        (self.parameters, self.body) = context.using(
            self.parameters,
            lambda: self.body.identifyVariables(context)
        )
        return self

    def prettyPrint(self, pp, **args):
        pp.join([self.variable] + self.parameters)
        pp += " = "
        pp += self.body


class LetExpression(Expression):
    def __init__(self, definitions, expression):
        self.definitions = definitions
        self.expression = expression

    def identifyVariables(self, context):
        self.definitions = [
            definition.identifyVariables(context)
            for definition in self.definitions
        ]
        self.expression = self.expression.identifyVariables(context)
        for definition in self.definitions:
            context.close(definition.variable)
        return self

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


class VariableContext:
    def __init__(self):
        self.variableStackMap = defaultdict(lambda: [])

    def stack(self, variable):
        return self.variableStackMap[variable.name]

    def new(self, variable):
        variable = Variable(variable.name)
        self.stack(variable).append(variable)
        return variable

    def get(self, variable):
        variableStack = self.stack(variable)
        if variableStack:
            return variableStack[-1]
        else:
            return self.new(variable)

    def close(self, variable):
        self.stack(variable).pop()

    def using(self, variables, body):
        variables = list(map(self.new, variables))
        bodyValue = body()
        list(map(self.close, variables))
        return (variables, bodyValue)
