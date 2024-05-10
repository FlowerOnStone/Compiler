package upl;


public class TRop implements AST {
  String op_str;

  public TRop (String op) {
    op_str = op;
  }

  public String toString() {
    return "TRop\n";
  }

}
