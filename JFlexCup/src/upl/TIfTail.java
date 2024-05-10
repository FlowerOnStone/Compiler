package upl;

public class TIfTail implements AST {
  StmtList body;

  public TIfTail (StmtList body) {
    this.body = body;
  }

  public TIfTail () {
    this.body = null;
  }

  public String toString() {
    return "IfTail\n";
  }
}
