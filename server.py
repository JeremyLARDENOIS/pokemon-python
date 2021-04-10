#!/usr/bin/env python3
#coding:utf-8

host = ""
port = 3333

import socket

##############################################################

def send_msg (conn,msg):
    """Send a message msg to conn connection
    Arguments: conn, msg
    """
    msg = str(msg)
    data = msg.encode("utf-8")
    conn.sendall(data)
    addr = str(conn).split(',')[6].split("'")[1]    #Get IP from conn
    port = str(conn).split(',')[7].split(")")[0][1:]#Get port from conn
	
    print(addr,port,"->", msg)

def recv_msg (conn):
    """ Get a message from conn connection
    Arguments: conn
    Return: msg
    """
    data = conn.recv(255)
    msg  = data.decode("utf-8")
    addr = str(conn).split(',')[6].split("'")[1]    #Get IP from conn
    port = str(conn).split(',')[7].split(")")[0][1:]#Get port from conn
    print(addr,port,"<-", msg)
    return msg

def send (conn,msg):
    """
    Allow to send a message msg on a connection conn on a safe way    
    Arguments: conn, msg
    """
    send_msg(conn,"READ");          # Send "READ"
    status = recv_msg(conn)         # Recv status
    # If status is "OK", we send the message 
    if (status == "OK"):            
        send_msg(conn,msg);         
        status = recv_msg(conn)    
        # While status isn't "OK", we send the message again 
        while (status != "OK"):   
            send_msg(conn,msg)
            status = recv_msg(conn)
    # If status isn't "OK", we try again
    else:
        send(conn,msg)

def recv (conn):
    """
    Allow to receive a message msg from a connection conn on a safe way    
    Arguments: conn
    Return: msg
    """
    send_msg(conn,"WRITE")          # Send "WRITE"
    msg = recv_msg(conn)            # We receive the message
    if (msg == ""):                 # If no message, try again
        msg = recv(conn)
    else:                           # If receive something
        send_msg(conn,"OK")         # Send "OK"
        recv_msg(conn)              # Client answer "OK" too
    return msg

def broadcast(msg):
    """
    Send a message to all users
    Arguments: msg
    """
    send(conn1,msg)
    send(conn2,msg)

def recv2():
    """
    Receive message from all users
    Returns: (msg1, msg2)
    """
    send_msg(conn1,"WRITE2")        # Send "WRITE2" to player 1
    send_msg(conn2,"WRITE2")        # Send "WRITE2" to player 2
    
    status1 = recv_msg(conn1)       # Receive status from player 1
    status2 = recv_msg(conn2)       # Receive status from player 2

    # If all status is "OK"
    if ((status1 == "OK")and(status2 == "OK")):
        send_msg(conn1,"SEND")      # Send "SEND" to player 1
        msg1 = recv_msg(conn1)      # Receive msg from player 1
        send_msg(conn2,"SEND")      # Send "SEND" to player 2
        msg2 = recv_msg(conn2)      # Receivemsg from player 2
        send_msg(conn1,"OK")        # Send "OK" to player 1
        recv_msg(conn1)             # Receive status from player 1
        send_msg(conn2,"OK")        # Send "OK" to player 2
        recv_msg(conn2)             # Receive status from player 2
    else:                           # If one of status isn't "OK"
        return recv2()              # Try again

    return (msg1,msg2)

def game(conn1,conn2):
    """
    Game
    Arguments: conn1, conn2
    """
    hp=50       # Basic Health Point
    atk=15      # Basic Attack damage
    heal=5      # Basic Heal
    catk=10     # Counter Attack   
    costca=5    # Cost of miss Counter Attack

    broadcast("=========================================================================")

    msg = "Welcome on the Pokemon plateform combat online!\n\n"
    msg += "The objective is to put K.O. your opponent in putting his HP to 0\n"
    msg += "You start with " + str(hp) + " hp.\n"
    msg += "To do this, you have 3 possibilities:"
    broadcast(msg)

    msg = "A attack who inflict " + str(atk) + " hp\n"
    msg += "A heal who restore " + str(heal) + "hp\n"
    msg += "A counter attack who cancel enemy damages and return " + str(catk) + "hp against him\n"
    msg += "But if the ennemy doesn't make you damage, you loose " + str(costca) + "hp"

    broadcast(msg)

    broadcast("\nLET THE BATTLE BEGIN!\n")

    broadcast("But first of all, what is your name?")
    
    name1,name2 = recv2() 

    #Dans le cadre d'une future amélioration
    hp1=hp
    hp2=hp
    atk1=atk
    atk2=atk
    catk1=catk
    catk2=catk
    costca1 = costca
    costca2 = costca
    heal1=heal
    heal2=heal
    nb_turns = 1

    # While the two players isn't K.O.
    while ((hp1 > 0)and(hp2 > 0)):
        broadcast("=========================================================================")
        broadcast("turn n°"+str(nb_turns)+" :")
        broadcast("\n"+name1+" = "+str(hp1)+" hp & "+name2+" = "+str(hp2)+" hp" )
        
        nb_turns +=1

        # turn of the 2 players
        broadcast("It's your turn\n")
        broadcast("What do you want to do?")
        broadcast("1 : Attack")
        broadcast("2 : Heal")
        broadcast("3 : Counter-attack")

        choix1, choix2 = recv2() # Reception of choices
        # Implementation of them
        # Heals are executed before attacks
        if (choix1 == "2"):                     # Heal of player 1
            broadcast(name1+" heals himself!")
            gain = min(hp,hp1+heal1) - hp1      # We don't want to exceed the basic hp limit
            hp1 += gain
            broadcast(name1+" won "+str(gain)+" hp.\n")
        if (choix2 == "2"):                     # Heal of player 2
            broadcast(name2+" heals himself!")
            gain = min(hp,hp2+heal2) - hp2      # We don't want to exceed the basic hp limit
            hp2 += gain
            broadcast(name2+" won "+str(gain)+" hp.\n")
        if (choix1 == "1"):                     # Attack of player 1
            broadcast(name1 +" attack!")
            if (choix2 == "3"):                 # Counter-attack of player 2
                broadcast("But "+ name2 +" counter-attack!")
                hp1 -= catk2
                broadcast(name1+" lost "+ str(catk2) +" hp.\n")
            else:
                hp2 -= atk1
                broadcast(name2+" lost "+str(atk1)+" hp.\n")
        if (choix2 == "1"):                     # Attack of player 2
            broadcast(name2+" attack!")
            if (choix1 == "3"):                 # Counter-attack of player 1
                broadcast("But "+name1+" counter-attack!")
                hp2 -= catk1
                broadcast(name2+" lost "+str(catk1)+" hp.\n")
            else:
                hp1 -= atk2
                broadcast(name1+" lost "+str(atk2)+" hp.\n")
        if ((choix1 == "3")and(choix2 != "1")):
                broadcast(name1 +" counter-attack!")
                broadcast("But it's useless...\n")
                hp1 -= costca1
                broadcast(name1+" lost "+str(costca1)+" hp.\n")
        if ((choix2 == "3")and(choix1 != "1")):
                broadcast(name2+" counter-attack!")
                broadcast("But it's useless...\n")
                hp2 -= costca2
                broadcast(name2+" lost "+str(costca2)+" hp.\n")

    if ((hp1 <= 0)and(hp2 <= 0)):
        broadcast("Both players have no more hp, it's a tie!")
    else:
        if (hp2 <= 0):
            broadcast(name1+" won!")
        if (hp1 <= 0):
            broadcast(name2+" won!")


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


