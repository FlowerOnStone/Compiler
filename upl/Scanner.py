import enum

class TokenType(enum.Enum):
    LEFT_BRACKET = 0,
    RIGHT_BRACKET = 1,
    LEFT_PARENTHESIS = 2,
    RIGHT_PARENTHESIS = 3,
    INT_T = 4,
    BOOL_T = 5,
    IDENTIFIER = 6,
    NUMBER = 7,
    ROP = 8,
    DO = 9,
    WHILE = 10,
    IF = 11, 
    THEN = 12,
    ELSE = 13,
    PRINT = 14,
    TOTAL_TOKENS = 15


class Token:
    def __init__(self, type: TokenType, lexeme: str, col: int, row: int) -> None:
        self.type = type
        self.lexeme = lexeme
        self.col = col
        self.row = row 

    def __str__(self) -> str:
        return f"({self.lexeme})"

class Scanner():
    regex = [""] * TOTAL_TOKENS
    # TODO: Fill in the regex array

    def __init__(self) -> None:
        pass

    def scan(self, filename:str) -> None:
        pass
    
    def separate(line:str) -> list:
        pass

    def read(self) -> None:
        pass

    def getTokenType(self) -> TokenType:
        pass

    def nextToken(self) -> Token:
        pass

if __name__ == "__main__":
    tmp = TokenType.ELSE
    print(tmp)