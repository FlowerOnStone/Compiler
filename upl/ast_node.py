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

    def dump(self, level, file, en=""):
        pass

    def indent(self, level, file):
        print("    " * level, end="", file=file)


class Statement(AST): ...


class Program(AST):
    body = None

    def __str__(self) -> str:
        return (
            f"Program(body=["
            + ",".join([str(statement) for statement in self.body])
            + "])"
        )

    def dump(self, level, file, en=""):
        print("Program(body=[", file=file)
        for index in range(len(self.body)):
            en = ","
            if index + 1 == len(self.body):
                en = ""
            self.body[index].dump(level + 1, file, en)
        print("])", file=file)


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

    def dump(self, level, file, en=""):
        print("Variable[", file=file)
        self.indent(level, file)
        print(f"name={self.name},", file=file)
        self.indent(level, file)
        print(f"type={self.type},", file=file)
        self.indent(level, file)
        print(f"value={self.value}", file=file)
        self.indent(level - 1, file)
        print("]", en, sep="", file=file)


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

    def dump(self, level, file, en=""):
        print("Constant[", file=file)
        self.indent(level, file)
        print(f"type={self.type},", file=file)
        self.indent(level, file)
        print(f"value={self.value}", file=file)
        self.indent(level - 1, file)
        print("]", en, sep="", file=file)

    type: str
    value = None


class Expression(AST):
    def __str__(self) -> str:
        return f"Expression[left={self.left},operation={self.operation},right={self.right}]"

    def dump(self, level, file, en=""):
        print("Expression[", file=file)
        self.indent(level, file)
        print(f"left=", end="", file=file)
        self.left.dump(level + 1, file, en=",")
        self.indent(level, file)
        print(f"operation={self.operation}", file=file)
        self.indent(level, file)
        print(f"right=", end="", file=file)
        self.right.dump(level + 1, file, en="")
        self.indent(level - 1, file)
        print("]", en, sep="", file=file)

    left = None
    operation = None
    right = None


class CompareExpression(AST):
    def __str__(self) -> str:
        return f"CompareExpression[left={self.left},operation={self.operation},right={self.right}]"

    left = None
    operation = None
    right = None

    def dump(self, level, file, en=""):
        print("CompareExpression[", file=file)
        self.indent(level, file)
        print(f"left=", end="", file=file)
        self.left.dump(level + 1, file, en=",")
        self.indent(level, file)
        print(f"operation={self.operation}", file=file)
        self.indent(level, file)
        print(f"right=", end="", file=file)
        self.right.dump(level + 1, file, en="")
        self.indent(level - 1, file)
        print("]", en, sep="", file=file)


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

    def dump(self, level, file, en=""):
        self.indent(level, file)
        print("IfStatement[", file=file)
        self.indent(level + 1, file)
        print(f"condition=", end="", file=file)
        self.condition.dump(level + 2, file, en=",")
        self.indent(level + 1, file)
        print(f"body=[", file=file)
        if self.else_body == None:
            for index in range(len(self.body)):
                en = ","
                if index + 1 == len(self.body):
                    en = ""
                self.body[index].dump(level + 2, file, en)
            self.indent(level + 1, file)
            print("]", file=file)
        else:
            for index in range(len(self.body)):
                en = ","
                if index + 1 == len(self.body):
                    en = ""
                self.body[index].dump(level + 2, file, en)
            self.indent(level + 1, file)
            print("],", file=file)
            self.indent(level + 1, file)
            print(f"else_body=[", file=file)
            for index in range(len(self.else_body)):
                en = ","
                if index + 1 == len(self.else_body):
                    en = ""
                self.else_body[index].dump(level + 2, file, en)
            self.indent(level + 1, file)
            print("]", file=file)
        self.indent(level, file)
        print("]", en, sep="", file=file)


class DoWhileStatement(Statement):
    condition = None
    body = None

    def __str__(self) -> str:
        return (
            f"DoWhileStatement[condition={self.condition},body=["
            + ",".join([str(statement) for statement in self.body])
            + "]]"
        )

    def dump(self, level, file, en=""):
        self.indent(level, file)
        print("DoWhileStatement[", file=file)
        self.indent(level + 1, file)
        print(f"condition=", end="", file=file)
        self.condition.dump(level + 2, file, en=",")
        self.indent(level + 1, file)
        print(f"body=[", file=file)
        for index in range(len(self.body)):
            en = ","
            if index + 1 == len(self.body):
                en = ""
            self.body[index].dump(level + 2, file, en)
        self.indent(level + 1, file)
        print("]", file=file)
        self.indent(level, file)
        print("]", en, sep="", file=file)


class PrintStatement(Statement):
    body = None

    def __str__(self) -> str:
        return f"PrintStatement[body={self.body}]"

    def dump(self, level, file, en=""):
        self.indent(level, file)
        print("PrintStatement[", file=file)
        self.indent(level + 1, file)
        print(f"body=", end="", file=file)
        self.body.dump(level + 2, file, en="")
        self.indent(level, file)
        print("]", en, sep="", file=file)


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

    def dump(self, level, file, en=""):
        self.indent(level, file)
        print("Declaration[", file=file)
        self.indent(level + 1, file)
        print(f"variable=", end="", file=file)
        self.variable.dump(level + 2, file, en=",")
        self.indent(level + 1, file)
        print(f"value=", end="", file=file)
        if self.value == None:
            print("None", file=file)
        else:
            self.value.dump(level + 2, file, en="")
        self.indent(level, file)
        print("]", en, sep="", file=file)


class DeclarationStatement(Statement):

    def __str__(self) -> str:
        return (
            f"DeclarationStatement[type={self.type},variables=["
            + ",".join([str(variable) for variable in self.variables])
            + "]]"
        )

    def dump(self, level, file, en=""):
        self.indent(level, file)
        print("DeclarationStatement[", file=file)
        self.indent(level + 1, file)
        print(f"type={self.type},", file=file)
        self.indent(level + 1, file)
        print(f"variables=[", file=file)
        for index in range(len(self.variables)):
            if index + 1 < len(self.variables):
                self.variables[index].dump(level + 2, file, en=",")
            else:
                self.variables[index].dump(level + 2, file, en="")
        self.indent(level + 1, file)
        print("]", file=file)
        self.indent(level, file)
        print("]", en, sep="", file=file)

    type = None
    variables = None


class AssignStatement(Statement):

    def __str__(self) -> str:
        return f"AssignStatement[variable={self.variable},value={self.value}]"

    def dump(self, level, file, en=""):
        self.indent(level, file)
        print("AssignStatement[", file=file)
        self.indent(level + 1, file)
        print(f"variable=", end="", file=file)
        self.variable.dump(level + 2, file, en=",")
        self.indent(level + 1, file)
        print(f"value=", end="", file=file)
        self.value.dump(level + 2, file, en="")
        self.indent(level, file)
        print("]", en, sep="", file=file)

    variable = None
    value = None
