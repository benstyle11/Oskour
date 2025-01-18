import sys, os

from oskour.dataStructure  import DataConv, ResultatsConv
from oskour.ioFunc import save_to_file, import_data, import_custom_constraint_from_file
from oskour.convSolver import solve
from oskour.postProcessing import displayConv
from oskour.customConstraint import CustomConstraintContainer

def import_solve_export(input_path:str,output_path:str, custom_constraints:list[CustomConstraintContainer] = []):
        
    dataConv:DataConv = import_data(input_path)
    
    path_constraints = os.path.join(input_path,"custom_constraints.yaml")
    if os.path.exists(path_constraints):
        c = import_custom_constraint_from_file(path_constraints,dataConv)
        custom_constraints.append(c)
    resConv:ResultatsConv = solve(dataConv,custom_constraints)
    if resConv.success:
        displayConv(dataConv,resConv)
        save_to_file(dataConv,resConv)

def main():
    if len(sys.argv) >= 2:
        input_path = sys.argv[1]
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    import_solve_export(input_path,output_path)

if __name__ == "__main__":
    main()