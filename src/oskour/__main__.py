import sys

from oskour.dataStructure  import DataConv, ResultatsConv
from oskour.ioFunc import save_to_file, import_data
from oskour.convSolver import solve
from oskour.postProcessing import displayConv

def import_solve_export(input_path:str,output_path:str, custom_constraints = []):
    dataConv:DataConv = import_data(input_path)
    resConv:ResultatsConv = solve(dataConv,custom_constraints)
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