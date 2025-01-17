import pulp as pl

from oskour.dataStructure import DataConv,ResultatsConv
from oskour.valueFunctions import defaultValueFunction

def displayConv(dataConv:DataConv,resultatsConv:ResultatsConv)->None:
    """Affiche les resultats de la conv sur le terminal

    Args:
        dataConv (DataConv): Les donnees de la convention
        resultatsConv (ResultatsConv): Le resultat du solver
    """
    mjs,rondes,scenars,equipes = dataConv.getBasicData()
    assMj,assEquipe,assVolant = resultatsConv.getAttribution()
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







def printSuccesRate(objectiveValue, nEquipes, nRondes, nChoix):
    sRate = getSuccessRate(objectiveValue, nEquipes, nRondes, nChoix)
    print(f"Le taux de succès est de : {sRate}")



def getSuccessRate(objectiveValue:float, nEquipes:int, nRondes:int, nChoix:int)->int:
    """Retourne le taux de succès du solveur. 
    Il est défini comme le succes atteint divisé par 
    le maximum possible atteignable.

    Args:
        objectiveValue (float): La valeur de la fonction objectif obtenue
        nEquipes (int): le nombre d'equipes
        nRondes (int): le nombre de rondes
        nChoix (int): le nombre de choix

    Returns:
        int: le taux de succès
    """
    maxTheoretical = 0
    for i in range(nRondes):
        maxTheoretical += defaultValueFunction(i)*nEquipes
    
    return objectiveValue/maxTheoretical

    
    

        
                        
            