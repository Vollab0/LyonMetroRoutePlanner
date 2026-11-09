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



""" ********************
    **** Classes ****
    ******************** """



""" ********************
    **** Functions ****
    ******************** """

##### Connexité #####

def parcours_profondeur(graphe, accessible, debut):
    accessible[debut] = True
    for voisins in range(len(graphe)):
        if graphe[debut][voisins] and not accessible[voisins]:
            parcours_profondeur(graphe, accessible, voisins)

def connexite(graphe):
    visite = [False] * len(graphe)
    parcours_profondeur(graphe, visite, 0)
    for sommet in visite:
        if not sommet:
            return False
    return True

##### Cycle Hamoltonien #####

def condition_Dirac(matrice): # Verifie la condition de Dirac qui dit qu'un cylce hamiltonien peut exister seuleument si deg(sommet) >= n/2
    matrice_ligne_sans_zeros = [[el for el in ligne if el != 0] for ligne in matrice]
    for i in range(len(matrice)):
        if len(matrice_ligne_sans_zeros[i]) < (len(matrice)/2): # la matrice est symetrique donc len(matrice) correspond au nombre de sommets
            return False
    return True 

##### Densité #####

def densite(graph):
    n=len(graph)
    somme_aretes=0
    for i in range(n):
        for j in range(n):
            if graph[i][j]!=0:
                somme_aretes+=1
    return somme_aretes/(n*(n-1)/2)

##### Centralité #####

def voisins(matrice,sommet):
    liste_voisins=[i for i in range(len(matrice)) if matrice[sommet][i]!=0]
    return liste_voisins

def centralite(graph):
    sommets_principaux={}
    n=len(graph)
    for i in range(n):
        if len(voisins(graph,i))>2:
            sommets_principaux[i]=len(voisins(graph,i))
    return sommets_principaux


""" ********************
    **** Global Var ****
    ******************** """



""" **************
    **** Main ****
    ************** """