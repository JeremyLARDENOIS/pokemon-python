#!/usr/bin/env python3
#coding:utf-8

#Version offline
from tkinter import *
from random import randint
from time import sleep

def main(self):
    """
    Debut du jeu
    """
    self.refresh()

    class Joueur:
      """
      Classe définissant les caracteristiques d'un joueur :
      """
      def __init__(slf, name = ""):
        """Constructeur de notre classe"""
        self.name = name
        self.pv=50       #PV de base
        self.atq=15      #Attaque de base
        self.soin=5      #Soin de base
        self.catq=10     #Contre attaque       
        self.coutca=5    #Cout de la contre attaque


#################################################"
    #On crée une frame de lecture de donnée et une frame d'interaction
    #Un peu comme une Nintendo DS
    self.read = Frame(self.content)
    self.read.pack()

    self.write = Frame(self.content)
    self.write.pack(side="bottom")

    #self.reading = False
    self.dialogs = list()    #Tableau des dialogues
    self.buttons = list()    #Tableau des dialogues
    self.dialog_number= -1  #init

    #On crée ensuite des méthodes pour utiliser ca simplement
    def exit():
        self.read.destroy()
        self.write.destroy()
        self.menu()

    def upload():
        '''Mets a jour l'affichage de self.read'''
        self.read.destroy()
        self.read = Frame(self.content)
        self.read.pack(side = "top")

        self.txt = Label(self.read,text=self.dialogs[self.dialog_number])
        self.txt.pack()

        self.write.destroy()
        self.write = Frame(self.content)
        self.write.pack(side="bottom")

        #self.tabButton = list() 
        #for cle,valeur in kwargs.items():
        #    self.tabButton.append(Button(self.write,text=cle,command=valeur).pack())

        self.tabButton = list() 
        for cle,valeur in self.buttons[self.dialog_number].items():
            self.tabButton.append(Button(self.write,text=cle,command=valeur).pack())

    def add_dial(msg, kwargs = 0):
        '''Affiche un message dans la frame de lecture'''
        #printf (str(self.reading)+"\n")

        '''
        if self.reading:
            self.io = IntVar()
            self.fenetre.wait_variable(self.io)
        '''
        self.dialogs.append(msg)

        if kwargs == 1:
            #On remets le meme bouton
            self.buttons.append(self.buttons[len(self.buttons)-1]) 
        else :
            self.buttons.append(kwargs)


    def next():
        '''Permet de passer au print suivant'''
        if self.dialog_number < len(self.dialogs)-1:
            self.dialog_number += 1
            upload()


    def button(kwargs):
        '''
        Affiche des boutons
        Prends en argument un dictionnaire clé = texte et valeur = commande
        '''
        self.write.destroy()
        self.write = Frame(self.content)
        self.write.pack(side="bottom")

        self.tabButton = list() 
        for cle,valeur in kwargs.items():
            self.tabButton.append(Button(self.write,text=cle,command=valeur).pack())
            
            
    add_dial("hello",{"Quitter":exit,"Next":next})
    upload() #Voir pour mettre upload dans add_dial
    add_dial("yo",1)
    add_dial("hello world",{"Quitter":exit})


    #exit()



