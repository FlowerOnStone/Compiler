package upl;

public class TExpr implements AST {
  TMExpr e;
  TExprTail tail;

  public TExpr(TMExpr e, TExprTail tail) {
    this.e = e;
    this.tail = tail;
  }

  public String toString() {
    return "TExpr\n";
  }
}




