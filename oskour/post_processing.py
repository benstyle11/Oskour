import pulp as pl
import numpy as np
from dataStructure import *
from evalFunction import evalFunction
import time
import os

def displayConv(dataConv:DataConv,resultatsConv:ResultatsConv)->None:
    mjs,rondes,scenars,equipes = dataConv.mjs,dataConv.rondes,dataConv.scenars,dataConv.equipes
    assMj,assEquipe,assVolant = resultatsConv.assMj, resultatsConv.assEquipe, resultatsConv.assVolant
    print("Currently displaying mjs")
    nVolant = {}
    L_stats_scenars = [ 0 for i in range(dataConv.nChoix)]
    nDesir = 0
    for j in rondes:
        print("#"*20)
        print(f"pour la ronde {j} ")
        nVolant[j] = 0
        for i in mjs:
            print("-"*20)
            print(f"Le mj {i} joue :")
            nVolant[j] += pl.value(assVolant[i][j])
            for l in scenars:
                if(pl.value((assMj[i][j][l]))):
                    print(f"joue le scenar {l}!!!")
                for k in equipes:
                    if pl.value(assEquipe[i][j][k][l]) == 1:
                        valScenar = dataConv.valScenar[equipes.index(k)][scenars.index(l)]
                        print(f"le scenar {l} avec l equipe {k}, n° du choix : {1 + valScenar if valScenar != -1 else -100}")
                        if valScenar == -1: nDesir+=1
                        L_stats_scenars[valScenar] += 1
            print(f"avec {int(pl.value(assVolant[i][j]))} pj volant a ses cotes")
        print()
        print(f"Besoin de {nVolant[j]} pour cette ronde")
    print("#"*20)
    print("Données macro : ")
    for i in range(dataConv.nChoix):
        print(f"au total, le nombre de choix {i} est de : {L_stats_scenars[i]}")
    print(f"Scenar non désirés : {nDesir}")
    print("Données pjs volants :")
    for i in range(len(dataConv.rondes)):
        print(f"pour la ronde {i+1} : ", end="")
        print(int(nVolant[rondes[i]]), end="")
        print(" pjs volants")
    printSuccesRate(resultatsConv.objectiveValue, len(equipes), len(rondes), 5)



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





def printSuccesRate(objectiveValue, nEquipes, nRondes, nChoix):
    sRate = getSuccessRate(objectiveValue, nEquipes, nRondes, nChoix)
    print(f"Le taux de succès est de : {sRate}")



def getSuccessRate(objectiveValue, nEquipes, nRondes, nChoix):
    
    maxTheoretical = 0

    for i in range(nRondes):
        maxTheoretical += evalFunction(i)*nEquipes
    
    return objectiveValue/maxTheoretical

    
    

        
                        
            