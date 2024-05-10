package upl;

public class TIf extends Stmt implements AST {

  TExpr expr;
  StmtList body;
  TIfTail tail;

  public TIf (TExpr expr, StmtList body, TIfTail tail) {
    this.expr = expr;
    this.body = body;
    this.tail = tail;
  }

  public String toString() {
    return "If Statement\n";
  }

}


