# Simple Lexical Analyzer Implementation

## Table of Contents
1. [📑Context-free Grammar](#grammar)
2. [⚙️ Implementing Lexical Analyzer](#implementing)
3. [🍒 Run](#run)
4. [👤 Our team](#team)


## 📑 \ Context-free Grammar <a name="grammar"></a>

```
SS -> begin <stmtList> end

// T = (){};+*=, int, bool, <Id>, <Number>, <ROP>, do, while, if, then, else, print

<stmtList>    ->  <stmt>;<stmtList> | epsilon

<stmt>  -> if <Expr> then { <stmtList> } <ifTail>
        | do { <stmtList> } while (<Expr>)
        | <Assignment>
        | <Declaration>
        | print(<Expr>)                     // should be some function or just print?

<ifTail> -> else { <stmtList> } | epsilon	// else part for IF command

<Declaration>   -> <Type> <L>
<Type>          -> int | bool
<L>             -> <L1><L2>
<L1>            -> <Id> | <Assignment> 
<L2>		-> , <L> | epsilon		// Multiple variables declaration

<Assignment> -> <Id> = <Expr>               // int a = true: should be caught on next phase, not parser

<Expr>      -> <M-Expr> <Tmp>
<Tmp>       -> ROP <M-Expr>  | epsilon          // <ROP> is right-associative
<M-Expr>    -> <Term> <METail>
<METail>    -> + <M-Expr> | epsilon
<Y>         -> Id | Number

# right-associative
<Term>      -> <Factor> <T2>
<Factor>    -> <Y> | (<M-Expr>) 
<T2>        -> * <Term> | epsilon
```

## \ ⚙️  Implementing  <a name="implementing"></a>

```py
class TokenType(IntEnum):
    DO = auto()
    WHILE = auto()
    IF = auto()
    ...

class Token(token_t: TokenType, lexeme: str, col: int, row: int)

class Scanner():
    # defined regex here
    # regex[TokenType.DO] = r"do\b"
    # ...
    def scan(self, path: str) -> None:
        # Parse a file into scanner
        pass

    def nextToken(self) -> Token:
        # return the next token
        pass
```

#### Output
```py
# pseudo code for testing
def main():
    scanner.scan("./inp")
    while token = scanner.nextToken():
        if token.type is EOF: break
        if token.type is UNKNOWN: alert(), exit()
        print(token)
```

![](https://cdn.discordapp.com/attachments/915575548959420416/1223127770276560936/example.png?ex=6618b981&is=66064481&hm=0b8d5607051fe5f6b2f38f871fcae49396cdc861ea5d3c8680e604c0a0b7abb4&)

## 🍒 Run <a name="run"></a>

```sh
~/Compiler/Lexical-Analyzer/v1-Code  ··································································
❯ ./Scanner.py file_path
```


## 👤 Our team <a name="team"></a>

- 21020055 Tran Thuy-Dung
- 21020037 Nguyen Duc-Thuan
- 21020455 Le Quoc-Toan
