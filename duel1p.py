#!/usr/bin/env python3
#coding:utf-8

#Version offline
from tkinter import *
from random import randint
from time import sleep

class Joueur:
  """
  Classe définissant les caracteristiques d'un joueur :
  """
  def __init__(j, name = ""):
    """Constructeur de notre classe"""
    j.name = name
    j.pv=50         #PV de base
    j.atq=15        #Attaque de base
    j.soin=5        #Soin de base
    j.catq=10       #Contre attaque       
    j.coutca=5      #Cout de la contre attaque
    j.choix = int() #Choix du type d'attaque

def combat(j1,j2):
    """Résolution du combat"""
                  
    bquit = ("bouton","Quitter",exit)
    bnext = ("bouton","Ok",next)

    #Les soins sont executées avant les attaques
    if (j1.choix == "2"): #Soin du J1
        add_dial(j1.name+" se soigne !",bnext)
        gain = min(Joueur().pv,j1.pv+j1.soin) - j1.pv #On ne souhaite pas dépasser la limite de pv de base
        j1.pv += gain
        add_dial(j1.name+" a gagné "+str(gain)+" pv.\n",bnext)
    if (j2.choix == "2"): #Soin du J2
        add_dial(j2.name + " se soigne !",bnext)
        gain = min(Joueur().pv,j2.pv+j2.soin) - j2.pv #On ne souhaite pas dépasser la limite de pv de base
        j2.pv += gain
        add_dial(j2.name+" a gagné "+str(gain)+" pv.\n",bnext)
    if (j1.choix == "1"): #Atq du J1
        add_dial(j1.name +" attaque !",bnext)
        if (j2.choix == "3"): #Catq du J2
            add_dial("Mais "+j2.name+" contre-attaque !",bnext)
            j1.pv -= j2.catq
            #j2.pv -= j2.coutca
            add_dial(j1.name+" a perdu "+str(j2.atq)+" pv.\n",bnext)
            #add_dial(j2.name+" a perdu "+str(j2.coutca)+" pv.\n")
        else:
            j2.pv -= j1.atq
            add_dial(j2.name+" a perdu "+str(j1.atq)+" pv.\n",bnext)
    if (j2.choix == "1"): #Atq du J2
        add_dial(j2.name+" attaque !",bnext)
        if (j1.choix == "3"): #Catq du J1
            add_dial("Mais "+j1.name+" contre-attaque !",bnext)
            #add_dial("Mais Joueur 1 contre-attaque et perds "+str(j1.coutca)+" pv!")
            j2.pv -= j1.catq
            #j1.pv -= j1.coutca
            add_dial(j2.name+" a perdu "+str(j1.catq)+" pv.\n",bnext)
            #add_dial(j1.name+" a perdu "+str(j1.coutca)+" pv.\n")
        else:
            j1.pv -= j2.atq
            add_dial(j1.name+" a perdu "+str(j2.atq)+" pv.\n",bnext)
    if ((j1.choix == "3")and(j2.choix != "1")):
            add_dial(j1.name +" contre-attaque !",bnext)
            add_dial("Mais c'est inefficace.\n",bnext)
            j1.pv -= j1.coutca
            add_dial(j1.name+" a perdu "+str(j1.coutca)+" pv.\n",bnext)
    if ((j2.choix == "3")and(j1.choix != "1")):
            add_dial(j2.name+" contre-attaque !",bnext)
            add_dial("Mais c'est inefficace\n",bnext)
            j2.pv -= j2.coutca
            add_dial(j2.name+" a perdu "+str(j2.coutca)+" pv.\n",bnext)

    #Si l'un des joueurs est mort
    if ((j1.pv <= 0)and(j2.pv <= 0)):
        add_dial("Les deux joueurs n'ont plus de pv, c'est une égalité !",bquit)
    else:
        if (j2.pv <= 0):
            add_dial(j1.name+" a gagné !",bquit)
        if (j1.pv <= 0):
            add_dial(j2.name+" a gagné !",bquit)
    #Sinon
    choix(j1,j2)

