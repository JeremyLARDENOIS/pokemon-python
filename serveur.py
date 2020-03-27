#!/usr/bin/env python3
#coding:utf-8

host = ""
port = 3334

import socket, threading, time
""" PAS BESOIN
class ThreadServer(threading.Thread):
    def __init__(self, conn, id_player):
        threading.Thread.__init__(self)
        self.conn = conn
        #self.id_player = id_player + 1
    def run(self):
        #
        #id_player = 0
        #

        msg = str(id_player)
        data = msg.encode("utf-8")
        print("ok")
        conn.send(data)
        data = conn.recv(255)
        msg = data.decode("utf_8")

        if (msg == "OK"):
            print (id_player,"joueur(s) connecté(s)")
            print(addr)
        else:
            id_player -= 1
            print("echec de la connection")
"""
##############################################################

def send_msg (conn,msg):
    """ Envoie un message a la connexion choisie
    Prends deux arguments, en premier la connexion et en deuxieme le message
    """
    msg = str(msg)
    data = msg.encode("utf-8")
    conn.sendall(data)
    print("->", msg)

def recv_msg (conn):
    """ Recois un message a la connexion choisie
    Prends en argument la connexion et renvoie le message de type string
    """
    data = conn.recv(255)
    msg  = data.decode("utf-8")
    print("<-", msg)
    return msg

def game(conn1,conn2):
    """
    Debut du jeu
    """
    def send (conn,msg):
        """
        Permet d'envoyer correctement un message en tcp
        """
        send_msg(conn,"READ");      #On envoie READ
        status = recv_msg(conn)        #On reçois OK
        if (status == "OK"):
            send_msg(conn,msg);     #On envoie le message
            status = recv_msg(conn)    #On recois OK
            while (status != "OK"):    #Tant que le message recu n'es pas ok
                send_msg(conn,msg); #On renvoie le message
                status = recv_msg(conn) 
        else: #Si le Client n'a pas recu READ, on recommence
            send(conn,msg)

    def recv (conn):
        """
        Permet de recevoir correctement un message en tcp et le retourne en sortie
        """
        send_msg(conn,"WRITE")   #On envoie WRITE
        msg = recv_msg(conn)     #On reçois le message
        if (msg == ""): #Si on a rien reçu on recommence
            msg = recv(conn)
        else: #Si on a reçu le message, on envoie OK
            send_msg(conn,"OK") 
            recv_msg(conn) #Le client nous renvoie OK
        return msg

    def broadcast(msg):
        """
        Envoie un message aux deux utilisateurs
        """
        send(conn1,msg)
        send(conn2,msg)

    #############DEBUT DU JEU##########################
    pv=30       #PV de base
    atq=10      #Attaque de base
    catq=atq    #Contre attaque       
    soin=5      #Soin de base
    tour=1      #Premier joueur à jouer

    broadcast("\nBienvenue sur la plateforme de Combat po.py")
    broadcast("Le but du jeu est de faire descendre les points de vie (pv) de l'adversaire à 0")
    broadcast("Pour cela, vous disposez de 3 possibilités:")
    broadcast("- Une attaque à "+str(atq)+" pv")
    broadcast("- Un soin à 5 pv")
    broadcast("- Une contre-attaque, qui annule les dégats de l'adversaires et les retournes contre lui")
    broadcast("\nQUE LE COMBAT COMMENCE !")
    
    #Dans le cadre d'une future amélioration
    pv1=pv
    pv2=pv
    atq1=atq
    atq2=atq
    catq1=catq
    catq2=catq
    soin1=soin
    soin2=soin

    while ((pv1 > 0)and(pv2 > 0)):
        broadcast("\nJoueur 1 = "+str(pv1)+" pv & Joueur 2 = "+str(pv2)+" pv" )

        #TOUR DU JOUEUR 1
        broadcast("C'est au tour du joueur 1\n")
        send(conn2,"En attente du joueur 1...\n")
        
        send(conn1,"Que voulez-vous faire ?")
        send(conn1,"1 : Attaque")
        send(conn1,"2 : Soin")
        send(conn1,"3 : Contre-attaque")
        choix1 = recv(conn1) #Réception du choix du joueur 1

        #TOUR DU JOUEUR 2
        broadcast("C'est au tour du joueur 2 :")
        send(conn1,"En attente du joueur 2...")
    
        send(conn2,"Que voulez-vous faire ?")
        send(conn2,"1 : Attaque")
        send(conn2,"2 : Soin")
        send(conn2,"3 : Contre-attaque")
        choix2 = recv(conn2) #Réception du choix du joueur 2

        #MISE EN CONFRONTATION DES CHOIX
        #Les soins sont executées avant les attaques
        if (choix1 == "2"): #Soin du J1
            broadcast("Joueur 1 se soigne !")
            gain = min(pv,pv1+soin1) - pv1 #On ne souhaite pas dépasser la limite de pv de base
            pv1 += gain
            broadcast("Joueur 1 a gagné "+str(gain)+" pv.\n")
        if (choix2 == "2"): #Soin du J2
            broadcast("Joueur 2 se soigne !")
            gain = min(pv,pv2+soin2) - pv2 #On ne souhaite pas dépasser la limite de pv de base
            pv2 += gain
            broadcast("Joueur 2 a gagné "+str(gain)+" pv.\n")
        if (choix1 == "1"): #Atq du J1
            broadcast("Joueur 1 attaque !")
            if (choix2 == "3"): #Catq du J2
                broadcast("Mais Joueur 2 contre-attaque !")
                pv1 -= catq2
                broadcast("Joueur 1 a perdu "+str(catq2)+" pv.\n")
            else:
                pv2 -= atq1
                broadcast("Joueur 2 a perdu "+str(atq1)+" pv.\n")
        if (choix2 == "1"): #Atq du J2
            broadcast("Joueur 2 attaque !")
            if (choix1 == "3"): #Catq du J1
                broadcast("Mais Joueur 1 contre-attaque !")
                pv2 -= catq1
                broadcast("Joueur 2 a perdu "+str(catq1)+" pv.\n")
            else:
                pv1 -= atq2
                broadcast("Joueur 1 a perdu "+str(atq2)+" pv.\n")
        if ((choix1 == "3")and(choix2 != "1")):
                broadcast("Joueur 1 contre-attaque !")
                broadcast("Mais c'est inefficace.\n")
        if ((choix2 == "3")and(choix1 != "1")):
                broadcast("Joueur 2 contre-attaque !")
                broadcast("Mais c'est inefficace\n")

    if ((pv1 <= 0)and(pv2 <= 0)):
        broadcast("Les deux joueurs n'ont plus de pv, c'est une égalité !")
    else:
        if (pv2 <= 0):
            broadcast("Le joueur 1 a gagné !")
        if (pv1 <= 0):
            broadcast("Le joueur 2 a gagné !")


