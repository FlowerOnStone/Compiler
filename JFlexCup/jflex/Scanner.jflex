package upl;

import java_cup.runtime.*;
import java.io.*;


%%


%class Scanner
%cup
%line
%column
%{
  StringBuffer string = new StringBuffer();

  private Symbol symbol(int type) {
      return new Symbol(type, yyline, yycolumn);
    }
  private Symbol symbol(int type, Object value) {
      return new Symbol(type, yyline, yycolumn, value);
    }
%}
%eofval{
    System.out.println("EOF"); return symbol(sym.EOF);
%eofval}


LEFT_BRACKET = [(]
RIGHT_BRACKET = [)]

LEFT_PARENTHESIS = "{"
RIGHT_PARENTHESIS = "}"

ADD = [+]
MUL = [*]

INT_T = (int)
BOOL_T = (bool)

BEGIN = (begin)
END = (end)

CONST_BOOL = (true) | (false)
CONST_INT = [0]|[1-9][0-9]*

IDENTIFIER = [a-zA-Z]+[0-9]*
// ROP = ==|<=|>=|=|<|>
GREATER = >
GREATER_EQUAL = >=
EQUAL = ==
ASSIGN = [=]

DO = (do)
WHILE = (while)
IF = (if)
THEN = (then)
ELSE = (else)
PRINT = (print)
SEMICOLON = ;

ONELINE_CMT = "//".*
MULTILINE_CMT = [/][*][^*]*[*]+([^*/][^*]*[*]+)*[/]

%%
{DO}                {System.out.println("(DO, " + yytext()+")"); return symbol(sym.DO);}
{WHILE}             {System.out.println("(WHILE, " + yytext()+")"); return symbol(sym.WHILE);}
{IF}                {System.out.println("(IF, " + yytext()+")"); return symbol(sym.IF);}
{THEN}              {System.out.println("(THEN, " + yytext()+")"); return symbol(sym.THEN);}
{ELSE}              {System.out.println("(ELSE, " + yytext()+")"); return symbol(sym.ELSE);}
{PRINT}             {System.out.println("(PRINT, " + yytext()+")"); return symbol(sym.PRINT);}
{INT_T}             {System.out.println("(INT_T, " + yytext()+")"); return symbol(sym.INT_T);}
{BOOL_T}            {System.out.println("(BOOL_T, " + yytext()+")"); return symbol(sym.BOOL_T);}
{BEGIN}             {System.out.println("(BEGIN, " + yytext()+")"); return symbol(sym.BEGIN);}
{END}               {System.out.println("(END, " + yytext()+")"); return symbol(sym.END);}
{CONST_BOOL}        {System.out.println("(CONST_BOOL, " + yytext()+")"); return symbol(sym.CONST_BOOL);}
{CONST_INT}         {System.out.println("(CONST_INT, " + yytext()+")"); return symbol(sym.CONST_INT);}
{ADD}               {System.out.println("(ADD, " + yytext()+")"); return symbol(sym.ADD);}
{MUL}               {System.out.println("(MUL, " + yytext()+")"); return symbol(sym.MUL);}
{LEFT_BRACKET}      {System.out.println("(LEFT_BRACKET, " + yytext()+")"); return symbol(sym.LEFT_BRACKET);}
{RIGHT_BRACKET}     {System.out.println("(RIGHT_BRACKET, " + yytext()+")"); return symbol(sym.RIGHT_BRACKET);}
{LEFT_PARENTHESIS}  {System.out.println("(LEFT_PARENTHESIS, " + yytext()+")"); return symbol(sym.LEFT_PARENTHESIS);}
{RIGHT_PARENTHESIS} {System.out.println("(RIGHT_PARENTHESIS, " + yytext()+")"); return symbol(sym.RIGHT_PARENTHESIS);}
{IDENTIFIER}        {System.out.println("(IDENTIFIER, " + yytext()+")"); return symbol(sym.IDENTIFIER);}
{ASSIGN}            {System.out.println("(ASSIGN, " + yytext()+")"); return symbol(sym.ASSIGN);}
 {GREATER}           {System.out.println("(ROP, " + yytext()+")"); return symbol(sym.GREATER);}
 {GREATER_EQUAL}     {System.out.println("(ROP, " + yytext()+")"); return symbol(sym.GREATER_EQUAL);}
 {EQUAL}             {System.out.println("(ROP, " + yytext()+")"); return symbol(sym.EQUAL);}
//{ROP}               {System.out.println("(ROP, " + yytext()+")"); return symbol(sym.ROP);}
{SEMICOLON}         {System.out.println("(SEMICOLON, " + yytext()+")"); return symbol(sym.SEMICOLON);}

{ONELINE_CMT}       {} // Ignore {System.out.println("(ONELINE_CMT, " + yytext()+")"); return symbol(sym.ONELINE_CMT);}
{MULTILINE_CMT}     {} // Ignore {System.out.println("(MULTILINE_CMT, " + yytext()+")"); return symbol(sym.MULTILINE_CMT);}


// [/][*]              { } // Ignore. System.out.println("Unterminated comment"); return symbol(sym.UNTERMINATED_CMT); }


[ \t\r\n\f] { /* ignore white space. */ }

. { System.out.println("Illegal character: line "+yyline + " col " + yycolumn); return symbol(sym.ILLEGAL);}