###############################################"
    """
    nb_tours = 0
    print("\nBienvenue sur la plateforme de Combat po.py \n\
Le but du jeu est de faire descendre les points de vie (pv) de l'adversaire à 0 \n\
Vous commencez avec "+ str(Joueur().pv)+" pv. \n\
Pour cela, vous disposez de 3 possibilités: \n")

    print("- Une attaque qui inflige "+str(Joueur().atq)+" pv \n\
- Un soin qui restore "+str(Joueur().soin)+" pv \n\
- Une contre-attaque, annule les dégats de l'adversaires et retourne "+ str(Joueur().catq)+"\
 contre lui sous reserve de perdre "+str(Joueur().catq)+" \
 pv si le contre-attaquant ne se fait pas attaqué \n\
\nQUE LE COMBAT COMMENCE !\n")

    #j1.name,j2.name = recv2()

    #Dans le cadre d'une future amélioration
    j1 = Joueur(input("\nMais avant tout, quel est votre nom ?\n-> "))
    
    j2 = Joueur("Le méchant")
 
    while ((j1.pv > 0)and(j2.pv > 0)):
        nb_tours +=1
        
        print("=========================================================================")
        print("tour n°"+str(nb_tours)+" :")
        print("\n"+j1.name+" = "+str(j1.pv)+" pv & "+j2.name+" = "+str(j2.pv)+" pv" )
        
        #TOUR DES DEUX JOUEURS
        print("C'est à votre tour\n")
        print("Que voulez-vous faire ?")
        print("1 : Attaque")
        print("2 : Soin")
        print("3 : Contre-attaque")

        #Réception des choix
        #choix1, choix2 = recv2()
        choix1 = input("Quel est votre choix ?\n")
        choix2 = str(randint(1,3))
        print(choix2)

        #MISE EN CONFRONTATION DES CHOIX
        #Les soins sont executées avant les attaques
        if (choix1 == "2"): #Soin du J1
            print(j1.name+" se soigne !")
            gain = min(Joueur().pv,j1.pv+j1.soin) - j1.pv #On ne souhaite pas dépasser la limite de pv de base
            j1.pv += gain
            print(j1.name+" a gagné "+str(gain)+" pv.\n")
        if (choix2 == "2"): #Soin du J2
            print(j2.name + " se soigne !")
            gain = min(Joueur().pv,j2.pv+j2.soin) - j2.pv #On ne souhaite pas dépasser la limite de pv de base
            j2.pv += gain
            print(j2.name+" a gagné "+str(gain)+" pv.\n")
        if (choix1 == "1"): #Atq du J1
            print(j1.name +" attaque !")
            if (choix2 == "3"): #Catq du J2
                print("Mais "+j2.name+" contre-attaque !")
                j1.pv -= j2.catq
                #j2.pv -= j2.coutca
                print(j1.name+" a perdu "+str(j2.atq)+" pv.\n")
                #print(j2.name+" a perdu "+str(j2.coutca)+" pv.\n")
            else:
                j2.pv -= j1.atq
                print(j2.name+" a perdu "+str(j1.atq)+" pv.\n")
        if (choix2 == "1"): #Atq du J2
            print(j2.name+" attaque !")
            if (choix1 == "3"): #Catq du J1
                print("Mais "+j1.name+" contre-attaque !")
                #print("Mais Joueur 1 contre-attaque et perds "+str(j1.coutca)+" pv!")
                j2.pv -= j1.catq
                #j1.pv -= j1.coutca
                print(j2.name+" a perdu "+str(j1.catq)+" pv.\n")
                #print(j1.name+" a perdu "+str(j1.coutca)+" pv.\n")
            else:
                j1.pv -= j2.atq
                print(j1.name+" a perdu "+str(j2.atq)+" pv.\n")
        if ((choix1 == "3")and(choix2 != "1")):
                print(j1.name +" contre-attaque !")
                print("Mais c'est inefficace.\n")
                j1.pv -= j1.coutca
                print(j1.name+" a perdu "+str(j1.coutca)+" pv.\n")
        if ((choix2 == "3")and(choix1 != "1")):
                print(j2.name+" contre-attaque !")
                print("Mais c'est inefficace\n")
                j2.pv -= j2.coutca
                print(j2.name+" a perdu "+str(j2.coutca)+" pv.\n")

    if ((j1.pv <= 0)and(j2.pv <= 0)):
        print("Les deux joueurs n'ont plus de pv, c'est une égalité !")
    else:
        if (j2.pv <= 0):
            print(j1.name+" a gagné !")
        if (j1.pv <= 0):
            print(j2.name+" a gagné !")
    """