############MAIN
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Type de connexion

#Etablissement de la connexion du serveur, on lui assigne un port
socket.bind((host,port))
print("Lancement du serveur") 

socket.listen(3) #Nombre de tentatives autorisées

while True:
    id_player = 1

    #Connexion des clients
    conn1, addr1 = socket.accept() #On attends que le client se connecte
    print("Connexion", id_player, "accepté")
    """PAS BESOIN
        my_thread = ThreadServer(conn,id_player)
        my_thread.start()
        #id_player += 1
    """
    send_msg(conn1,id_player)
    msg = recv_msg(conn1)
    if (msg == "OK"):
        print (id_player,"joueur(s) connecté(s)")
        print(addr1)
        id_player += 1
    else:
        print("echec de la connection")
        exit(1) #Arrete le serveur
    #deuxieme client
    conn2, addr2 = socket.accept()
    print("Connexion", id_player, "accepté")
    """ PAS BESOIN
        my_thread = ThreadServer(conn,id_player)
        my_thread.start()
        #id_player += 1
    """
    send_msg(conn2,id_player)
    msg = recv_msg(conn2)
    if (msg == "OK"):
        print (id_player,"joueur(s) connecté(s)")
        print(addr2)
        id_player += 1 #Permet de sortir de la boucle
    else:
        print("echec de la connection")
        exit(1) #Arrete le serveur

    send_msg(conn1,"READY")
    send_msg(conn2,"READY")

    msg1 = recv_msg(conn1)
    msg2 = recv_msg(conn2)
    if ((msg1 == "READY")and(msg2 == "READY")):
        print("CONNECTION SUCCESSFULL")

    game(conn1,conn2) #Lancement du jeu

    #Déconnexion
    send_msg(conn1,"STOP") 
    send_msg(conn2,"STOP")
    conn1.close() 
    conn2.close() 

socket.close()


