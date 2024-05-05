
### Our group: 

- 21020055 Trần Thùy Dung 
- 21020037 Nguyễn Đức Thuận 
- 21020455 Lê Quốc Toản

```
S -> begin <stmtList> end

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

## 19/03/2024: 5h20-7h45 Toan & Dung working on grammar and scanner
TODO:  Dung

- regex for comments: van de do split() cac words
- parser
- color printer

## 21/03/2024

**Steps for making Parser.**

- Eliminate left recursion
- Loai bo de quy gian tiep
- FIRST & FOLLOW

## 22/03/2024: 10PM
Grammar