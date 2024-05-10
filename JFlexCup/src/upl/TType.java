package upl;

public class TType implements AST {
  String type_str;

  public TType (String t) {
    this.type_str = t;
  }

  public String toString() {
    return "Type " + type_str + "\n";
  }
}

