package upl;


public class TIntLiteral implements AST, TY {
  // ADD  M_Exr
  Integer val;

  public TIntLiteral (String s) {
    try { val = Integer.parseInt(s); }
    catch (NumberFormatException e) { val=-1; };
  }

  public String toString() {
    return "TTerm\n";
  }

}



