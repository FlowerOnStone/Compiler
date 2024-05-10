package upl;

class SPrint extends Stmt implements AST {

  TExpr expr;

  public SPrint(TExpr expr) {
    this.expr = expr;
  }

  public String toString() {
    return "SPrint\n";
  }

}





