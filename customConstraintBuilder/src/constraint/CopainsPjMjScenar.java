package constraint;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class CopainsPjMjScenar implements Constraint {
    private HashMap<String, String> attributes;

    public CopainsPjMjScenar(Scanner s) {
        attributes = new HashMap<>();
        s.nextLine();
        ArrayList<String> names = Utility.attributeNames("equipe1", "mj", "scenar");
        for (String str : names){
            System.out.printf("Attribute for [" + str + "] : ");
            String s1 = s.nextLine();
            attributes.put(str, s1);
        }
    }
    
    public String toYaml(){
        String res = "";
        res += "- type: CopainsPjMjScenar\n";
        for (String s : new ArrayList<>(attributes.keySet()).reversed()){
            res += "  " + s + ": " + attributes.get(s) + "\n";
        } 
        
        return res;
    }

    public String toString(){
        return attributes.toString();
    }
}
