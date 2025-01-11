from dataclasses import dataclass

@dataclass
class DataConv:
    """Donnees d'une convention (sans les contraintes custom)
    """
    mjs : list[str] # liste des noms des mjs
    rondes : list[str] # liste des noms des rondes
    scenars : list[str] # liste des scenars
    intervalScenar : list[list[int]] # liste des bornes infs et sup des scenars. 
                                    # Le scenar i a comme borne sup intervalScenar[i][1] et inf intervalScenar[i][0] 
    equipes : list[str] # liste des noms des équipes
    dispMj : list[list[list[int]]] # disponibilité des mjs "le mj i est dispo à la ronde j pour le scenar k"
    dispPj : list[list[int]] # disponibilité des pjs "l'equipe i, à la ronde j est composée de dispPj[i,j] personnes"
    dispVol : list[int] # dispo pjs volant "à la ronde j il y a dispVol[j] pjs volants"
    valScenar : list[list[int]] # l'equipe k, associe au scenar l la valeur valScenar[k][l]
    nChoix : int # nombre de choix que chaque equipe donne
    estAuteur : list[bool] #si le mj m est un auteur

@dataclass
class ResultatsConv:
    assMj : list[list[list[bool]]] # Le mj i joue à la ronde j le scenar k ssi assMj[i][j][k] == 1
    assEquipe : list[list[list[list[bool]]]] # le mj i mjise à la ronde j à l'equipe k le scenar l ssi assEquipe[i][j][k][l]==1
    assVolant : list[list[bool]] # Le mj i dispose à la ronde j de assVolant[i][j] pjs volants
    success : int # =1 ssi le solveur a trouvé une solution
    objectiveValue : float # valeur de la fonction objectif

if __name__ == "__main__":
    d = DataConv(["toto"],["ronde 1"],["au bord du yop"], [[1],[2]],["les totoros"], [[[1]]], [[2]], [1], [[200]])
    print(d)