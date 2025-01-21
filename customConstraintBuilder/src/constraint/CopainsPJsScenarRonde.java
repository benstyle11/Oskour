package constraint;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class CopainsPJsScenarRonde implements Constraint {
    private HashMap<String, String> attributes;

    public CopainsPJsScenarRonde(Scanner s) {
        attributes = new HashMap<>();
        s.nextLine();
        ArrayList<String> names = Utility.attributeNames("equipe 1", "equipe 2", "ronde", "scenar");
        for (String str : names){
            System.out.printf("Attribute for [" + str + "] : ");
            attributes.put(str, s.nextLine());
        }
    }

    public String toYaml(){
        String res = "";
        res += "- type: CopainsPJsScenarRonde\n";
        for (String s : new ArrayList<>(attributes.keySet()).reversed()){
            res += "\t" + s + ": " + attributes.get(s) + "\n";
        } 
        
        return res;
    }

    public String toString(){
        return attributes.toString();
    }
}
