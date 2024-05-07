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


class Statement(AST): ...


class Program(AST):
    body = None

    def __str__(self) -> str:
        return (
            f"Program[body=["
            + ",".join([str(statement) for statement in self.body])
            + "]]"
        )


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

    type: str
    value = None


class Expression(AST):
    def __str__(self) -> str:
        return f"Expression[left={self.left},operation={self.operation},right={self.right}]"

    left = None
    operation = None
    right = None


class CompareExpression(AST):
    def __str__(self) -> str:
        return f"CompareExpression[left={self.left},operation={self.operation},right={self.right}]"

    left = None
    operation = None
    right = None


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


class DoWhileStatement(Statement):
    condition = None
    body = None
    def __str__(self) -> str:
        return (
            f"DoWhileStatement[condition={self.condition},body=["
            + ",".join([str(statement) for statement in self.body])
            + "]]"
        )


class PrintStatement(Statement):
    body = None

    def __str__(self) -> str:
        return f"PrintStatement[body={self.body}]"


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


class DeclarationStatement(Statement):

    def __str__(self) -> str:
        return (
            f"DeclarationStatement[type={self.type},variables=["
            + ",".join([str(variable) for variable in self.variables])
            + "]]"
        )

    type = None
    variables = None


class AssignStatement(Statement):

    def __str__(self) -> str:
        return f"AssignStatement[variable={self.variable},value={self.value}]"

    variable = None
    value = None
