package upl;

/**
 * AST node for the whole program (top node).
 * 
 * Also contains two symbol tables, one for input variables,
 * one for function names. 
 *
 * All operations like context check, symbol table build up
 * etc. start here.
 */ 
public class StmtList implements AST {

  // Tparlist parlist;           // input variables
  // Tdekllist dekllist;         // function declarations 
  // Texplist explist;           // result expressions
  // Texplist arguments;         // input values  
  Stmt stmt;
  StmtList stmtList;

  public StmtList(Stmt stmt, StmtList stmtList) {
    this.stmt = stmt;
    this.stmtList = stmtList;
  }

  public StmtList() {
    this.stmt = null;
    this.stmtList = null;
  }


  public String toString() {
    return "StmtList bro!!\n";
  }

}
