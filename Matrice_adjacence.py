# -*- coding: utf-8 -*-
"""
************************
@author : Gabin
created on : Tue Jan 10 20:47:32 2023
last mod : 2022
title : notitle
goals : brief description
to do : what should be done next time
************************* """

""" ********************
    **** Imports ****
    ******************** """
    
import numpy as np
from Recuperation_donnees import distance

""" ********************
    **** Classes ****
    ******************** """
# no data

""" ********************
    **** Functions ****
    ******************** """
    
def creation_matrice(lignes_infos,stations_infos): # Crée la matrice d'adjacence a partir de la liste des dico de stations et de la liste des dico de lignes
    
    matrice = np.zeros((len(stations_infos),len(stations_infos)))
    liste_stations = [el['properties']['nom'] for el in stations_infos.values()]
    liste_stations.sort()
    
    for i in range(len(liste_stations)):
        for j in range(len(liste_stations)):
            if voisins(liste_stations[i],liste_stations[j],lignes_infos) :
                matrice[i][j] = distance(stations_infos[liste_stations[i]],stations_infos[liste_stations[j]])
    

    return matrice,liste_stations




def voisins(station1,station2,lignes_infos): # Renvoie True si les stations sont voisines
    assert type(station1) == str and type(station2) == str, 'Cette fonction ne prend que des chaines de caractères en arguments'
    flag = False
    for ligne in list(lignes_infos.values()): 
        
        if (station1 in ligne['stations']) and (station2 in ligne['stations']):
            
            if ligne['stations'].index(station1) < len(ligne['stations'])-1 : # Si la station n'est pas la dernière de la liste...
                if ligne['stations'][ligne['stations'].index(station1) + 1] == station2 : # ...on compare avec la station suivante 
                    flag = True
                    
            if ligne['stations'].index(station1) > 0 : # Si la station n'est pas la première de la liste...
                if ligne['stations'][ligne['stations'].index(station1) - 1] == station2 : # ...on compare avec la station precedente 
                    flag = True
                    
    return flag    


""" ********************
    **** Global Var ****
    ******************** """
# no data

""" **************
    **** Main ****
    ************** """
# no data



