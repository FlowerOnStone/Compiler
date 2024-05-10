package upl;

public class TMExpr implements AST {

  TTerm term;
  TMETail tail;

  Integer val;

  public TMExpr (TTerm term, TMETail tail) {
    this.term = term;
    this.tail = tail;

    this.val = null;
  }

  // public TMExpr (Integer val) {
  //   this.val = val;
  // }

  public String toString() {
    return "TMExpr\n";
  }

}



