package constraint;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class PasCopainsPjs implements Constraint {
    private HashMap<String, String> attributes;

    public PasCopainsPjs(Scanner s) {
        attributes = new HashMap<>();
        s.nextLine();
        ArrayList<String> names = Utility.attributeNames("equipe1", "equipe2");
        for (String str : names){
            System.out.printf("Attribute for [" + str + "] : ");
            attributes.put(str, s.nextLine());
        }
    }

    public String toYaml(){
        String res = "";
        res += "- type: PasCopainsPjs\n";
        for (String s : new ArrayList<>(attributes.keySet()).reversed()){
            res += "  " + s + ": " + attributes.get(s) + "\n";
        } 
        
        return res;
    }

    public String toString(){
        return attributes.toString();
    }
}
