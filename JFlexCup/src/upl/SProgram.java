package upl;

class SProgram implements AST {

  StmtList stmtList;

  public SProgram(StmtList stmtList) {
    this.stmtList = stmtList;
  }

  public String toString() {
    return("Program:\n=============\n umm "); //+stmtList);
  }

}

