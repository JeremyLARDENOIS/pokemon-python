from lib.network import *
from lib.user import User


def game(user1, user2):
    """
    Game
    Arguments: conn1, conn2
    """
    conns = [user1.conn, user2.conn]

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

    user1.name, user2.name = recv2(conns)

    nb_turns = 1

    # While the two players isn't K.O.
    while ((user1.hp > 0) and (user2.hp > 0)):
        broadcast(
            conns, "=========================================================================")
        broadcast(conns, "turn n°"+str(nb_turns)+" :")
        broadcast(conns, "\n"+user1.name+" = "+str(user1.hp) +
                  " hp & "+user2.name+" = "+str(user2.hp)+" hp")

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
            broadcast(conns, user1.name+" heals himself!")
            # We don't want to exceed the basic hp limit
            gain = min(User().hp, user1.hp +
                       user1.heal) - user1.hp
            user1.hp += gain
            broadcast(conns, user1.name+" won "+str(gain)+" hp.\n")
        if (choix2 == "2"):                     # Heal of player 2
            broadcast(conns, user2.name+" heals himself!")
            # We don't want to exceed the basic hp limit
            gain = min(User().hp, user2.hp +
                       user2.heal) - user2.hp
            user2.hp += gain
            broadcast(conns, user2.name+" won "+str(gain)+" hp.\n")
        if (choix1 == "1"):                     # Attack of player 1
            broadcast(conns, user1.name + " attack!")
            if (choix2 == "3"):                 # If player 2 do counter attack
                broadcast(conns, "But " + user2.name + " counter-attack!")
                user1.hp -= user2.catk
                broadcast(conns, user1.name+" lost " +
                          str(user2.catk) + " hp.\n")
            else:                               # If player 2 doesn't counter-attack
                user2.hp -= user1.atk
                broadcast(conns, user2.name +
                          " lost "+str(user1.atk)+" hp.\n")
        if (choix2 == "1"):                     # Attack of player 2
            broadcast(conns, user2.name+" attack!")
            if (choix1 == "3"):                 # Counter-attack of player 1
                broadcast(conns, "But "+user1.name+" counter-attack!")
                user2.hp -= user1.catk
                broadcast(conns, user2.name +
                          " lost "+str(user1.catk)+" hp.\n")
            else:
                user1.hp -= user2.atk
                broadcast(conns, user1.name +
                          " lost "+str(user2.atk)+" hp.\n")
        if ((choix1 == "3") and (choix2 != "1")):
            broadcast(conns, user1.name + " counter-attack!")
            broadcast(conns, "But it's useless...\n")
            user1.hp -= user1.costca
            broadcast(conns, user1.name+" lost " +
                      str(user1.costca)+" hp.\n")
        # If player 2 do counter attack and player 1 doesn't attack
        if ((choix2 == "3") and (choix1 != "1")):
            broadcast(conns, user2.name+" counter-attack!")
            broadcast(conns, "But it's useless...\n")
            user2.hp -= user2.costca
            broadcast(conns, user2.name+" lost " +
                      str(user2.costca)+" hp.\n")

    if ((user1.hp <= 0) and (user2.hp <= 0)):
        broadcast(conns, "Both players have no more hp, it's a tie!")
    else:
        if (user2.hp <= 0):
            broadcast(conns, user1.name+" won!")
        if (user1.hp <= 0):
            broadcast(conns, user2.name+" won!")
