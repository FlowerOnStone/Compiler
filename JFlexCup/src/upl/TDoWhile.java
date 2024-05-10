package upl;

public class TDoWhile extends Stmt implements AST {

  StmtList  body;
  TExpr     cond;

  public TDoWhile (StmtList body, TExpr cond) {
    this.body = body;
    this.cond = cond;
  }

  public String toString() {
    return "Do-While\n";
  }

}



