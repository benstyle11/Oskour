package constraint;
import java.util.ArrayList;

public class Utility {
    public static ArrayList<String> attributeNames(String... args){
        ArrayList<String> list = new ArrayList<>();
        for (String s: args){
            list.add(s);
        }

        return list;
    }
}
