from enum import IntEnum, auto
from Scanner import *
from ast_node import *

# Sau này sẽ có class Compiler để manage tương tác giữa Scanner và Parser
# Thay vì Scanner là 1 attribute của Parser -> passing arguments overhead


"""
Tại sao cần: Vẫn cần ID để phân biệt các token với nhau.
IntEnum.
"""


class SymbolType(IntEnum):
    # TODO: Thay đổi, vì văn phạm mới có thể có S', F' gì đó
    S = auto()
    STMT_LIST = auto()
    EXPR = auto()
    M_EXPR = auto()
    ...


class Symbol:
    """
    Trả về trong get_production(current_symbol, next_sym):
    [Symbol, Symbol, ...]
    nó khác với [SymbolType, SymbolType, ..] ở chỗ có giá trị cụ thể,
    StartToken đi kèm row, col để báo lỗi khi cần...
    """

    _type = 0  # SymbolType
    start_token = None
    # Giả sử symbol S,
    # dùng dẫn xuất S -> begin stmtList end  thì start_token = TokenType.BEGIN

    val = 0  # NOTE: ignore, pha sau mới dùng

    def __init__(self, name, productions=[]):
        self.__name__ = name


class Grammar:
    # người dùng ko nhìn thấy
    # PRODUCTION = dict()
    # FIRST = dict()
    # FOLLOW = dict() i.e. FOLLOW[SymbolType]
    # parse_table = None

    def get_production(current_symbol, next_sym) -> [Symbol]:
        pass