def choix(j1,j2):
    """Permet au joueur de choisir quel action faire"""
    #Le choix du j1 est choisi alors que celui de j2 est aléatoire
    #ADD DIAL NOT DEFINED
    def choix1():
        j1.choix=1

    def choix2():
        j1.choix=2

    def choix3():
        j1.choix=3

    bouton1 = ("bouton","Attaquer",choix1)
    bouton2 = ("bouton","Attaquer",choix2)
    bouton3 = ("bouton","Attaquer",choix3)
    
    add_dial("Que faites-vous ?",bouton1,bouton2,bouton3)

    j2.choix=1 ###RENDRE ALEATOIRE

    combat(j1,j2) #Permet de résoudre le tour

def main(interface):
    """
    Debut du jeu
    """
    interface.refresh()


#################################################"
    #On crée une frame de lecture de donnée et une frame d'interaction
    #Un peu comme une Nintendo DS
    interface.read = Frame(interface.content)
    interface.read.pack()

    interface.write = Frame(interface.content)
    interface.write.pack(side="bottom")

    #interface.reading = False
    interface.dialogs = list()    #Tableau des dialogues
    interface.interactions = list()    #Tableau des dialogues
    interface.dialog_number= 0  #init

    #On crée ensuite des méthodes pour utiliser ca simplement
    def exit():
        interface.read.destroy()
        interface.write.destroy()
        interface.menu()

    def upload():
        '''Mets a jour l'affichage de interface.read'''
        interface.read.destroy()
        interface.read = Frame(interface.content)
        interface.read.pack(side = "top")

        interface.txt = Label(interface.read,text=interface.dialogs[interface.dialog_number])
        interface.txt.pack()

        interface.write.destroy()
        interface.write = Frame(interface.content)
        interface.write.pack(side="bottom")

        interface.tabButton = list() 
        for interaction in interface.interactions[interface.dialog_number]:
            typeInteraction,message,fonction = interaction
            if typeInteraction == "bouton":
                interface.tabButton.append(Button(interface.write,text=message,command=fonction).pack())

    def add_dial(msg,*kwargs):
        '''Affiche un message dans la frame de lecture'''
        interface.dialogs.append(msg)

        interface.interactions.append(kwargs) #append tuple of tuple


    def next():
        '''Permet de passer au add_dial suivant'''
        if interface.dialog_number < len(interface.dialogs)-1:
            interface.dialog_number += 1
            upload()

    bquit = ("bouton","Quitter",exit)
    bnext = ("bouton","Ok",next)

    add_dial("hello",bquit,bnext)
    #add_dial("yo",bquit,bnext)
    #add_dial("Fin",bquit)

    upload() #Voir pour mettre upload dans add_dial

    #exit()



