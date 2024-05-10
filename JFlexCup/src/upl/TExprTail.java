package upl;


public class TExprTail implements AST {

  TRop rop;
  TMExpr expr;

  public TExprTail (TRop rop, TMExpr expr) {
    this.rop = rop;
    this.expr = expr;
  }

  public TExprTail () {
    this.rop = null;
    this.expr = null;
  }

  public String toString() {
    return "TExprTail\n";
  }

}







