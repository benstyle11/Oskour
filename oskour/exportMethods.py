import time, os

import pulp as pl

from dataStructure import DataConv, ResultatsConv



def save_to_file(dataConv:DataConv,resultatsConv:ResultatsConv, output="")->None:
    dir = "./output/"
    
    if output == "":
        output = time.strftime("Resultat_Conv_%Y_%m_%d_%H_h_%M_m_%S.csv",time.localtime(time.time()))
    path = os.path.join(dir,output)
    f = open(path,"w")
    
    f.write("Equipe,")
    for r in dataConv.rondes:
        f.write(f"Scenar {r}, MJ {r}, Equipes {r}")
        f.write(",")
    f.write("\n")
    for e in dataConv.equipes:
        f.write(e)
        f.write(",")
        for r in dataConv.rondes:
            joue = False
            for m in dataConv.mjs:
                for s in dataConv.scenars:
                    if pl.value(resultatsConv.assEquipe[m][r][e][s]) == 1:
                        joue = True
                        f.write(f"\"{s}\", \"{m}\", ")
                        f.write("\"")
                        for e2 in dataConv.equipes:
                            if pl.value(resultatsConv.assEquipe[m][r][e2][s]) == 1:
                                f.write(f"|| {e2} ||")
                        f.write("\"")
                    
            if not(joue):
                f.write(",,")
            f.write(",")
        f.write("\n")
    
    
    f.close()
