package upl;


public class TDeclaration extends Stmt implements AST {
  TType t;
  TIdentifier var;
  TExpr val;

  public TDeclaration (TType t, TIdentifier var) {
    this.t = t;
    this.var = var;
    this.val = null;
  }

  public TDeclaration (TType t, TIdentifier var, TExpr val) {
    this.t = t;
    this.var = var;
    this.val = val;
  }

  public String toString() {
    return "TDeclaration\n";
  }

}