class Parser:
    # Output là [[Symbol],...]

    scanner = Scanner()
    current_token = None

    def __init__(self) -> None:
        pass

    def token(self):
        return self.current_token

    def match(self):
        while True:
            self.current_token = self.scanner.nextToken()
            if self.current_token.token_t != TokenType.UNKNOWN:
                break
        print(self.current_token)

    def parse(self, path) -> list:
        """
        Trả về List Productions có dạng:
        [
            [BEGIN, stmtList, END],
            [Symbol, Symbol, Symbol...],
            [Symbol, Symbol],
            [..]
        ]

        Lý do không cần vế trái vì chúng ta parse leftmost nên
        vế trái là non-terminal trái nhất trên cây tính đến thời điểm hiện tại.
        Mỗi lúc dẫn xuất ta chọn lại sinh các con mới cho nút hiện tại.
        """

        self.scanner.scan(path)
        self.match()
        result = self.parser_start()
        result.dump(0)

    def parser_start(self) -> bool:
        """
        S -> begin <stmtList> end
        """
        result = Program(self.token())
        if self.token().token_t != TokenType.BEGIN:
            return False
        self.match()
        result.body = self.parser_statement_list()
        if result.body == False:
            return False
        if self.token().token_t != TokenType.END:
            return False
        self.match()
        if self.token().token_t != TokenType.EOF:
            return False
        return result

    def parser_statement_list(self):
        """
        <stmtList> ->  <stmt> <stmtList> | epsilon
        """
        result= [self.parser_statement()]
        if result[0] == False:
            return False
        if (
            self.token().token_t == TokenType.END
            or self.token().token_t == TokenType.RIGHT_PARENTHESIS
        ):
            return result
        result.extend(self.parser_statement_list())
        return result

    def parser_statement(self) -> bool:
        """
        <stmt>  -> if <Expr> then { <stmtList> } <ifTail>
                | do { <stmtList> } while (<Expr>)
                | <Assignment>
                | <Declaration>
                | print(<Expr>)
        """
        if (
            self.token().token_t == TokenType.INT_T
            or self.token().token_t == TokenType.BOOL_T
        ):
            return self.parser_declaration()
        if self.token().token_t == TokenType.IF:
            return self.parser_if_condition()
        if self.token().token_t == TokenType.IDENTIFIER:
            return self.parser_assignment()
        if self.token().token_t == TokenType.PRINT:
            return self.parse_print_statement()
        if self.token().token_t == TokenType.DO:
            return self.parse_do_while_statement()
        return False

    def parser_declaration(self) -> bool:
        """
        <Declaration>   -> <Type> <L>
        """
        result = DeclarationStatement(self.token())
        declaration_type = self.parser_type()
        if declaration_type == False:
            return False
        result.type = declaration_type
        variables = self.parser_l()
        if variables[0] == False:
            return False
        result.variables = variables
        print(result)
        if self.token().token_t != TokenType.SEMICOLON:
            return False
        self.match()
        return result

    def parser_if_condition(self) -> bool:
        """
        if <Expr> then { <stmtList> } <ifTail>
        """
        result = IfStatement(self.token())
        if self.token().token_t != TokenType.IF:
            return False
        self.match()
        result.condition= self.parser_expression()
        if result.condition == False:
            return False
        if self.token().token_t != TokenType.THEN:
            return False
        self.match()
        if self.token().token_t != TokenType.LEFT_PARENTHESIS:
            return False
        self.match()
        result.body = self.parser_statement_list()
        if result.body == False:
            return False
        if self.token().token_t != TokenType.RIGHT_PARENTHESIS:
            return False
        self.match()
        result.else_body = self.parser_if_tail()
        return result

    def parser_if_tail(self) -> bool:
        """
        <ifTail> -> else { <stmtList> } | epsilon
        """
        if self.token().token_t != TokenType.ELSE:
            return None
        self.match()
        if self.token().token_t != TokenType.LEFT_PARENTHESIS:
            return False
        self.match()
        result = self.parser_statement_list()
        if result == False:
            return False
        if self.token().token_t != TokenType.RIGHT_PARENTHESIS:
            return False
        self.match()
        return result

    def parser_assignment(self) -> bool:
        """
        <Assignment> -> <Id> = <Expr>;
        """
        if self.token().token_t != TokenType.IDENTIFIER:
            return False
        result = AssignStatement(self.token())
        result.variable = Variable(self.token())
        self.match()
        if self.token().token_t != TokenType.ASSIGN:
            return False
        self.match()
        result.value = self.parser_expression()
        if result.value == False:
            return False
        if self.token().token_t != TokenType.SEMICOLON:
            return False
        self.match()
        print(result)
        return result

    def parse_print_statement(self) -> bool:
        """
        print(<Expr>);
        """
        result = PrintStatement(self.token())
        if self.token().token_t != TokenType.PRINT:
            return False
        self.match()
        if self.token().token_t != TokenType.LEFT_BRACKET:
            return False
        self.match()
        result.body = self.parser_expression()
        if result.body == False:
            return False
        if self.token().token_t != TokenType.RIGHT_BRACKET:
            return False
        self.match()
        if self.token().token_t != TokenType.SEMICOLON:
            return False
        self.match()
        print(result)
        return result

    def parse_do_while_statement(self) -> bool:
        """
        do { <stmtList> } while (<Expr>);
        """
        result = DoWhileStatement(self.token())
        if self.token().token_t != TokenType.DO:
            return False
        self.match()
        if self.token().token_t != TokenType.LEFT_PARENTHESIS:
            return False
        self.match()
        result.body = self.parser_statement_list()
        if result.body == False:
            return False
        if self.token().token_t != TokenType.RIGHT_PARENTHESIS:
            return False
        self.match()
        if self.token().token_t != TokenType.WHILE:
            return False
        self.match()
        if self.token().token_t != TokenType.LEFT_BRACKET:
            return False
        self.match()
        result.condition = self.parser_expression()
        if result.condition == False:
            return False
        if self.token().token_t != TokenType.RIGHT_BRACKET:
            return False
        self.match()
        if self.token().token_t != TokenType.SEMICOLON:
            return False
        self.match()
        return result

    def parser_type(self):
        """
        <Type>          -> int | bool
        """
        if (
            self.token().token_t != TokenType.INT_T
            and self.token().token_t != TokenType.BOOL_T
        ):
            return False
        result = Type(self.token())
        print(result)
        self.match()
        return result

    def parser_l(self):
        """
        <L>             -> <L1><L2>
        """
        result =  [self.parser_l1()]
        result.extend(self.parser_l2())
        return result

    def parser_l1(self):
        """
        <L1>            -> <Id> <Declaration_Assignment>
        """
        if self.token().token_t != TokenType.IDENTIFIER:
            return False
        variable = Variable(self.token())
        result = Declaration(self.token())
        result.variable = variable
        self.match()
        if (
            self.token().token_t == TokenType.COMMA
            or self.token().token_t == TokenType.SEMICOLON
        ):
            print(result)
            return result
        if self.token().token_t == TokenType.ASSIGN:
            result.value = self.parser_declaration_assignment()
            print(result)
            return result
        return False
    def parser_l2(self):
        """
        <L2>		-> , <L> | epsilon
        """
        if self.token().token_t == TokenType.SEMICOLON:
            return [] 
        if self.token().token_t != TokenType.COMMA:
            return False
        self.match()
        return self.parser_l()

    def parser_declaration_assignment(self):
        """
        <Declaration_Assignment> -> = <Expr> | epsilon
        """
        if self.token().token_t != TokenType.ASSIGN:
            return None
        self.match()
        if (
            self.token().token_t != TokenType.IDENTIFIER
            and self.token().token_t != TokenType.CONST_INT
            and self.token().token_t != TokenType.CONST_BOOL
            and self.token().token_t != TokenType.LEFT_BRACKET
        ):
            return None
        return self.parser_expression()

    def parser_expression(self):
        """
        <Expr>      -> <M-Expr> <Tmp>
        """
        result = CompareExpression(self.token())
        left = self.parser_m_expression()
        if left == False:
            return False
        op, right = self.parser_tmp()
        if op == None:
            return left
        result.left = left
        result.operation = op
        result.right = right
        print(result)
        return result

    def parser_tmp(self):
        """
        <Tmp>       -> ROP <M-Expr>  | epsilon
        """
        if self.token().token_t != TokenType.ROP:
            return None, None
        op = CompareOperation(self.token())
        print(op)
        self.match()
        right = self.parser_m_expression()
        return op, right

    def parser_m_expression(self):
        """
        <M-Expr>    -> <Term> <METail>
        """
        result = Expression(self.token())
        left = self.parser_term()
        if left == False:
            return False
        op, right = self.parser_metail()
        if op == None:
            return left
        result.left = left
        result.operation = op
        result.right = right
        print(result)
        return result

    def parser_metail(self) -> bool:
        """
        <METail>    -> + <M-Expr> | epsilon
        """
        if self.token().token_t != TokenType.ADD:
            return None, None
        op = Operation(self.token())
        print(op)
        self.match()
        right = self.parser_m_expression()
        return op, right

    def parser_term(self) -> bool:
        """
        <Term>      -> <Factor> <T2>
        """
        result = Expression(self.token())
        left = self.parser_factor()
        if left == False:
            return False
        result.left = left
        op, right = self.parser_t2()
        if op == None:
            return left
        result.operation = op
        result.right = right
        print(result)
        return result

    def parser_t2(self):
        """
        <T2>        -> * <Term> | epsilon
        """
        if self.token().token_t != TokenType.MUL:
            return None, None
        op = Operation(self.token())
        self.match()
        right = self.parser_term()
        return op, right

    def parser_factor(self):
        """
        <Factor>    -> <Y> | (<M-Expr>)
        """
        if self.token().token_t == TokenType.LEFT_BRACKET:
            self.match()
            result = self.parser_m_expression()
            if result == False:
                return False
            if self.token().token_t != TokenType.RIGHT_BRACKET:
                return False
            self.match()
            return result
        return self.parser_y()

    def parser_y(self):
        """
        <Y>         -> Id | Number
        """
        if self.token().token_t == TokenType.IDENTIFIER:
            result = Variable(self.token())
            print(result)
            self.match()
            return result
        if (
            self.token().token_t == TokenType.CONST_INT
            or self.token().token_t == TokenType.CONST_BOOL
        ):
            result = Constant(self.token())
            print(result)
            self.match()
            return result
        return False


if __name__ == "__main__":
    parser = Parser()
    parser.parse("test.upl")
