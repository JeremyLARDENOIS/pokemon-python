class User:
    """
    Class User :
    """

    def __init__(self, name="", conn=None, addr=None, id=None):
        """Init user"""
        self.name: str = name
        self.hp = 50        # Basic Health Point
        self.atk = 15       # Basic Attack damage
        self.heal = 5       # Basic Heal
        self.catk = 10      # Counter Attack
        self.costca = 5     # Cost of miss Counter Attack
        self.conn = conn    # Connection
        self.addr = addr    # Address
        self.id = id        # Id

    def __str__(self):
        """String of user"""
        return f"{self.name} : {self.hp} hp"

    def stop(self):
        """Stop user"""
        self.conn.close()
