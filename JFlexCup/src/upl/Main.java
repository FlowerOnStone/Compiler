package upl;


import java_cup.runtime.*;
import java.io.*;


public class Main{
    public static void main(String[] args) throws Exception{

      
       Scanner s=null;
	    if (args.length==0) 
            s= new Scanner(new InputStreamReader(System.in));
	    else 
            s = new Scanner(new InputStreamReader(new java.io.FileInputStream(args[0])));

      Parser p = new Parser(s);
     //  System.out.println("What");
     //
     SProgram ss = (SProgram) p.parse().value;
    // System.out.println(ss);


      
     //    
      // Symbol status = null;
      // do{
      //     status=p.scan();
      // System.out.println(status);
      // }while(status.sym != sym.EOF);
        
        //s.yylex();
    }
}
