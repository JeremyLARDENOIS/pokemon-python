from lib.network import *
from lib.user import User


def game(conn1, conn2):
    """
    Game
    Arguments: conn1, conn2
    """
    conns = [conn1, conn2]
    players = [User(), User()]

    broadcast(
        conns, "=========================================================================")

    msg = "Welcome on the Pokemon plateform combat online!\n\n"
    msg += "The objective is to put K.O. your opponent in putting his HP to 0\n"
    msg += "You start with " + str(User().hp) + " hp.\n"
    msg += "To do this, you have 3 possibilities:"
    broadcast(conns, msg)

    msg = "A attack who inflict " + str(User().atk) + " hp\n"
    msg += "A heal who restore " + str(User().heal) + "hp\n"
    msg += "A counter attack who cancel enemy damages and return " + \
        str(User().catk) + "hp against him\n"
    msg += "But if the ennemy doesn't make you damage, you loose " + \
        str(User().costca) + "hp"

    broadcast(conns, msg)

    broadcast(conns, "\nLET THE BATTLE BEGIN!\n")

    broadcast(conns, "But first of all, what is your name?")

    players[0].name, players[1].name = recv2(conns)

    nb_turns = 1

    # While the two players isn't K.O.
    while ((players[0].hp > 0) and (players[1].hp > 0)):
        broadcast(
            conns, "=========================================================================")
        broadcast(conns, "turn n°"+str(nb_turns)+" :")
        broadcast(conns, "\n"+players[0].name+" = "+str(players[0].hp) +
                  " hp & "+players[1].name+" = "+str(players[1].hp)+" hp")

        nb_turns += 1

        # turn of the 2 players
        broadcast(conns, "What do you want to do?")
        broadcast(conns, "1 : Attack")
        broadcast(conns, "2 : Heal")
        broadcast(conns, "3 : Counter-attack")

        choix1, choix2 = recv2(conns)  # Reception of choices
        # Implementation of them
        # Heals are executed before attacks
        if (choix1 == "2"):                     # Heal of player 1
            broadcast(conns, players[0].name+" heals himself!")
            # We don't want to exceed the basic hp limit
            gain = min(User().hp, players[0].hp +
                       players[0].heal) - players[0].hp
            players[0].hp += gain
            broadcast(conns, players[0].name+" won "+str(gain)+" hp.\n")
        if (choix2 == "2"):                     # Heal of player 2
            broadcast(conns, players[1].name+" heals himself!")
            # We don't want to exceed the basic hp limit
            gain = min(User().hp, players[1].hp +
                       players[1].heal) - players[1].hp
            players[1].hp += gain
            broadcast(conns, players[1].name+" won "+str(gain)+" hp.\n")
        if (choix1 == "1"):                     # Attack of player 1
            broadcast(conns, players[0].name + " attack!")
            if (choix2 == "3"):                 # If player 2 do counter attack
                broadcast(conns, "But " + players[1].name + " counter-attack!")
                players[0].hp -= players[1].catk
                broadcast(conns, players[0].name+" lost " +
                          str(players[1].catk) + " hp.\n")
            else:                               # If player 2 doesn't counter-attack
                players[1].hp -= players[0].atk
                broadcast(conns, players[1].name +
                          " lost "+str(players[0].atk)+" hp.\n")
        if (choix2 == "1"):                     # Attack of player 2
            broadcast(conns, players[1].name+" attack!")
            if (choix1 == "3"):                 # Counter-attack of player 1
                broadcast(conns, "But "+players[0].name+" counter-attack!")
                players[1].hp -= players[0].catk
                broadcast(conns, players[1].name +
                          " lost "+str(players[0].catk)+" hp.\n")
            else:
                players[0].hp -= players[1].atk
                broadcast(conns, players[0].name +
                          " lost "+str(players[1].atk)+" hp.\n")
        if ((choix1 == "3") and (choix2 != "1")):
            broadcast(conns, players[0].name + " counter-attack!")
            broadcast(conns, "But it's useless...\n")
            players[0].hp -= players[0].costca
            broadcast(conns, players[0].name+" lost " +
                      str(players[0].costca)+" hp.\n")
        # If player 2 do counter attack and player 1 doesn't attack
        if ((choix2 == "3") and (choix1 != "1")):
            broadcast(conns, players[1].name+" counter-attack!")
            broadcast(conns, "But it's useless...\n")
            players[1].hp -= players[1].costca
            broadcast(conns, players[1].name+" lost " +
                      str(players[1].costca)+" hp.\n")

    if ((players[0].hp <= 0) and (players[1].hp <= 0)):
        broadcast(conns, "Both players have no more hp, it's a tie!")
    else:
        if (players[1].hp <= 0):
            broadcast(conns, players[0].name+" won!")
        if (players[0].hp <= 0):
            broadcast(conns, players[1].name+" won!")
