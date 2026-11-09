# -*- coding: utf-8 -*-
"""
************************
@author : Gabin
created on : Tue Jan 3 16:02:26 2023
last mod : 2022
title : notitle
goals : brief description
to do : what should be done next time
************************* """

""" ********************
    **** Imports ****
    ******************** """
import requests
import numpy as np

""" ********************
    **** Classes ****
    ******************** """
# no data

""" ********************
    **** Functions ****
    ******************** """
    
def recup(lien_lignes,lien_arrets):
    
    liste_lignes_provisoire = requests.get(lien_lignes).json()["features"]
    liste_stations_provisoire = requests.get(lien_arrets).json()["features"]
    
    
    stations_infos = {} # dictionnaire des stations
    lignes_infos ={} # dictionnaire des lignes
    
    
    codes_lignes = {} # dictionnaire qui relie les lettres des lignes à leurs code de ligne
    
    liste_provisoire = [] # liste qui stocke provisoirement les stations
    

    
    for el in liste_lignes_provisoire : # Crée un dictionnaire qui relie le code de ligne à la lettre de la ligne
        codes_lignes[el['properties']['ligne']] = el['properties']['code_ligne'][:3]
    
    
    for el in liste_stations_provisoire : # l'objectif est ici de recuperer seuleument les arrets de metro et de funiculaires et de ne pas garder ceux de bus
        desserte = el['properties']['desserte']
        
        if len(desserte) > 6 :
            desserte_split = desserte.split(',')
            for i in desserte_split:
                if i[:3] in codes_lignes.values() :
                    liste_provisoire.append(el)
                                            
        if desserte[:3] in codes_lignes.values() :
            liste_provisoire.append(el)
            
    
    
    for d in liste_provisoire:# Crée le dictionnaire stations_infos a partir de la liste provisoire
        if d['properties']['nom'] in stations_infos:
            if d['properties']['desserte'] not in stations_infos[d['properties']['nom']]['properties']['desserte']:
                stations_infos[d['properties']['nom']]['properties']['desserte'] += "," + d['properties']['desserte']
        else:
            stations_infos[d['properties']['nom']] = d
            
    
    for el in liste_lignes_provisoire: # Crée le dictionnaire lignes_infos a partir de la liste provisoire
        lignes_infos[el['properties']['ligne']] = el
        lignes_infos[el['properties']['ligne']]['stations'] = [d for d in stations_infos.values() if codes_lignes[el['properties']['ligne']] in d['properties']['desserte']]
   
    
    for ligne in lignes_infos.values() : # Met la station d'origine au debut de la liste station
        stations_ordonnées = [première_station for première_station in ligne['stations'] if première_station['properties']['nom'][:5] == ligne['properties']['nom_origine'][:5]] + [autre_station for autre_station in ligne['stations'] if autre_station['properties']['nom'][:5] != ligne['properties']['nom_origine'][:5]]
        ligne['stations'] = stations_ordonnées
        
    
    for ligne in lignes_infos.values() : # Ordonne les stations dans le bon ordre
    
        for i in range(len(ligne['stations'])-1) :
            
            station_de_reference = ligne['stations'][i]
            
            # Crée un dictionnaire qui indique les distance avec les autres stations :
            distance_avec = {station_comparée['properties']['nom']: distance(station_de_reference, station_comparée) for station_comparée in ligne['stations'][ligne['stations'].index(station_de_reference)+1:]}
            
            # Recupère la clef de la valeur la plus petite car la comparaison se fait sur les valeurs (key = distance_avec.get)
            station_plus_proche = min(distance_avec, key = distance_avec.get)
            
            index_station_plus_proche = ligne['stations'].index(stations_infos[station_plus_proche])
            
            # La station la plus proche est mise a la suite de la station de reference :
            ligne['stations'][index_station_plus_proche], ligne['stations'][i+1] = ligne['stations'][i+1],ligne['stations'][index_station_plus_proche]
         
            
    #=========== Reparation de l'erreur inconnue qui ne met pas la station Cuire au bon endroit ============
    Cuire = lignes_infos['C']['stations'].pop(2)
    lignes_infos['C']['stations'].append(Cuire)
    #====================================================================================
     
    for ligne in lignes_infos.values() : # Change les dictionnaires des stations par seulement leurs noms dans lignes_infos['X']['stations'] 
        stations_noms = []
        for station in ligne['stations']:
            stations_noms.append(station['properties']['nom'])
        ligne['stations'] = stations_noms
       
        
    return (stations_infos,lignes_infos,codes_lignes)



def distance(station1,station2): # Calcul la distance entre deux stations
    x1,y1 = station1['geometry']['coordinates'][0],station1['geometry']['coordinates'][1]
    x2,y2 = station2['geometry']['coordinates'][0],station1['geometry']['coordinates'][1]
    distance = np.sqrt( (x2-x1)**2 + (y2-y1)**2 )
    return distance

""" ********************
    **** Global Var ****
    ******************** """
# no data

""" **************
    **** Main ****
    ************** """
# no data








    
    




