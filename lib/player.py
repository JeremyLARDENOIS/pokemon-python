class Player:
    """
    Class Player :
    """

    def __init__(self, name=""):
        """Init player"""
        self.name = name
        self.hp = 50       # Basic Health Point
        self.atk = 15      # Basic Attack damage
        self.heal = 5      # Basic Heal
        self.catk = 10     # Counter Attack
        self.costca = 5    # Cost of miss Counter Attack
