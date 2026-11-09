# -*- coding: utf-8 -*-
"""
************************
@author : Gabin
created on : Tue Jan 10 22:18:18 2023
last mod : 2022
title : notitle
goals : brief description
to do : what should be done next time
************************* """

""" ********************
    **** Imports ****
    ******************** """
import sys


from Recuperation_donnees import recup
from Recuperation_donnees import distance
from Matrice_adjacence import creation_matrice
from Algo_PCC import dijkstra_dic
from Algo_PCC import mat_to_dico
from Verifications import connexite
from Verifications import condition_Dirac
from Verifications import densite
from Verifications import centralite
from Changements import changements


from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.animation import Animation
from kivymd.theming import ThemeManager
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.image import AsyncImage
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.boxlayout import MDBoxLayout    
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.core.window import Window

Window.size = (540, 1080)


""" ********************
    **** Classes ****
    ******************** """
# no data

""" ********************
    **** Functions ****
    ******************** """
    
def appartenance_ligne(station): # Renvoie les lignes auquelles appartient la station
    assert type(station) == str , 'Cette fonction ne prend que des chaines de caractères en arguments'
    ligne = [ligne for ligne in list(lignes_infos.keys()) if station in lignes_infos[ligne]['stations']]
    return ligne

def recherche_itineraire(depart,destination): # Renvoie le dictionnaire des changements, le chemin et la distance entre le depart et la destination 
    chemin_indices,distance = dijkstra_dic(dico_matrice, liste_stations_matrice.index(depart), liste_stations_matrice.index(destination))
    chemin = [liste_stations_matrice[el] for el in chemin_indices]
    dico_changements = changements(chemin,appartenance_ligne)
    return chemin,distance,dico_changements # dico_changement = {station : [ligne d'arrivé,ligne de départ]}


""" ********************
    **** Global Var ****
    ******************** """

lien_lignes = "https://download.data.grandlyon.com/wfs/rdata?SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=tcl_sytral.tcllignemf_2_0_0&outputFormat=application/json; subtype=geojson&SRSNAME=EPSG:3946&startIndex=0&count=100"
lien_arrets = "https://download.data.grandlyon.com/wfs/rdata?SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=tcl_sytral.tclarret&outputFormat=application/json; subtype=geojson&SRSNAME=EPSG:3946&startIndex=0&count=4657"

stations_infos,lignes_infos,codes_lignes = recup(lien_lignes, lien_arrets)

matrice,liste_stations_matrice = creation_matrice(lignes_infos, stations_infos)

dico_matrice=mat_to_dico(matrice)

Couleurs = {'A': [.863, .235, .6, 1.0],'B': [.188, .474, .761, 1.0],'C': [.925, .58, .063, 1.0],'D': [.255, .666, .286, 1.0],'F': [.572, .776, .278, 1.0]} 

distance_foch_massena = 691.19 # distance utilisée pour transformer les distances en EPSG:3946 en mètres
distance_en_EPSG = distance(stations_infos['Foch'],stations_infos['Masséna'])
facteur_distance = distance_foch_massena / distance_en_EPSG # calcul du facteur reliant les deux unitées de mesures

vitesse_metro = 21


""" **************
    **** Main ****
    ************** """

if connexite(matrice): # Verifie la connexité du graphe
    print('Le graphe est connexe')
else :
    print('Le graphe est non connexe')

if densite(matrice)<0.15:
    print('Le graphe est creux')
elif densite(matrice)>0.5:
    print("Le graphe est dense")
else:
    print("Le graphe n'est ni dense, ni creux")  

if condition_Dirac(matrice):
    print('Il existe un cycle Hamiltonien')
else:
    print("Il n'existe pas de cycle Hamiltonien")

dico_centralite={}
for i in centralite(matrice).keys():
    dico_centralite[liste_stations_matrice[i]]=centralite(matrice)[i]
print('Les sommets principaux sont:',dico_centralite)




