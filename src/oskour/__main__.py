import sys, os

import argparse

from oskour.dataStructure  import DataConv, ResultatsConv
from oskour.ioFunc import save_to_file, import_data, import_custom_constraint_from_file
from oskour.convSolver import solve
from oskour.postProcessing import displayConv
from oskour.customConstraint import CustomConstraintContainer

def import_solve_export(input_path:str,output_path:str, omnipotent:bool=False, timelimit: float =None, nthreads:int = (os.cpu_count() -1)):
    custom_constraints:list[CustomConstraintContainer] = []
    dataConv:DataConv = import_data(input_path,omnipotent_mj=omnipotent)
    
    path_constraints = os.path.join(input_path,"custom_constraints.yaml")
    if os.path.exists(path_constraints):
        c = import_custom_constraint_from_file(path_constraints,dataConv)
        custom_constraints.append(c)
    resConv:ResultatsConv = solve(dataConv,custom_constraints,timelimit,nthreads)
    if resConv.success:
        displayConv(dataConv,resConv)
        save_to_file(dataConv,resConv,output_path)

def main():
    
    parser = argparse.ArgumentParser(prog="Oskour",description="Programme de PLNE résolvant le problème de la convention")
    parser.add_argument("inputdirectory",default=None ,help="Répertoire d'entrée, doit contenir: \n Equipes.csv : Noms, disponibilité et voeux des equipes \
                         \n MJ.csv: Noms, disponibilité et capacité des mjs \
                            \n param_conv.csv: paramètres de la convention, nombre de Rondes et de choix\
                            \n PjVolants.csv: Nombre de Pjs volants à chaque Ronde \
                            \n Scenars.csv: Nom et nombre de pj de chaque scenar (dans le meme ordre que dans MJ.csv)")
    parser.add_argument("outputdirectory",default=None ,help="Répertoire de sortie")
    parser.add_argument("--omnipotent", action="store_true",help="Rend les mjs omnipotents, ie pouvant mjser tout scenario")
    parser.add_argument("--maxtime", action="store",type=float)
    parser.add_argument("--nthreads", action="store", type=int)
    args = parser.parse_args()
    
    input_path = args.inputdirectory
    output_path = args.outputdirectory
    omnipotent = args.omnipotent
    maxtime = args.maxtime
    nthreads = args.nthreads
    import_solve_export(input_path,output_path,omnipotent,maxtime,nthreads)

if __name__ == "__main__":
    main()