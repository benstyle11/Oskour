import argparse


def create_parser()->argparse.ArgumentParser:
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