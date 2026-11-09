# -*- coding: utf-8 -*-
"""
************************
@author : damie
created on : Thu Mar 23 23:12:38 2023
last mod : 
title : 
goals : 
to do : 
************************* """

""" ********************
    **** Imports ****
    ******************** """

import heapq
from Recuperation_donnees import recup
from Recuperation_donnees import distance
from Matrice_adjacence import creation_matrice


""" ********************
    **** Classes ****
    ******************** """



""" ********************
    **** Functions ****
    ******************** """

def voisins(matrice, sommet):
    liste_voisins=[i for i in range(len(matrice)) if matrice[sommet][i]!=0]
    return liste_voisins

##########

def dijkstra_mat(matadj, start, end):
    assert type(start) == int , "L'indice de la station de départ doit être un entier"
    assert type(end) == int , "L'indice de la station d'arrivé doit être un entier"
    n = len(matadj)
    distances = [float('inf') for i in range(n)]
    sommet_pre = [None for i in range(n)]
    visite = [False for i in range(n)]
    distances[start] = 0
    file = [start]
    voisins_end=voisins(matadj,end)

    while len(voisins_end)!=0:
        sommet_act = file[0]
        visite[sommet_act] = True
        del file[0]
        for i in range(n):
            if matadj[sommet_act][i] != 0:
                if distances[i] > distances[sommet_act] + matadj[sommet_act][i]:
                    distances[i] = distances[sommet_act] + matadj[sommet_act][i]
                    sommet_pre[i] = sommet_act
                if i not in file:
                    file.append(i)
                if sommet_act in voisins_end:
                    voisins_end.remove(sommet_act)
    
    chemin = [end]
    sommet_act = end
    
    while sommet_act != start:
        chemin.append(sommet_pre[sommet_act])
        sommet_act = sommet_pre[sommet_act]
    
    chemin.reverse()
        
    return chemin, distances[end]

##########

def mat_to_dico(matrice):
    dico = {}
    for i in range(len(matrice)):
        dico[i] = {}
        for j in range(len(matrice[i])):
            if matrice[i][j] != 0:
                dico[i][j] = matrice[i][j]
    return dico

##########

def dijkstra_dic(dico, depart, arrivee):
    assert type(depart) == int , "L'indice de la station de départ doit être un entier"
    assert type(arrivee) == int , "L'indice de la station d'arrivé doit être un entier"
    distances = {sommet : float('inf') for sommet in dico}
    distances[depart] = 0
    heap = [(0, depart)]
    sommet_pre = {}
    
    while heap:
        (distance_act, sommet_act) = heapq.heappop(heap)
        
        if sommet_act == arrivee:
            chemin = []
            
            while sommet_act in sommet_pre:
                chemin.insert(0, sommet_act)
                sommet_act = sommet_pre[sommet_act]
            
            chemin.insert(0, depart)
            return (chemin, distance_act)
        
        for voisins, distance in dico[sommet_act].items():
            distance_temp = distances[sommet_act] + distance
            
            if distance_temp < distances[voisins]:
                distances[voisins] = distance_temp
                sommet_pre[voisins] = sommet_act
                heapq.heappush(heap, (distance_temp, voisins))
                
    return None

##########

def Astar(matrice, debut, fin):
    openlist = [debut]
    closedlist = []
    parents = {}
    poids = {debut: 0}
    distances = {debut: 0}

    while len(openlist) != 0:

        cout = float("inf")
        for noeud in openlist:
            if poids[noeud] + distance(stations_infos[liste_stations_matrice[noeud]], stations_infos[liste_stations_matrice[fin]]) < cout:
                cout = poids[noeud] + distance(stations_infos[liste_stations_matrice[noeud]], stations_infos[liste_stations_matrice[fin]])
                noeud_act = noeud

        if noeud_act == fin:
            chemin = [fin]
            dernier = fin
            while dernier != debut:
                chemin.append(parents[dernier])
                dernier = parents[dernier]
            chemin.reverse()
            return chemin, distances[fin]

        closedlist.append(noeud_act)
        openlist.remove(noeud_act)

        for voi in voisins(matrice, noeud_act):
            if voi not in closedlist:
                new_poids = poids[noeud_act] + matrice[noeud_act][voi]
                if voi not in openlist or new_poids < poids[voi]:
                    parents[voi] = noeud_act
                    poids[voi] = new_poids
                    distances[voi] = distances[noeud_act] + matrice[noeud_act][voi]
                    if voi not in openlist:
                        openlist.append(voi)

    return "Impossible d'atteindre l'arrivée", "distance inconnue"

""" ********************
    **** Global Var ****
    ******************** """



""" **************
    **** Main ****
    ************** """

lien_lignes = "https://download.data.grandlyon.com/wfs/rdata?SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=tcl_sytral.tcllignemf_2_0_0&outputFormat=application/json; subtype=geojson&SRSNAME=EPSG:3946&startIndex=0&count=100"
lien_arrets = "https://download.data.grandlyon.com/wfs/rdata?SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=tcl_sytral.tclarret&outputFormat=application/json; subtype=geojson&SRSNAME=EPSG:3946&startIndex=0&count=4657"

stations_infos,lignes_infos,codes_lignes = recup(lien_lignes, lien_arrets)

matrice,liste_stations_matrice = creation_matrice(lignes_infos, stations_infos)
