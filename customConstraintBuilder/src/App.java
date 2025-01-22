import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Scanner;

import constraint.*;

public class App {
    public static void main(String[] args) throws Exception {
        boolean end = false;
        ArrayList<String> constraints = new ArrayList<>();
        constraints.add("CopainsPjMjScenar");
        constraints.add("CopainsPJs");
        constraints.add("CopainsPjsRonde");
        constraints.add("CopainsPjsScenarRonde");
        constraints.add("PasCopainsPjs");
        constraints.add("PjsScenarRonde");
        Scanner s = new Scanner(System.in);
        String toWrite = "";

        while (!end){
            System.out.println("Which constraint to write ?");
            for (int i = 0; i < constraints.size(); i++){
                System.out.println(i + ": " + constraints.get(i));
            }
            System.out.printf("> ");
            int input = s.nextInt();
            Constraint c = null;
            switch (input){
                case 0: c = new CopainsPjMjScenar(s);break;
                case 1: c = new CopainsPjs(s);break;
                case 2: c = new CopainsPjsRonde(s);break;
                case 3: c = new CopainsPjsScenarRonde(s);break;
                case 4: c = new PasCopainsPjs(s);break;
                case 5: c = new PjsScenarRonde(s);break;
                default: System.out.println("Number not reconized");return;
            }  
            System.out.println(c.toString());
            toWrite += c.toYaml();
            
            System.out.println("continue (y/N) ?");
            System.out.printf("> ");
            String ans = s.nextLine();
            if (ans.charAt(0) != 'y'){
                end = true;
            }
        }

        System.out.println("Erase existing file (y/N) ?");
        System.out.printf("> ");
        String ans = s.nextLine();
        if (ans.charAt(0) == 'y'){
            try(PrintWriter out = new PrintWriter(new FileWriter("custom_constraints.yaml"))){
                out.write(toWrite);
            }
        }
        else{
            String old = "";
            try(BufferedReader in = new BufferedReader(new FileReader("custom_constraints.yaml"))){
                while (in.ready()){
                    String str = in.readLine();
                    String correct = "";
                    for (char c : str.toCharArray()){
                        if (c != '\t'){
                            correct += String.valueOf(c);
                        }
                        else{
                            correct += "  ";
                        }
                    }
                    old += correct + "\n";
                }
            }
            try(PrintWriter out = new PrintWriter(new FileWriter("custom_constraints.yaml"))){
                out.write(old + toWrite);
            }
        }
    }
}
