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
    pv1=30
    pv2=30
    atq1=10
    atq2=10
    tour=1

    while ((pv1 > 0)and(pv2 > 0)):
        broadcast("\nJoueur 1 = "+str(pv1)+" pv & Joueur 2 = "+str(pv2)+" pv" )
        broadcast("C'est au tour du joueur 1\n")
        send(conn2,"En attente du joueur 1...\n")
        
        send(conn1,"Que voulez-vous faire ?")
        send(conn1,"1 : Attaque")
        choix = recv(conn1)

        if(choix == "1"):
            broadcast("Joueur 1 attaque !")
            pv2 -= atq1
            broadcast("Joueur 2 a perdu "+str(atq1)+" pv")

        if (pv2 > 0):
            broadcast("\nJoueur 1 = "+str(pv1)+" pv & Joueur 2 = "+str(pv2)+" pv" )
            broadcast("C'est au tour du joueur 2 :")
            send(conn1,"En attente du joueur 2...")
        
            send(conn2,"Que voulez-vous faire ?")
            send(conn2,"1 : Attaque")
            choix = recv(conn2)

            if(choix == "1"):
                broadcast("Joueur 2 attaque !")
                pv1 -= atq2
                broadcast("Joueur 1 a perdu "+str(atq2)+" pv")
    if (pv2 <= 0):
        broadcast("Le joueur 1 a gagné")
    if (pv1 <= 0):
        broadcast("Le joueur 2 a gagné")


############MAIN
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Type de connexion

#Etablissement de la connexion du serveur, on lui assigne un port
socket.bind((host,port))
print("Lancement du serveur") 

socket.listen(3) #Nombre de tentatives autorisées

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

