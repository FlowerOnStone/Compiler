package upl;


public class TMETail implements AST {
  // ADD  M_Exr
  TMExpr expr;

  public TMETail (TMExpr expr) {
    this.expr = expr;
  }

  public TMETail () {
    this.expr = null;
  }

  public String toString() {
    return "METail\n";
  }

}
