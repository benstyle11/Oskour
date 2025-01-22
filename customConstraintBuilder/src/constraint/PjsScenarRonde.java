package constraint;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class PjsScenarRonde implements Constraint {
    private HashMap<String, String> attributes;

    public PjsScenarRonde(Scanner s) {
        attributes = new HashMap<>();
        s.nextLine();
        ArrayList<String> names = Utility.attributeNames("equipe1", "ronde", "scenar");
        for (String str : names){
            System.out.printf("Attribute for [" + str + "] : ");
            String s1 = s.nextLine();
            if (str.equals("ronde")){
                s1 = "Ronde " + s1;
            }
            attributes.put(str, s1);
        }
    }

    public String toYaml(){
        String res = "";
        res += "- type: PjsScenarRonde\n";
        for (String s : new ArrayList<>(attributes.keySet()).reversed()){
            res += "  " + s + ": " + attributes.get(s) + "\n";
        } 
        
        return res;
    }

    public String toString(){
        return attributes.toString();
    }
}
