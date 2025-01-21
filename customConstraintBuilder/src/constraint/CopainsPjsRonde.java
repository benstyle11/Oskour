package constraint;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class CopainsPjsRonde implements Constraint {
    private HashMap<String, String> attributes;

    public CopainsPjsRonde(Scanner s) {
        attributes = new HashMap<>();
        s.nextLine();
        ArrayList<String> names = Utility.attributeNames("equipe 1", "equipe 2", "ronde");
        for (String str : names){
            System.out.printf("Attribute for [" + str + "] : ");
            String s1 = s.nextLine();
            attributes.put(str, s1);
        }
    }
    
    public String toYaml(){
        String res = "";
        res += "- type: CopainsPJsRonde\n";
        for (String s : new ArrayList<>(attributes.keySet()).reversed()){
            res += "\t" + s + ": " + attributes.get(s) + "\n";
        } 
        
        return res;
    }

    public String toString(){
        return attributes.toString();
    }
}
