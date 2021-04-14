#!/usr/bin/env python3
#coding:utf-8

host = ""
port = 3333

import socket

from lib.network import *
from lib.game import *

# def game(conn1,conn2):
#     """
#     Game
#     Arguments: conn1, conn2
#     """
#     conns = (conn1,conn2)
#     hp=50       # Basic Health Point
#     atk=15      # Basic Attack damage
#     heal=5      # Basic Heal
#     catk=10     # Counter Attack   
#     costca=5    # Cost of miss Counter Attack

#     broadcast(conns, "=========================================================================")

#     msg = "Welcome on the Pokemon plateform combat online!\n\n"
#     msg += "The objective is to put K.O. your opponent in putting his HP to 0\n"
#     msg += "You start with " + str(hp) + " hp.\n"
#     msg += "To do this, you have 3 possibilities:"
#     broadcast(conns, msg)

#     msg = "A attack who inflict " + str(atk) + " hp\n"
#     msg += "A heal who restore " + str(heal) + "hp\n"
#     msg += "A counter attack who cancel enemy damages and return " + str(catk) + "hp against him\n"
#     msg += "But if the ennemy doesn't make you damage, you loose " + str(costca) + "hp"

#     broadcast(conns, msg)

#     broadcast(conns, "\nLET THE BATTLE BEGIN!\n")

#     broadcast(conns, "But first of all, what is your name?")
    
#     name1,name2 = recv2(conns) 

#     #Dans le cadre d'une future amélioration
#     hp1=hp
#     hp2=hp
#     atk1=atk
#     atk2=atk
#     catk1=catk
#     catk2=catk
#     costca1 = costca
#     costca2 = costca
#     heal1=heal
#     heal2=heal
#     nb_turns = 1

#     # While the two players isn't K.O.
#     while ((hp1 > 0)and(hp2 > 0)):
#         broadcast(conns, "=========================================================================")
#         broadcast(conns, "turn n°"+str(nb_turns)+" :")
#         broadcast(conns, "\n"+name1+" = "+str(hp1)+" hp & "+name2+" = "+str(hp2)+" hp" )
        
#         nb_turns +=1

#         # turn of the 2 players
#         broadcast(conns, "It's your turn\n")
#         broadcast(conns, "What do you want to do?")
#         broadcast(conns, "1 : Attack")
#         broadcast(conns, "2 : Heal")
#         broadcast(conns, "3 : Counter-attack")

#         choix1, choix2 = recv2(conns) # Reception of choices
#         # Implementation of them
#         # Heals are executed before attacks
#         if (choix1 == "2"):                     # Heal of player 1
#             broadcast(conns, name1+" heals himself!")
#             gain = min(hp,hp1+heal1) - hp1      # We don't want to exceed the basic hp limit
#             hp1 += gain
#             broadcast(conns, name1+" won "+str(gain)+" hp.\n")
#         if (choix2 == "2"):                     # Heal of player 2
#             broadcast(conns, name2+" heals himself!")
#             gain = min(hp,hp2+heal2) - hp2      # We don't want to exceed the basic hp limit
#             hp2 += gain
#             broadcast(conns, name2+" won "+str(gain)+" hp.\n")
#         if (choix1 == "1"):                     # Attack of player 1
#             broadcast(conns, name1 +" attack!")
#             if (choix2 == "3"):                 # Counter-attack of player 2
#                 broadcast(conns, "But "+ name2 +" counter-attack!")
#                 hp1 -= catk2
#                 broadcast(conns, name1+" lost "+ str(catk2) +" hp.\n")
#             else:
#                 hp2 -= atk1
#                 broadcast(conns, name2+" lost "+str(atk1)+" hp.\n")
#         if (choix2 == "1"):                     # Attack of player 2
#             broadcast(conns, name2+" attack!")
#             if (choix1 == "3"):                 # Counter-attack of player 1
#                 broadcast(conns, "But "+name1+" counter-attack!")
#                 hp2 -= catk1
#                 broadcast(conns, name2+" lost "+str(catk1)+" hp.\n")
#             else:
#                 hp1 -= atk2
#                 broadcast(conns, name1+" lost "+str(atk2)+" hp.\n")
#         if ((choix1 == "3")and(choix2 != "1")):
#                 broadcast(conns, name1 +" counter-attack!")
#                 broadcast(conns, "But it's useless...\n")
#                 hp1 -= costca1
#                 broadcast(conns, name1+" lost "+str(costca1)+" hp.\n")
#         if ((choix2 == "3")and(choix1 != "1")):
#                 broadcast(conns, name2+" counter-attack!")
#                 broadcast(conns, "But it's useless...\n")
#                 hp2 -= costca2
#                 broadcast(conns, name2+" lost "+str(costca2)+" hp.\n")

#     if ((hp1 <= 0)and(hp2 <= 0)):
#         broadcast(conns, "Both players have no more hp, it's a tie!")
#     else:
#         if (hp2 <= 0):
#             broadcast(conns, name1+" won!")
#         if (hp1 <= 0):
#             broadcast(conns, name2+" won!")


##################################MAIN#############################################
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   # Type de connexion
socket.bind((host,port))                                    # Establishment of the server connection
print("Launching server") 
socket.listen(3)                                            # Number of attempts allowed

while True:                                                 # The server doesn't close at the end of the game
    id_player = 1

    # Clients connection
    conn1, addr1 = socket.accept()                          # Waiting for clients
    print(conn1)
    print("Connexion", id_player, "accepté")

    send_msg(conn1,id_player)
    msg = recv_msg(conn1)
    if (msg == "OK"):
        print (id_player,"joueur(s) connecté(s)")
        print(addr1)
        id_player += 1
    else:
        print("echec de la connection")
        exit(1) # Stop server
    
    # Second client
    conn2, addr2 = socket.accept()
    print("Connexion", id_player, "accepté")

    send_msg(conn2,id_player)
    msg = recv_msg(conn2)
    if (msg == "OK"):
        print (id_player,"joueur(s) connecté(s)")
        print(addr2)
        id_player += 1
    else:
        print("echec de la connection")
        exit(1) # Stop server

    send_msg(conn1,"READY")
    send_msg(conn2,"READY")

    msg1 = recv_msg(conn1)
    msg2 = recv_msg(conn2)
    if ((msg1 == "READY")and(msg2 == "READY")):
        print("CONNECTION SUCCESSFULL")

    ###################################
    game(conn1,conn2) # Launch the game
    ###################################

    #Déconnexion
    send_msg(conn1,"STOP") 
    send_msg(conn2,"STOP")
    conn1.close() 
    conn2.close() 

socket.close()


