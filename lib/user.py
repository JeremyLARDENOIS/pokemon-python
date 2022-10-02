'''Module of the class User'''

from socket import socket


class User:
    '''
    Class User :
    '''
    hp = 50        # Basic Health Point
    atk = 15       # Basic Attack damage
    heal = 5       # Basic Heal
    catk = 10      # Counter Attack
    costca = 5     # Cost of miss Counter Attack

    def __init__(self, name: str, conn: socket, addr: str, connection_id: int) -> None:
        '''Init user'''
        self.name: str = name
        self.conn = conn    # Connection
        self.addr = addr    # Address
        self.connection_id = connection_id        # Id

    def __str__(self) -> str:
        '''String of user'''
        return f'{self.name} : {self.hp} hp'

    def stop(self) -> None:
        '''Stop user'''
        if self.conn:
            self.conn.close()
