import _ast
from Scanner import Token, TokenType


class AST:
    def __init__(self, token: Token) -> None:
        self.lineno = token.row
        self.col_offset = token.col
        pass

    lineno: int
    col_offset: int
    end_lineno: int
    end_col_offset: int
    type_comment: str

    def dump(self, level, en=""):
        pass

    def indent(self, level):
        print("    " * level, end="")


class Statement(AST): ...


class Program(AST):
    body = None

    def __str__(self) -> str:
        return (
            f"Program(body=["
            + ",".join([str(statement) for statement in self.body])
            + "])"
        )

    def dump(self, level, en=""):
        print("Program(body=[")
        for index in range(len(self.body)):
            en = ","
            if index + 1 == len(self.body):
                en = ""
            self.body[index].dump(level + 1, en)
        print("])")


class Operation(AST):

    def __init__(self, token: Token) -> None:
        super().__init__(token)
        self.name = token.lexeme

    def __str__(self) -> str:
        return f"Operation[name={self.name}]"

    name = None


class CompareOperation(AST):
    def __init__(self, token: Token) -> None:
        super().__init__(token)
        self.name = token.lexeme

    def __str__(self) -> str:
        return f"CompareOperation[name={self.name}]"

    name = None


class Variable(AST):
    def __init__(self, token: Token) -> None:
        super().__init__(token)
        self.name = token.lexeme

    def __str__(self) -> str:
        return f"Variable[name={self.name},type={self.type},value={self.value}]"

    name: str
    type = None
    value = None

    def dump(self, level, en=""):
        print("Variable[")
        self.indent(level)
        print(f"name={self.name},")
        self.indent(level)
        print(f"type={self.type},")
        self.indent(level)
        print(f"value={self.value}")
        self.indent(level - 1)
        print("]", en, sep="")


class Constant(AST):
    def __init__(self, token: Token) -> None:
        super().__init__(token)
        if token.token_t == TokenType.CONST_INT:
            self.type = "int"
            self.value = int(token.lexeme)
        else:
            self.type = "bool"
            if token.lexeme == "true":
                self.value = True
            else:
                self.value = False

    def __str__(self) -> str:
        return f"Constant[type={self.type},value={self.value}]"

    def dump(self, level, en=""):
        print("Constant[")
        self.indent(level)
        print(f"type={self.type},")
        self.indent(level)
        print(f"value={self.value}")
        self.indent(level - 1)
        print("]", en, sep="")

    type: str
    value = None


class Expression(AST):
    def __str__(self) -> str:
        return f"Expression[left={self.left},operation={self.operation},right={self.right}]"

    def dump(self, level, en=""):
        print("Expression[")
        self.indent(level)
        print(f"left=", end="")
        self.left.dump(level + 1, en=",")
        self.indent(level)
        print(f"operation={self.operation}")
        self.indent(level)
        print(f"right=", end="")
        self.right.dump(level + 1, en="")
        self.indent(level - 1)
        print("]", en, sep="")

    left = None
    operation = None
    right = None


class CompareExpression(AST):
    def __str__(self) -> str:
        return f"CompareExpression[left={self.left},operation={self.operation},right={self.right}]"

    left = None
    operation = None
    right = None

    def dump(self, level, en=""):
        print("CompareExpression[")
        self.indent(level)
        print(f"left=", end="")
        self.left.dump(level + 1, en=",")
        self.indent(level)
        print(f"operation={self.operation}")
        self.indent(level)
        print(f"right=", end="")
        self.right.dump(level + 1, en="")
        self.indent(level - 1)
        print("]", en, sep="")


