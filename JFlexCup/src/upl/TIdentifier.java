package upl;

public class TIdentifier implements AST, TY {
  String var_name;
  TType t; // TODO: hmm

  public TIdentifier (String var_name) {
    this.var_name = var_name;
  }

  public String toString() {
    return "[Identifier " + var_name + "]\n";
  }
}


