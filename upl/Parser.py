from enum import IntEnum, auto
from Scanner import *

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
        print(self.parser_start())

    def parser_start(self) -> bool:
        if self.token().token_t != TokenType.BEGIN:
            return False
        self.match()
        if not self.parser_statement_list():
            return False
        if self.token().token_t != TokenType.END:
            return False
        self.match()
        if self.token().token_t != TokenType.EOF:
            return False
        return True

    def parser_statement_list(self):
        if not self.parser_statement():
            return False
        if (
            self.token().token_t == TokenType.END
            or self.token().token_t == TokenType.RIGHT_PARENTHESIS
        ):
            return True
        return self.parser_statement_list()

    def parser_statement(self) -> bool:
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
        if not self.parser_type():
            return False
        if not self.parser_l1():
            return False
        if self.token().token_t != TokenType.SEMICOLON:
            return False
        self.match()
        return True

    def parser_if_condition(self) -> bool:
        if self.token().token_t != TokenType.IF:
            return False
        self.match()
        if not self.parser_expression():
            return False
        if self.token().token_t != TokenType.THEN:
            return False
        self.match()
        if self.token().token_t != TokenType.LEFT_PARENTHESIS:
            return False
        self.match()
        if not self.parser_statement_list():
            return False
        if self.token().token_t != TokenType.RIGHT_PARENTHESIS:
            return False
        self.match()
        return self.parser_if_tail()

    def parser_if_tail(self) -> bool:
        if self.token().token_t != TokenType.ELSE:
            return True
        self.match()
        if self.token().token_t != TokenType.LEFT_PARENTHESIS:
            return False
        self.match()
        if not self.parser_statement_list():
            return False
        if self.token().token_t != TokenType.RIGHT_PARENTHESIS:
            return False
        self.match()
        return True

    def parser_assignment(self) -> bool:
        if self.token().token_t != TokenType.IDENTIFIER:
            return False
        self.match()
        if self.token().token_t != TokenType.ASSIGN:
            return False
        self.match()
        if not self.parser_expression():
            return False
        if self.token().token_t != TokenType.SEMICOLON:
            return False
        self.match()
        return True

    def parse_print_statement(self) -> bool :
        if self.token().token_t != TokenType.PRINT:
            return False
        self.match()
        if self.token().token_t != TokenType.LEFT_BRACKET:
            return False
        self.match()
        if not self.parser_expression():
            return False
        if self.token().token_t != TokenType.RIGHT_BRACKET:
            return False
        self.match()
        if self.token().token_t != TokenType.SEMICOLON:
            return False
        self.match()
        return True

    def parse_do_while_statement(self) -> bool:
        if self.token().token_t != TokenType.DO:
            return False
        self.match()
        if self.token().token_t != TokenType.LEFT_PARENTHESIS:
            return False
        self.match()
        if not self.parser_statement_list():
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
        if not self.parser_expression():
            return False
        if self.token().token_t != TokenType.RIGHT_BRACKET:
            return False
        self.match()
        if self.token().token_t != TokenType.SEMICOLON:
            return False
        self.match()
        return True

    def parser_type(self):
        if (
            self.token().token_t != TokenType.INT_T
            and self.token().token_t != TokenType.BOOL_T
        ):
            return False
        self.match()
        return True

    def parser_l1(self):
        if self.token().token_t != TokenType.IDENTIFIER:
            return False
        self.match()
        if self.token().token_t == TokenType.COMMA or self.token().token_t == TokenType.SEMICOLON:
            return True
        if self.token().token_t == TokenType.ASSIGN:
            return self.parser_declaration_assignment()
        return False

    def parser_declaration_assignment(self) -> bool:
        if self.token().token_t != TokenType.ASSIGN:
            return False
        self.match()
        if self.token().token_t != TokenType.IDENTIFIER and self.token().token_t != TokenType.CONST_INT and self.token().token_t != TokenType.CONST_BOOL and self.token().token_t != TokenType.LEFT_BRACKET:
            return False
        return self.parser_expression()

    def parser_expression(self) -> bool:
        if not self.parser_m_expression():
            return False
        return self.parser_tmp()

    def parser_tmp(self) -> bool:
        if self.token().token_t != TokenType.ROP:
            return True
        self.match()
        return self.parser_m_expression()

    def parser_m_expression(self) -> bool:
        if not self.parser_term():
            return False
        return self.parser_metail()

    def parser_metail(self) -> bool:
        if self.token().token_t != TokenType.ADD:
            return True
        self.match()
        return self.parser_m_expression()

    def parser_term(self) -> bool:
        if not self.parser_factor():
            return False
        return self.parser_t2()

    def parser_t2(self) -> bool:
        if self.token().token_t == TokenType.MUL:
            self.match()
            return self.parser_term()
        return True

    def parser_factor(self) -> bool:
        if self.token().token_t == TokenType.LEFT_BRACKET:
            self.match()
            if not self.parser_m_expression():
                return False
            if self.token().token_t != TokenType.RIGHT_BRACKET:
                return False
            self.match()
            return True
        return self.parser_y()

    def parser_y(self) -> bool:
        if self.token().token_t == TokenType.IDENTIFIER or self.token().token_t == TokenType.CONST_INT or self.token().token_t == TokenType.CONST_BOOL:
            self.match()
            return True
        return False

if __name__ == "__main__":
    parser = Parser()
    parser.parse("test.upl")
