#!/usr/bin/env python3
#coding:utf-8

#Version offline
from random import randint


def main():
    """
    Debut du jeu
    """
    pv=50       #PV de base
    atq=15      #Attaque de base
    soin=5      #Soin de base
    catq=10    #Contre attaque       
    coutca=5    #Cout de la contre attaque

    print("=========================================================================")

    print("\nBienvenue sur la plateforme de Combat po.py \n\
Le but du jeu est de faire descendre les points de vie (pv) de l'adversaire à 0 \n\
Vous commencez avec "+ str(pv)+" pv. \n\
Pour cela, vous disposez de 3 possibilités: \n")

    print("- Une attaque qui inflige "+str(atq)+" pv \n\
- Un soin qui restore "+str(soin)+" pv \n\
- Une contre-attaque, annule les dégats de l'adversaires et retourne "+ str(catq)+"\
 contre lui sous reserve de perdre "+str(catq)+" \
 pv si le contre-attaquant ne se fait pas attaqué \n\
\nQUE LE COMBAT COMMENCE !\n")

    #print("\nMais avant tout, quel est votre nom ?")
    
    #name1,name2 = recv2()
    name1 = input("\nMais avant tout, quel est votre nom ?\n-> ")
    
    name2 = "Le méchant"


    #Dans le cadre d'une future amélioration
    pv1=pv
    pv2=pv
    atq1=atq
    atq2=atq
    catq1=catq
    catq2=catq
    coutca1 = coutca
    coutca2 = coutca
    soin1=soin
    soin2=soin
    nb_tours = 0

    while ((pv1 > 0)and(pv2 > 0)):
        nb_tours +=1
        
        print("=========================================================================")
        print("tour n°"+str(nb_tours)+" :")
        print("\n"+name1+" = "+str(pv1)+" pv & "+name2+" = "+str(pv2)+" pv" )
        
                #"""
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
            print(name1+" se soigne !")
            gain = min(pv,pv1+soin1) - pv1 #On ne souhaite pas dépasser la limite de pv de base
            pv1 += gain
            print(name1+" a gagné "+str(gain)+" pv.\n")
        if (choix2 == "2"): #Soin du J2
            print(name2 + " se soigne !")
            gain = min(pv,pv2+soin2) - pv2 #On ne souhaite pas dépasser la limite de pv de base
            pv2 += gain
            print(name2+" a gagné "+str(gain)+" pv.\n")
        if (choix1 == "1"): #Atq du J1
            print(name1 +" attaque !")
            if (choix2 == "3"): #Catq du J2
                print("Mais "+name2+" contre-attaque !")
                pv1 -= catq2
                #pv2 -= coutca2
                print(name1+" a perdu "+str(catq2)+" pv.\n")
                #print(name2+" a perdu "+str(coutca2)+" pv.\n")
            else:
                pv2 -= atq1
                print(name2+" a perdu "+str(atq1)+" pv.\n")
        if (choix2 == "1"): #Atq du J2
            print(name2+" attaque !")
            if (choix1 == "3"): #Catq du J1
                print("Mais "+name1+" contre-attaque !")
                #print("Mais Joueur 1 contre-attaque et perds "+str(coutca1)+" pv!")
                pv2 -= catq1
                #pv1 -= coutca1
                print(name2+" a perdu "+str(catq1)+" pv.\n")
                #print(name1+" a perdu "+str(coutca1)+" pv.\n")
            else:
                pv1 -= atq2
                print(name1+" a perdu "+str(atq2)+" pv.\n")
        if ((choix1 == "3")and(choix2 != "1")):
                print(name1 +" contre-attaque !")
                print("Mais c'est inefficace.\n")
                pv1 -= coutca1
                print(name1+" a perdu "+str(coutca1)+" pv.\n")
        if ((choix2 == "3")and(choix1 != "1")):
                print(name2+" contre-attaque !")
                print("Mais c'est inefficace\n")
                pv2 -= coutca2
                print(name2+" a perdu "+str(coutca2)+" pv.\n")

    if ((pv1 <= 0)and(pv2 <= 0)):
        print("Les deux joueurs n'ont plus de pv, c'est une égalité !")
    else:
        if (pv2 <= 0):
            print(name1+" a gagné !")
        if (pv1 <= 0):
            print(name2+" a gagné !")

main()