class IfStatement(Statement):
    condition = None
    body = None
    else_body = None

    def __str__(self) -> str:
        result = (
            f"IfStatement[condition={self.condition},body=["
            + ",".join([str(statement) for statement in self.body])
            + "],else_body="
        )
        if self.else_body == None:
            result += "None]"
        else:
            result = (
                result
                + "["
                + ",".join([str(statement) for statement in self.else_body])
                + "]]"
            )
        return result

    def dump(self, level, en=""):
        self.indent(level)
        print("IfStatement[")
        self.indent(level + 1)
        print(f"condition=", end="")
        self.condition.dump(level + 2, en=",")
        self.indent(level + 1)
        print(f"body=[")
        if self.else_body == None:
            for index in range(len(self.body)):
                en = ","
                if index + 1 == len(self.body):
                    en = ""
                self.body[index].dump(level + 2, en)
            self.indent(level + 1)
            print("]")
        else:
            for index in range(len(self.body)):
                en = ","
                if index + 1 == len(self.body):
                    en = ""
                self.body[index].dump(level + 2, en)
            self.indent(level + 1)
            print("],")
            self.indent(level + 1)
            print(f"else_body=[")
            for index in range(len(self.else_body)):
                en = ","
                if index + 1 == len(self.else_body):
                    en = ""
                self.else_body[index].dump(level + 2, en)
            self.indent(level + 1)
            print("]")
        self.indent(level)
        print("]", en, sep="")


class DoWhileStatement(Statement):
    condition = None
    body = None

    def __str__(self) -> str:
        return (
            f"DoWhileStatement[condition={self.condition},body=["
            + ",".join([str(statement) for statement in self.body])
            + "]]"
        )

    def dump(self, level, en=""):
        self.indent(level)
        print("DoWhileStatement[")
        self.indent(level+1)
        print(f"condition=", end="")
        self.condition.dump(level + 2, en=",")
        self.indent(level + 1)
        print(f"body=[")
        for index in range(len(self.body)):
            en = ","
            if index + 1 == len(self.body):
                en = ""
            self.body[index].dump(level + 2, en)
        self.indent(level + 1)
        print("]")
        self.indent(level)
        print("]", en, sep="")


class PrintStatement(Statement):
    body = None

    def __str__(self) -> str:
        return f"PrintStatement[body={self.body}]"

    def dump(self, level, en=""):
        self.indent(level)
        print("PrintStatement[")
        self.indent(level + 1)
        print(f"body=", end="")
        self.body.dump(level + 2, en="")
        self.indent(level)
        print("]", en, sep="")


class Type(Statement):
    def __init__(self, token: Token) -> None:
        super().__init__(token)
        if token.token_t == TokenType.INT_T:
            self.name = "int"
        else:
            self.name = "bool"

    def __str__(self) -> str:
        return f"Type[name={self.name}]"

    name = None


class Declaration(Statement):

    def __str__(self) -> str:
        return f"Declaration[variable={self.variable},value={self.value}]"

    variable = None
    value = None

    def dump(self, level, en=""):
        self.indent(level)
        print("Declaration[")
        self.indent(level + 1)
        print(f"variable=", end="")
        self.variable.dump(level + 2, en=",")
        self.indent(level + 1)
        print(f"value=", end="")
        if self.value == None:
            print("None")
        else:
            self.value.dump(level + 2, en="")
        self.indent(level)
        print("]", en, sep="")


class DeclarationStatement(Statement):

    def __str__(self) -> str:
        return (
            f"DeclarationStatement[type={self.type},variables=["
            + ",".join([str(variable) for variable in self.variables])
            + "]]"
        )

    def dump(self, level, en=""):
        self.indent(level)
        print("DeclarationStatement[")
        self.indent(level + 1)
        print(f"type={self.type},")
        self.indent(level + 1)
        print(f"variables=[")
        for index in range(len(self.variables)):
            if index + 1 < len(self.variables):
                self.variables[index].dump(level + 2, en=",")
            else:
                self.variables[index].dump(level + 2, en="")
        self.indent(level + 1)
        print("]")
        self.indent(level)
        print("]", en, sep="")

    type = None
    variables = None


class AssignStatement(Statement):

    def __str__(self) -> str:
        return f"AssignStatement[variable={self.variable},value={self.value}]"

    def dump(self, level, en=""):
        self.indent(level)
        print("AssignStatement[")
        self.indent(level + 1)
        print(f"variable=", end="")
        self.variable.dump(level + 2, en=",")
        self.indent(level + 1)
        print(f"value=", end="")
        self.value.dump(level + 2, en="")
        self.indent(level)
        print("]", en, sep="")

    variable = None
    value = None
