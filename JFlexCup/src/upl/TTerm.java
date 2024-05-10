package upl;


public class TTerm implements AST {
  // ADD  M_Exr
  TMExpr expr;

  public TTerm (TMExpr expr) {
    this.expr = expr;
  }

  public TTerm () {
    this.expr = null;
  }

  public String toString() {
    return "TTerm\n";
  }

}

