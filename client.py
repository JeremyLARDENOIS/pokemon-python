#!/usr/bin/env python3

import socket

host = ""
port = 3334

######################################

def send_msg (msg):
    """
    Envoie un message au serveur
    """
    data = msg.encode("utf-8")
    socket.sendall(data)

def recv_msg ():
    """
    Permet de recevoir message du serveur et le retourne en sortie
    """
    data = socket.recv(255)
    msg = data.decode("utf-8") 
    return msg

##########################################################

socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try :
    socket.connect((host,port)) #On se connecte au serveur
    print("Client connecté au Client") 
    print("Demande d'un id_player au serveur...")
    id_player = recv_msg() #On récupère un identifiant
    if (id_player != ""):
        send_msg("OK") #On dit au serveur que l'on a bien recu l'identifiant
        print("Connecté avec l'identifiant", id_player)
    else:
        print ("non connecté")
        exit(1)
    if (recv_msg() == "READY"): #Si le serveur est pret
            send_msg("READY") #On lui répond que l'on est prêt
    else:
        print("Déconnexion du serveur")
        socket.close()
        exit(2)

### D'abord le serveur nous dit quoi faire, puis on agit selon ce qu'il dit
    status = recv_msg()
    while ((status != "" )and( status != "STOP")):
        if (status == "READ"):
            send_msg("OK")          #On signal que l'on est prêt à la reception
            msg = recv_msg()        #On reçoit le message
            print(msg)
            if (msg != ""):         #Si on a bien reçu quelque chose
                status = "OK"       #On demande au client de renvoyer ok
        if (status == "WRITE"):
            msg = input('-> ')       #L'utilisateur rentre un message
            send_msg(msg)           #On envoie son message
            status = recv_msg()     #On reçois le status
        if (status == "OK"):
            send_msg("OK")
        
        status = recv_msg()

    """
    while ((status != "")and(status != "STOP")):
        if (status == "READ"):
            send_msg
            recv_msg()
        if (status == "WRITE"):
            msg = input()
            send_msg(msg)
        status = recv_msg()
        print(status)
    """


finally:       
    socket.close()



"""
Exemple d'erreur:
On obtient cela pour le premier status:
> READC'est au tour du joueur 1 :READQue voulez-vous faire ?READ1 : AttaqueWRITE
Et on voudrait obtenir:
> READ
Car la suite est censé etre dans les variables suivantes..
"""

