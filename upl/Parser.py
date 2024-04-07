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


class Symbol():
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

    val = 0 # NOTE: ignore, pha sau mới dùng

    def __init__(self, name, productions = []):
        self.__name__ = name

class Grammar():
    # người dùng ko nhìn thấy
    # PRODUCTION = dict()
    # FIRST = dict()  
    # FOLLOW = dict() i.e. FOLLOW[SymbolType]
    # parse_table = None

    def get_production(current_symbol, next_sym) -> [Symbol]:
        pass
        

class Parser:
    # Output là [[Symbol],...]

    grammar = None

    s = Scanner()

    def __init__(self, grammar) -> None:
        self.grammar = grammar

    def parse(path) -> list: 
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

        self.s.scan(path)