###############################################"
    
    nb_tours = 0
    add_dial("\nBienvenue sur la plateforme de Combat po.py \n\
Le but du jeu est de faire descendre les points de vie (pv) de l'adversaire à 0 \n\
Vous commencez avec "+ str(Joueur().pv)+" pv. \n",bnext)



    add_dial("Pour cela, vous aurez 3 possibilités d'actions :\n\
- Une attaque qui inflige "+str(Joueur().atq)+" pv \n\
- Un soin qui restore "+str(Joueur().soin)+" pv \n\
- Une contre-attaque, annule les dégats de l'adversaires et retourne "+ str(Joueur().catq)+"\
 contre lui sous reserve de perdre "+str(Joueur().catq)+" \
 pv si le contre-attaquant ne se fait pas attaqué \n",bnext)

    add_dial("QUE LE COMBAT COMMENCE !\n",bnext)

    
    #j1.name,j2.name = recv2()

    #Dans le cadre d'une future amélioration
    #j1 = Joueur(input("\nMais avant tout, quel est votre nom ?\n-> "))
    j1 = Joueur("Vous")
    
    j2 = Joueur("Le méchant")

    #start = len(interface.dialogs)-1  #Début du combat
 
    choix(j1,j2)
    
    '''
    ###############LE SYSTEME DE BOUCLE BLOQUE TKINTER !
    while ((j1.pv > 0)and(j2.pv > 0)):
        nb_tours +=1
        
        msg = "tour n°"+str(nb_tours)+" :\n"
        msg += "\n"+j1.name+" = "+str(j1.pv)+" pv & "+j2.name+" = "+str(j2.pv)+" pv\n" 
        
        #TOUR DES DEUX JOUEURS
        msg += "C'est à votre tour\n\n"
        msg += "Que voulez-vous faire ?\n"
        msg += "1 : Attaque\n"
        msg += "2 : Soin\n"
        msg += "3 : Contre-attaque\n"

        add_dial(msg,bquit)
                
        #Réception des choix
        #choix1, choix2 = recv2()
        choix1 = input("Quel est votre choix ?\n")
        choix2 = str(randint(1,3))
        add_dial(choix2)

        #MISE EN CONFRONTATION DES CHOIX
        #Les soins sont executées avant les attaques
        if (choix1 == "2"): #Soin du J1
            add_dial(j1.name+" se soigne !")
            gain = min(Joueur().pv,j1.pv+j1.soin) - j1.pv #On ne souhaite pas dépasser la limite de pv de base
            j1.pv += gain
            add_dial(j1.name+" a gagné "+str(gain)+" pv.\n")
        if (choix2 == "2"): #Soin du J2
            add_dial(j2.name + " se soigne !")
            gain = min(Joueur().pv,j2.pv+j2.soin) - j2.pv #On ne souhaite pas dépasser la limite de pv de base
            j2.pv += gain
            add_dial(j2.name+" a gagné "+str(gain)+" pv.\n")
        if (choix1 == "1"): #Atq du J1
            add_dial(j1.name +" attaque !")
            if (choix2 == "3"): #Catq du J2
                add_dial("Mais "+j2.name+" contre-attaque !")
                j1.pv -= j2.catq
                #j2.pv -= j2.coutca
                add_dial(j1.name+" a perdu "+str(j2.atq)+" pv.\n")
                #add_dial(j2.name+" a perdu "+str(j2.coutca)+" pv.\n")
            else:
                j2.pv -= j1.atq
                add_dial(j2.name+" a perdu "+str(j1.atq)+" pv.\n")
        if (choix2 == "1"): #Atq du J2
            add_dial(j2.name+" attaque !")
            if (choix1 == "3"): #Catq du J1
                add_dial("Mais "+j1.name+" contre-attaque !")
                #add_dial("Mais Joueur 1 contre-attaque et perds "+str(j1.coutca)+" pv!")
                j2.pv -= j1.catq
                #j1.pv -= j1.coutca
                add_dial(j2.name+" a perdu "+str(j1.catq)+" pv.\n")
                #add_dial(j1.name+" a perdu "+str(j1.coutca)+" pv.\n")
            else:
                j1.pv -= j2.atq
                add_dial(j1.name+" a perdu "+str(j2.atq)+" pv.\n")
        if ((choix1 == "3")and(choix2 != "1")):
                add_dial(j1.name +" contre-attaque !")
                add_dial("Mais c'est inefficace.\n")
                j1.pv -= j1.coutca
                add_dial(j1.name+" a perdu "+str(j1.coutca)+" pv.\n")
        if ((choix2 == "3")and(choix1 != "1")):
                add_dial(j2.name+" contre-attaque !")
                add_dial("Mais c'est inefficace\n")
                j2.pv -= j2.coutca
                add_dial(j2.name+" a perdu "+str(j2.coutca)+" pv.\n")

    if ((j1.pv <= 0)and(j2.pv <= 0)):
        add_dial("Les deux joueurs n'ont plus de pv, c'est une égalité !")
    else:
        if (j2.pv <= 0):
            add_dial(j1.name+" a gagné !")
        if (j1.pv <= 0):
            add_dial(j2.name+" a gagné !")
    '''

    add_dial("END",bquit)
            
