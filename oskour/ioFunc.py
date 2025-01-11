import time, os


import pandas as pd
import numpy as np
import pulp as pl

from oskourdataStructure import DataConv, ResultatsConv
from oskour.dataStructure import DataConv


def import_data(folder="./input/", omnipotent_mj=False):

    pathEquipes = os.path.join(folder,"Equipes.csv")
    pathMJ = os.path.join(folder,"MJ.csv")
    pathScenars = os.path.join(folder,"Scenars.csv")
    pathVolant = os.path.join(folder,"PjVolants.csv")
    pathParam = os.path.join(folder,"param_conv.csv")

    # read data
    data_equipes = pd.read_csv(pathEquipes)

    data_scenars = pd.read_csv(pathScenars)
    data_scenars = data_scenars.dropna()

    data_mj = pd.read_csv(pathMJ)
    data_mj = data_mj.iloc[:-4,:]
    data_mj = data_mj[data_mj["MJ"].notnull()]

    data_volants = pd.read_csv(pathVolant)

    data_param = pd.read_csv(pathParam)

    # parametres de la conv

    nRondes = data_param.nRondes[0]#3 # number of rondes
    nChoix = data_param.nChoix[0]#5 # number of choix de scenars
    print(f"Le nombre de rondes est {nRondes}")





    rondes = [f"Ronde {i+1}" for i in range(nRondes)]

    ## Pjs volants dispos pour la ronde
    dispVol = data_volants.iloc[0,:].to_list()


    #remove empty rows
    data_equipes = data_equipes.dropna(0,"all",subset=['Nom']).reset_index(drop=True)

    #fill Equipe du joueur avec nom+prenom si indiv
    data_equipes["Équipe du joueur"] = np.where( data_equipes["Équipe du joueur"] =="X",\
                                         data_equipes["Nom"] +" "+ data_equipes["Prénom"],data_equipes["Équipe du joueur"] )

    noms_equipes = data_equipes["Équipe du joueur"]

    ## get the lis of teams, ordered.
    equipes = sorted(list(set(noms_equipes.to_list())))


    ## get the dispPj array

    dispPj=[]

    for e in equipes:
        l_r = []
        for i in range(1,nRondes+1):
            l_r.append( np.count_nonzero(data_equipes[f"Ronde {i}"][data_equipes["Équipe du joueur"] == e] == "Oui"))
        dispPj.append(l_r)




    ## get the scenars
    scenars = list(data_scenars["Titre du scenar"])
    scenars_key = list(data_scenars.Code)

    intervalScenar = []

    intervalScenar.append(data_scenars["Nb de PJ min"].to_list())
    intervalScenar.append(data_scenars["Nb de PJ max"].to_list())



    print(f"Les scenars sont : {scenars}, {len(scenars)} en tout")

    print("")
    print("#"*20)
    print("")
    print(f"Les equipes sont {equipes}, {len(equipes)} en tout")



    valScenar = [[-1 for i in range(len(scenars)) ] for j in range(len(equipes))]

    for k in range(len(equipes)):
        for i in range(nChoix):
            ## trouver le i eme scenar dans les nChoix /!! i + 1
            nb = "er" if i==0 else "e"
            s = str(data_equipes[f"{1+i}{nb} Choix"][data_equipes["Équipe du joueur"]==equipes[k]].to_list()[0])

            if not s in scenars:
                print(f"SCENAR {s} IGNORE")
                continue

            index = scenars.index(s)

            print(f"L'equipe {equipes[k]} veut ke scenar {s} en voeux {i+1}")
            ## associer la valeur au scenar
            valScenar[k][index] = i

    nScenars = len(scenars)
    nEquipes = len(equipes)

    print("\n")

    mjs = data_mj["MJ"].to_list()

    nMj = len(mjs)

    dispMj = [[[0 for i in range(nScenars)] for j in range(nRondes)] for k in range(nMj)]

    isAuteur = [0 for i in mjs]


    ## Auteur ne joue que son scenar
    for k in range(nMj):
        for i in range(nScenars):
            if (data_mj.iloc[k,i+1]) == "Auteur":
                isAuteur[k] = 1

    for k in range(nMj):
        for i in range(nScenars):
            m = mjs[k]
            state = data_mj[data_mj["MJ"]==m].iloc[0,i+1]

            b = bool( (state in ["Joué", "MJsé"] and not isAuteur[k])   or state == "Auteur")
            b = b or omnipotent_mj

            if b:
                print(mjs[k], " a joué ", scenars[i])
            for j in range(nRondes):
                if(data_mj[f"Ronde {j+1}"].to_list()[k].upper() == "Y"):
                    dispMj[k][j][i] = b



    print(f"Les mj sont : {mjs}, avec {len(mjs)} en tout")

    dataConv = DataConv(mjs,rondes,scenars,intervalScenar,equipes,dispMj,dispPj,dispVol,valScenar,nChoix,isAuteur)

    return dataConv






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
                    if pl.value(resultatsConv.attrEquipe[m][r][e][s]) == 1:
                        joue = True
                        f.write(f"\"{s}\", \"{m}\", ")
                        f.write("\"")
                        for e2 in dataConv.equipes:
                            if pl.value(resultatsConv.attrEquipe[m][r][e2][s]) == 1:
                                f.write(f"|| {e2} ||")
                        f.write("\"")

            if not(joue):
                f.write(",,")
            f.write(",")
        f.write("\n")


    f.close()


if __name__ == "__main__":
    import_data(folder="./input/conv2023/")
