from dataclasses import dataclass

import pulp as pl

from oskour.dataStructure import DataConv


@dataclass
class _CopainsPjsScenarRonde:
    E1:str
    E2:str
    ronde:str
    scenar:str


@dataclass
class _PjsScenarRonde:
    equipe:str
    ronde:str
    scenar:str
    
@dataclass
class _PasCopainsPjs:
    E1:str
    E2:str
@dataclass
class _CopainsPjs:
    E1:str
    E2:str
@dataclass
class _CopainsPjMjScenar:
    E:str
    MJ:str
    S:str
@dataclass
class _CopainsPjsRonde:
    E1:str
    E2:str
    R:str

class CustomConstraint:

    def __init__(self,dataConv:DataConv) -> None:
        
        self.__dataConv = dataConv
            
        self.__copains_pjs_Scenar_Ronde:list[_CopainsPjsScenarRonde] = []

        self.__pas_copains_pjs:list[_PasCopainsPjs] = []
        
        self.__copains_pjs:list[_CopainsPjs] = []
        
        self.__copains_pjs_ronde:list[_CopainsPjsRonde] = []

        self.__copains_pj_mj_scenar:list[_CopainsPjMjScenar] = []
        
        self.__pj_scenar_ronde:list[_PjsScenarRonde] = []
    
    def _checkPlayer(self,E):
        assert (E in self.__dataConv.equipes), f"EQUIPE {E} NON DEFINIE"
    def _checkScenar(self,S):
        assert (S in self.__dataConv.scenars), f"SCENAR {S} NON DEFINI"
    def _checkRonde(self,R):
        assert(R in self.__dataConv.rondes), f"RONDE {R} NON DEFINIE"
    def _checkMj(self,MJ):
        assert(MJ in self.__dataConv.mjs), f"MJ {MJ} NON DEFINIE"
    
    def add_copains_pjs_scenar_ronde(self,E1:str, E2:str, ronde:str, scenar:str)->None:
        """Ajoute la contrainte "équipe 1 veut jouer avec équipe 2 le scenar "scenar" sur la ronde "ronde""

        Args:
            E1 (str): équipe 1
            E2 (str): équipe 2
            ronde (str): ronde 
            scenar (str): scénar
        """
        self._checkPlayer(E1)
        self._checkPlayer(E2)
        self._checkRonde(ronde)
        self._checkScenar(scenar)
        
        self.__copains_pjs_Scenar_Ronde.append(_CopainsPjsScenarRonde(E1, E2, ronde, scenar))

    def add_copains_pjs_ronde(self,E1:str,E2:str,ronde:str):
        """Ajoute la contrainte "équipe 1 veut jouer avec équipe 2 sur la ronde "ronde""

        Args:
            E1 (str): _description_
            E2 (str): _description_
            ronde (str): _description_
        """
        self._checkPlayer(E1)
        self._checkPlayer(E2)
        self._checkRonde(ronde)
        
        self.__copains_pjs_ronde.append(_CopainsPjsRonde(E1,E2,ronde))

    def add_pas_copains_pjs(self,E1:str,E2:str)->None:
        """Ajoute la contrainte "équipe 1 et équipe 2 ne joueront pas ensemble"

        Args:
            E1 (str): _description_
            E2 (str): _description_
        """
        self._checkPlayer(E1)
        self._checkPlayer(E2)
        
        self.__pas_copains_pjs.append(_PasCopainsPjs(E1, E2))
    
    def add_copain_pj_mj_scenar(self,E:str,MJ:str,scenar:str):
        """Ajoute la contrainte "équipe 1 veut jouer avec mj MJ sur le scénar "scenar"

        Args:
            E (str): equipe
            MJ (str): mj
            scenar (str): scenar
        """
        self._checkPlayer(E)
        self._checkMj(MJ)
        self._checkScenar(scenar)

        self.__copains_pj_mj_scenar.append(_CopainsPjMjScenar(E, MJ, scenar))
    
    def add_copains_pjs(self,E1:str,E2:str)->None:
        """Ajoute la contrainte "équipe 1 et équipe 2 joueront toujours ensemble"

        Args:
            E1 (str): equipe 1
            E2 (str): equipe 2
        """
        self._checkPlayer(E1)
        self._checkPlayer(E2)
        
        self.__copains_pjs.append(_CopainsPjs(E1,E2))
    
    def add_pj_scenar_ronde(self,E1:str,scenar:str,ronde:str):
        """Ajoute la contrainte "equipe 1 jouera le scenar "scenar" a la ronde "ronde""

        Args:
            E1 (str): _description_
            scenar (str): _description_
            ronde (str): _description_
        """
        self._checkPlayer(E1)
        self._checkScenar(scenar)
        self._checkRonde(ronde)
        
        self.__pj_scenar_ronde.append(_PjsScenarRonde(E1,ronde,scenar))

    def get_copains_pj_scenar_ronde(self):
        return self.__copains_pjs_Scenar_Ronde
    
    def get_pas_copains_pj(self):
        return self.__pas_copains_pjs
    
    def get_copains_pj(self):
        return self.__copains_pjs
    
    def get_copains_pj_mj_scenar(self):
        return self.__copains_pj_mj_scenar

    def get_copains_pjs_ronde(self):
        return self.__copains_pjs_ronde
    
    def get_pj_scenar_ronde(self):
        return self.__pj_scenar_ronde