class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class Application(MDApp):

    zone_texte_destination = ObjectProperty(None)
    zone_texte_depart = ObjectProperty(None)

    dico_changements = ObjectProperty(None)
    distance = ObjectProperty(None)
    chemin = ListProperty(['depart'])



    def build(self):

        self.theme_cls = ThemeManager()

        self.root = ScreenManager() # Gestion des differentes pages
        self.root.add_widget(Builder.load_file('page_principale.kv')) # Charge le premier ecran
        self.root.add_widget(Builder.load_file('page_resultats.kv')) # Charge le deuxième ecran
        stations_clees = list(stations_infos.keys())
        stations_triees = sorted(stations_clees)

        liste_choix_station_depart = [
            {
                "viewclass": "IconListItem",
                "icon": "Images/Metro.png",
                "text": station,
                "height": 50,
                "font_name": 'SPoppins',
                "on_release": lambda x=station: self.nom_station_depart(x),
            } for station in stations_triees
        ]
        liste_choix_station_arrivee = [
            {
                "viewclass": "IconListItem",
                "icon": "Images/Metro.png",
                "text": station,
                "height": 50,
                "font_name": 'SPoppins',
                "on_release": lambda x=station: self.nom_station_arrivee(x),
            } for station in stations_triees
        ]
        self.menu_station_depart = MDDropdownMenu(
            caller = self.root.get_screen('main').ids.choix_station_depart,
            items = liste_choix_station_depart,
            position = "center",
            hor_growth=None,
            ver_growth="down",
            width_mult = 4,
        )
        self.menu_station_arrivee = MDDropdownMenu(
            caller = self.root.get_screen('main').ids.choix_station_arrivee,
            items = liste_choix_station_arrivee,
            position = "center",
            hor_growth=None,
            ver_growth="down",
            width_mult = 4,
        )
        
        return self.root # Affiche les pages
    
    def nom_station_depart(self, nom): # Cette fonction met a jour dynamiquement le nom de la station choisie et ferme le menu
        page_principale = self.root.get_screen('main')
        page_principale.ids.choix_station_depart.text = nom
        self.item_depart = nom
        self.menu_station_depart.dismiss()

        popup = self.root.get_screen('main').ids.popup
        anim = Animation(opacity = 0, duration = 0.3)
        anim.start(popup)
    
    def nom_station_arrivee(self, nom): # Cette fonction met a jour dynamiquement le nom de la station choisie et ferme le menu
        page_principale = self.root.get_screen('main')
        page_principale.ids.choix_station_arrivee.text = nom
        self.item_arrivee = nom
        self.menu_station_arrivee.dismiss()

        popup = self.root.get_screen('main').ids.popup
        anim = Animation(opacity = 0, duration = 0.3)
        anim.start(popup)

    def inverser_stations(self):
        page_principale = self.root.get_screen('main')
        page_principale.ids.choix_station_arrivee.text,page_principale.ids.choix_station_depart.text = page_principale.ids.choix_station_depart.text,page_principale.ids.choix_station_arrivee.text
        self.item_arrivee,self.item_depart = self.item_depart,self.item_arrivee

        popup = self.root.get_screen('main').ids.popup
        anim = Animation(opacity = 0, duration = 0.3)
        anim.start(popup)



    def afficher_resultats(self):
        ligne_layout = self.root.get_screen('resultat').ids.ligne_layout
        ligne_layout.clear_widgets()

        ligne_precedente = ''

        for key, value in self.dico_changements.items():
            
            if ligne_precedente != value[0]:

                icone = AsyncImage(source='Images/IconeMetro'+ str(value[0]) + '.png')               
                icone.texture_size = (204, 112)
                icone.size_hint = (None, None)


                dico_taille_images = {1: (250.5, 'moyenne.png'), 2: (150, 'courte.png'), 3: (120, 'courte.png')} # relie le nombre de changements (clées) aux images avec leurs hauteurs correspondantes (valeurs)

                taille_image = dico_taille_images[len(self.dico_changements.keys())]
                image = AsyncImage(source=f'Images/LigneMetro{value[0][0]}{taille_image[1]}')
                image.texture_size = (92, 496)
                image.size_hint = (None, None)
                image.width = 100
                image.height = taille_image[0]
                image.pos_hint = {'center_x': .5}

                Boite_image = MDBoxLayout(orientation='vertical', size_hint_x=.3)
                Boite_image.add_widget(image)

                icone.height = 35
                icone.pos_hint = {'center_x': .6, 'center_y': .5}
                Boite_icone = MDBoxLayout(orientation='horizontal', size_hint_x=.35)
                Boite_icone.add_widget(icone)

                distance_entre_changements = distance(stations_infos[self.chemin[0]],stations_infos[key]) 
                distance_en_metres = facteur_distance * distance_entre_changements
                duree = distance_en_metres / ( vitesse_metro * 1000/60 ) # On convertie la vitesse du métro en metres / minutes
                duree = round(duree) # on arrondit la durée en minutes
                temps = MDLabel(text=str(duree) + ' min')
                temps.font_name = 'MPoppins'
                temps.font_size = '20sp'
                temps.color = Couleurs[value[0][0]]
                temps.pos_hint = {'x': 0, 'center_y': .5}

                Boite_temps = MDBoxLayout(orientation='vertical', size_hint_x=.35)
                Boite_temps.add_widget(temps)

                Boite = MDBoxLayout(orientation='horizontal', size_hint_x=.4, size_hint_y=None, height=image.height)
                Boite.add_widget(Boite_temps)
                Boite.add_widget(Boite_image)
                Boite.add_widget(Boite_icone)
                Boite.pos_hint = {'center_x': .5, 'center_y': .5}

                ligne_layout.add_widget(Boite)

            
            label = MDLabel(text=key)

            label.pos_hint = {'center_x':.5}
            label.halign = 'center'
            label.font_name = 'RPoppins'
            label.font_size = '20sp'

            icone = AsyncImage(source='Images/IconeMetro'+ str(value[1]) + '.png')               
            icone.texture_size = (204, 112)
            icone.size_hint = (None, None)
            
            dico_taille_images = {1: (250.5, 'moyenne.png'), 2: (150, 'courte.png'), 3: (120, 'courte.png')} # relie le nombre de changements (clées) aux images avec leurs hauteurs correspondantes (valeurs)

            taille_image = dico_taille_images[len(self.dico_changements.keys())]

            image = AsyncImage(source=f'Images/LigneMetro{value[1][0]}{taille_image[1]}')
            image.texture_size = (92, 496)
            image.size_hint = (None, None)

            image.width = 100
            image.height = taille_image[0]
            image.pos_hint = {'center_x':.5}

            Boite_image = MDBoxLayout(orientation='vertical', size_hint_x=.3)
            Boite_image.add_widget(image)

            icone.height = 35
            icone.pos_hint = {'center_x': .6, 'center_y': .5}  

            Boite_icone = MDBoxLayout(orientation='horizontal', size_hint_x=.35)
            Boite_icone.add_widget(icone)

            distance_entre_changements = distance(stations_infos[key],stations_infos[list(self.dico_changements.keys())[list(self.dico_changements.keys()).index(key) - 1]])
            distance_en_metres = facteur_distance * distance_entre_changements
            duree = distance_en_metres / ( vitesse_metro * 1000/60 ) # On convertie la vitesse du métro en metres / minutes
            duree = round(duree) # on arrondit la durée en minutes
            temps = MDLabel(text=str(duree) + ' min')
            temps.font_name = "MPoppins"
            temps.font_size = '20sp'
            temps.color = Couleurs[value[1][0]]
            temps.pos_hint = {'x': 0, 'center_y': .5}

            Boite_temps = MDBoxLayout(orientation='vertical', size_hint_x=.35)
            Boite_temps.add_widget(temps)

            Boite = MDBoxLayout(orientation='horizontal', size_hint_x=.4, size_hint_y=None, height=image.height)
            Boite.add_widget(Boite_temps)
            Boite.add_widget(Boite_image)
            Boite.add_widget(Boite_icone)

            Boite.pos_hint = {'center_x': .5, 'center_y': .5}



            ligne_layout.add_widget(label)
            ligne_layout.add_widget(Boite)

            ligne_precedente = value[1] 


        if len(self.dico_changements.keys()) == 0 : # Si il n'y a pas de changement, on affiche une seule ligne 

            lignes_passant_par_la_station_de_depart = appartenance_ligne(self.chemin[0])  
            lignes_passant_par_la_station_d_arrive = appartenance_ligne(self.chemin[-1]) 

            for el in lignes_passant_par_la_station_de_depart:
                if el in lignes_passant_par_la_station_d_arrive:
                    ligne_en_commun = el

            image = AsyncImage(source='Images/LigneMetro'+ str(ligne_en_commun) + 'longue.png')
            image.texture_size = (100, 100)
            image.size_hint_y = 1
            image.pos_hint = {'center_x':.5, 'center_y': .5}

            Boite_image = MDBoxLayout(orientation= 'vertical', size_hint = (.3,1))
            Boite_image.add_widget(image)

            icone = AsyncImage(source='Images/IconeMetro'+ str(ligne_en_commun) + '.png')      
            icone.texture_size = (204, 112)
            icone.size_hint = (None, None)
            icone.height = 35
            icone.pos_hint = {'center_x': .6,'center_y': .5} 

            Boite_icone = MDBoxLayout(orientation= 'horizontal', size_hint= (.35,1))
            Boite_icone.add_widget(icone)

            distance_entre_changements = distance(stations_infos[self.chemin[0]],stations_infos[self.chemin[-1]])
            distance_en_metres = facteur_distance * distance_entre_changements
            duree = distance_en_metres / ( vitesse_metro * 1000/60 ) # On convertie la vitesse du métro en metres / minutes
            duree = round(duree) # on arrondit la durée en minutes
            temps = MDLabel(text=str(duree) + ' min')
            temps.font_name = "MPoppins"
            temps.font_size = '20sp'
            temps.color = Couleurs[ligne_en_commun[0]]
            temps.pos_hint = {'x': 0,'center_y': .5}

            Boite_temps = MDBoxLayout(orientation= 'vertical', size_hint= (.35,1))
            Boite_temps.add_widget(temps)

            Boite = MDBoxLayout(orientation='horizontal',size_hint_x= .4,size_hint_y= 1)
            Boite.add_widget(Boite_temps)
            Boite.add_widget(Boite_image)
            Boite.add_widget(Boite_icone)

            Boite.pos_hint = {'center_x':.5, 'center_y': .5}

            ligne_layout.add_widget(Boite)




    def rechercher(self): # Renvoie le resultat de la recherche
        
        try: # essaie d'executer le code suivant 
            depart = self.item_depart
            destination = self.item_arrivee

        except AttributeError: # code qui s'execute si l'erreur AttributeError est detectée, càd si les stations n'ont pas été selectionnée
            popup = self.root.get_screen('main').ids.popup
            popup_text = self.root.get_screen('main').ids.popup_text
            popup_text.text = 'Veuillez selectionner les stations demandées'

            anim = Animation(opacity = 1, duration = 0.3)
            anim.start(popup)

        else: # code qui s'execute si il n'y a pas d'erreur
            
            if depart == destination:
                popup = self.root.get_screen('main').ids.popup
                popup_text = self.root.get_screen('main').ids.popup_text
                popup_text.text = 'Merci de choisir deux stations différentes'

                anim = Animation(opacity = 1, duration = 0.3)
                anim.start(popup)
                
                
            else:
                self.chemin,self.distance,self.dico_changements = recherche_itineraire(depart,destination)

                
                self.distance = (self.distance * facteur_distance) / 1000 # on met en km
                self.distance = round(self.distance,1)
                

                self.root.transition.direction = 'left'
                self.root.current = 'resultat'

                self.afficher_resultats()
        
        
    def quitter(self):
        sys.exit()

if __name__ == "__main__":
    LabelBase.register("RPoppins", "Poppins/Poppins-Regular.ttf") # initialise la police de caractère
    LabelBase.register("MPoppins", "Poppins/Poppins-Medium.ttf") 
    LabelBase.register("BPoppins", "Poppins/Poppins-SemiBold.ttf")
    Application().run()                                           # lance l'application à l'execution du script python





