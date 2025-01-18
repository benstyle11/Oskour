from dataclasses import astuple
import os

import pulp as pl
import numpy as np

from oskour.customConstraint import CustomConstraintContainer
from oskour.dataStructure import DataConv, ResultatsConv
from oskour.valueFunctions import defaultValueFunction
if __name__ == "__main__":
    import oskour.postProcessing as postProcessing

"""
i : un mjs,
j : une ronde,
k : une equipe;
l : un scenar
"""


def solve(dataConv:DataConv,customConsList:list[CustomConstraintContainer]=[],timelimit=None, nthreads:int=(os.cpu_count()-1)) -> ResultatsConv:
    mjs,rondes, scenars,intervalScenar, equipes, dispMj, dispPj, dispVol, valScenar, nChoix,estAuteur = astuple(dataConv)
    # declaration du pb, avec maximalisation du bousin
    prob = pl.LpProblem("Probleme_de_la_convention", pl.LpMaximize)
    
    ## define datas

    intervalScenar = pl.makeDict([["min", "max"], scenars], intervalScenar) # interval min/max du scenar l

    dispMj = pl.makeDict([mjs,rondes,scenars],dispMj) #dispo du mj i à la ronde j pr le scenar l

    dispPj = pl.makeDict([equipes,rondes],dispPj) #nb de joueurs de l'equipe k a la ronde j

    dispVol = pl.makeDict([rondes], dispVol) # dispo des pjs volants à la ronde j
    
    estAuteur = pl.makeDict([mjs], dataConv.estAuteur) # le mjs i est auteur

    valScenar = pl.makeDict([equipes, scenars], valScenar) # valeur pour l equipe k du scenar l

    ## define variables

    # le mj i joue a la ronde j le scenar l
    assMj = pl.LpVariable.dicts("AssMj", (mjs,rondes,scenars), cat="Binary") 

    # le mj i à la ronde j meujise a l equipe k le scenar l
    assEquipe = pl.LpVariable.dicts("AssEquipe", (mjs,rondes,equipes,scenars), cat="Binary")  

    # le mj i dispose a la ronde j de assVolant[i][j] en +
    assVolant = pl.LpVariable.dicts("AssVolant", (mjs,rondes),lowBound=0, cat="Integer")

    ## ADD Custom Constraints

    for c in customConsList:
        for cons in c.get_copains_pj_scenar_ronde():
            for i in mjs:
                prob += assEquipe[i][cons.ronde][cons.E1][cons.scenar] == assEquipe[i][cons.ronde][cons.E2][cons.scenar]
            prob += pl.lpSum([assEquipe[i][cons.ronde][cons.E1][cons.scenar] for i in mjs]) == 1
        for cons in c.get_pas_copains_pj():
            for i in mjs:
                for j in rondes:
                    for k in scenars:
                        e1 = assEquipe[i][j][cons.E1][k]
                        e2 = assEquipe[i][j][cons.E2][k]
                        prob += e1 + e2 <= 1
        for cons in c.get_copains_pj():
            for i in mjs:
                for j in rondes:
                    for l in scenars:
                        ## add constraint iff both are avail
                        if dispPj[cons.E1][j] >0 and dispPj[cons.E2][j] > 0:
                            prob += assEquipe[i][j][cons.E1][l] == assEquipe[i][j][cons.E2][l]
        for cons in c.get_copains_pj_mj_scenar():
            prob += pl.lpSum([assEquipe[cons.MJ][j][cons.E][cons.S] for j in rondes]) == 1
        
        for cons in c.get_copains_pjs_ronde():
            for s in scenars:
                for m in mjs:
                    prob += assEquipe[m][cons.R][cons.E1][s] == assEquipe[m][cons.R][cons.E2][s]
        for cons in c.get_pj_scenar_ronde():
            prob += pl.lpSum([assEquipe[m][cons.ronde][cons.equipe][cons.scenar] for m in mjs]) == 1

    ## define constraints

    #A chaque ronde, une equipe joue au moins et au plus une fois si elle est dispo 

    for j in rondes:
        for k in equipes:
            prob += pl.lpSum([assEquipe[i][j][k][l] for i in mjs for l in scenars])*(dispPj[k][j]) == (dispPj[k][j])
            prob += pl.lpSum([assEquipe[i][j][k][l] for i in mjs for l in scenars]) <= (dispPj[k][j])


    # chaque equipe joue au plus une fois 1 scenar

    for k in equipes:
        for l in scenars:
            prob += pl.lpSum([assEquipe[i][j][k][l] for i in mjs for j in rondes]) <= 1


    # N pjs max respecté pour tout les scenars

    for i in mjs:
        for l in scenars:
            for j in rondes:
                prob += pl.lpSum([assEquipe[i][j][k][l]*dispPj[k][j] for k in equipes ]) <=  intervalScenar["max"][l]
    for i in mjs:
        for l in scenars:
            for j in rondes:            
                prob += assVolant[i][j] + pl.lpSum([assEquipe[i][j][k][l]*dispPj[k][j] for k in equipes ]) >= assMj[i][j][l]*intervalScenar["min"][l] 

    # une equipe ne peut jouer que si le mj est dispo

    for i in mjs:
        for l in scenars:
            for j in rondes:
                for k in equipes:
                    prob += assEquipe[i][j][k][l] <= assMj[i][j][l]

    # une equipe joue au pire un voeux 5
    
    for i in mjs:
        for j in rondes:
            for k in equipes:    
                for l in scenars:
                        if valScenar[k][l] == -1:
                            prob += assEquipe[i][j][k][l] == 0
    

    # mj ne joue qu'une fois et peut meujiser le scenar

    for i in mjs:
        for j in rondes:
            prob += pl.lpSum([assMj[i][j][l] for l in scenars]) <= 1 #max 1 meujisage par ronde
            for l in scenars:
                prob += assMj[i][j][l] <= dispMj[i][j][l] # peut meujiser le scenar



    ## nb de pjs volants assigne pas grand

    for j in rondes:
        prob += pl.lpSum([assVolant[i][j] for i in mjs]) <= dispVol[j]        
        
        
        
    ## fonction de cout        
    
    prob += -5 * pl.lpSum([assVolant[i][j] for i in mjs for j in rondes])\
        + pl.lpSum([pl.lpSum([assEquipe[i][j][k][l] for i in mjs for j in rondes])*defaultValueFunction(valScenar[k][l]) for k in equipes for l in scenars])\
        + 15.*pl.lpSum([estAuteur[m]*assMj[m][r][s] for m in mjs for r in rondes for s in scenars])

    solver = pl.apis.PULP_CBC_CMD(timeLimit=timelimit,threads=nthreads)
    
    
    prob.solve(solver)
    
    success = (prob.status == 1)
    
    resConv = ResultatsConv(assMj,assEquipe,assVolant,success,prob.objective.value())
    
    return resConv # returns the solution


if __name__ == "__main__":
    nMj = 15
    nRondes = 3
    nScenar = 3
    nEquipes = 20

    mjs = range(nMj)
    rondes = range(nRondes)
    scenars = list(range(nScenar))
    scenars[0] = "patates douces et chimpanzees"
    scenars[1] = "Marianne a la plage"
    scenars[2] = "envi de craimebrulee"
    equipes = range(nEquipes)

    intervalScenar = [
        [3]*nScenar,
        [6]*nScenar
    ]

    dispMj = [[
        [1]*nScenar
    ]*nRondes]*nMj

    dispPj = [[2]*nRondes]*nEquipes

    dispVol = [15]*nRondes

    valScenar = [[i for i in range(len(scenars))] for j in equipes]
    nChoix = 5
    estAuteur = [False for i in mjs]

    dataConv = DataConv(mjs,rondes,scenars,intervalScenar,equipes,dispMj,dispPj,dispVol,valScenar,nChoix,estAuteur)
    
    resultatsConv: ResultatsConv = solve(dataConv,[],timelimit=20)
    success = resultatsConv.success
    #display everything
    if success:
        postProcessing.displayConv(dataConv, resultatsConv)
    
