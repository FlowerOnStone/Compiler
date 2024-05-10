package upl;


public class TAssignment extends Stmt implements AST {
  TIdentifier id;
  TExpr val;

  public TAssignment (TIdentifier id, TExpr val) {
    this.id = id;
    this.val = val;
  }

  public String toString() {
    return "TAssignment\n";
  }

}




