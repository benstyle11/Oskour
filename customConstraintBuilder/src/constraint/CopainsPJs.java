package constraint;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class CopainsPJs implements Constraint {
    private HashMap<String, String> attributes;

    public CopainsPJs(Scanner s) {
        attributes = new HashMap<>();
        s.nextLine();
        ArrayList<String> names = Utility.attributeNames("equipe 1", "equipe 2");
        for (String str : names){
            System.out.printf("Attribute for [" + str + "] : ");
            String s1 = s.nextLine();
            attributes.put(str, s1);
        }
    }
    
    public String toYaml(){
        String res = "";
        res += "- type: CopainsPJs\n";
        for (String s : new ArrayList<>(attributes.keySet()).reversed()){
            res += "\t" + s + ": " + attributes.get(s) + "\n";
        } 
        
        return res;
    }

    public String toString(){
        return attributes.toString();
    }
}
