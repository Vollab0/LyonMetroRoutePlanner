# -*- coding: utf-8 -*-
"""
************************
@author : Gabin
created on : Sun Jan 22 20:29:06 2023
last mod : 2022
title : notitle
goals : brief description
to do : what should be done next time
************************* """

""" ********************
    **** Imports ****
    ******************** """

""" ********************
    **** Classes ****
    ******************** """
# no data

""" ********************
    **** Functions ****
    ******************** """

def changements(chemin,fct_appartenance_ligne):
    liste_lignes = [fct_appartenance_ligne(el) for el in chemin]
    changements = {}
        
    if len(liste_lignes[0]) == 1: # si la première station n'appartient qu'a une ligne, on la définit comme la ligne actuelle
        ligne_actuelle = liste_lignes[0][0]
    else : # sinon, la ligne actuelle est la ligne en commun entre les deux premières stations
        ligne_actuelle = [ligne for ligne in liste_lignes[0] if ligne in liste_lignes[1]][0]
    for el in liste_lignes:
        if ligne_actuelle not in el :
            if len(el) == 1:
                prochaine_ligne = el[0]
            else :
                if liste_lignes.index(el) == len(liste_lignes)-1:
                    prochaine_ligne = None                         
                else:                                             
                    prochaine_ligne = liste_lignes[liste_lignes.index(el)+1][0]

            changements[chemin[liste_lignes.index(el)-1]] = ligne_actuelle,prochaine_ligne
            ligne_actuelle = prochaine_ligne
    
    return changements  # clée = station, valeurs = (ligne_arrivé,ligne_depart)
    

""" ********************
    **** Global Var ****
    ******************** """
# no data

""" **************
    **** Main ****
    ************** """
# no data



