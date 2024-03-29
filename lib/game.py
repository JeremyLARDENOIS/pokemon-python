'''Module of the game function'''

from socket import socket
from typing import List, Tuple
import lib.network as n
from lib.user import User


def game(users: Tuple[User, User]) -> None:
    '''
    Definition of the game from game module
    '''
    user1, user2 = users
    conns: List[socket] = [user1.conn, user2.conn]

    n.broadcast(
        conns, '=========================================================================')

    msg = 'Welcome on the Pokemon plateform combat online!\n\n'
    msg += 'The objective is to put K.O. your opponent in putting his HP to 0\n'
    msg += f'You start with {User.hp} hp.\n'
    msg += 'To do this, you have 3 possibilities:'
    n.broadcast(conns, msg)

    msg = f'A attack who inflict {User.atk} hp\n'
    msg += f'A heal who restore {User.heal} hp\n'
    msg += f'A counter attack who cancel enemy damages and return {User.catk} hp against him\n'
    msg += f'But if the ennemy doesn\'t make you damage, you loose {User.costca} hp'

    n.broadcast(conns, msg)

    n.broadcast(conns, '\nLET THE BATTLE BEGIN!\n')

    n.broadcast(conns, 'But first of all, what is your name?')

    user1.name, user2.name = n.recv2(conns)

    nb_turns = 1

    # While the two players isn't K.O.
    while ((user1.hp > 0) and (user2.hp > 0)):
        n.broadcast(
            conns, '=========================================================================')
        n.broadcast(conns, f'turn n°{nb_turns}:')
        n.broadcast(
            conns, f'\n{user1.name} = {user1.hp} hp & {user2.name} = {user2.hp} hp')

        nb_turns += 1

        # turn of the 2 players
        n.broadcast(conns, 'What do you want to do?')
        n.broadcast(conns, '1 : Attack')
        n.broadcast(conns, '2 : Heal')
        n.broadcast(conns, '3 : Counter-attack')

        choice1, choice2 = n.recv2(conns)  # Reception of choices
        # choice1, choice2 = n.recv_choose(conns, '1', '2', '3')  # Reception of choices
        # Implementation of them
        # Heals are executed before attacks
        # can be a match case
        if choice1 == '2':                     # Heal of player 1
            n.broadcast(conns, f'{user1.name} heals himself!')
            # We don't want to exceed the basic hp limit
            gain = min(User.hp, user1.hp +
                user1.heal) - user1.hp
            user1.hp += gain
            n.broadcast(conns, f'{user1.name} won {gain} hp.\n')
        if choice2 == '2':                     # Heal of player 2
            n.broadcast(conns, f'{user2.name} heals himself!')
            # We don't want to exceed the basic hp limit
            gain = min(User.hp, user2.hp +
                       user2.heal) - user2.hp
            user2.hp += gain
            n.broadcast(conns, f'{user2.name} won {gain} hp.\n')
        if choice1 == '1':                     # Attack of player 1
            n.broadcast(conns, f'{user1.name} attack!')
            if choice2 == '3':                 # If player 2 do counter attack
                n.broadcast(conns, f'But {user2.name} counter-attack!')
                user1.hp -= user2.catk
                n.broadcast(conns, f'{user1.name} lost {user2.catk} hp.\n')
            else:                               # If player 2 doesn't counter-attack
                user2.hp -= user1.atk
                n.broadcast(conns, f'{user2.name} lost {user1.atk} hp.\n')
        if choice2 == '1':                     # Attack of player 2
            n.broadcast(conns, f'{user2.name} attack!')
            if choice1 == '3':                 # Counter-attack of player 1
                n.broadcast(conns, f'But {user1.name} counter-attack!')
                user2.hp -= user1.catk
                n.broadcast(conns, f'{user2.name} lost {user1.catk} hp.\n')
            else:
                user1.hp -= user2.atk
                n.broadcast(conns, f'{user1.name} lost {user2.atk} hp.\n')
        if ((choice1 == '3') and (choice2 != '1')):
            n.broadcast(conns, f'{user1.name} counter-attack!')
            n.broadcast(conns, 'But it\'s useless...\n')
            user1.hp -= user1.costca
            n.broadcast(conns, f'{user1.name} lost {user1.costca} hp.\n')
        # If player 2 do counter attack and player 1 doesn't attack
        if ((choice2 == '3') and (choice1 != '1')):
            n.broadcast(conns, f'{user2.name} counter-attack!')
            n.broadcast(conns, 'But it\'s useless...\n')
            user2.hp -= user2.costca
            n.broadcast(conns, f'{user2.name} lost {user2.costca} hp.\n')

    if ((user1.hp <= 0) and (user2.hp <= 0)):
        n.broadcast(conns, 'Both players have no more hp, it\'s a tie!')
    else:
        if user2.hp <= 0:
            n.broadcast(conns, f'{user1.name} won with {user1.hp} HP!')
        if user1.hp <= 0:
            n.broadcast(conns, f'{user2.name} won with {user2.hp} HP!')
