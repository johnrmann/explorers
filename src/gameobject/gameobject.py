class GameObject(object):
    """
    Represents a thing in the game world. Can be a character, a prop, or
    invisible tiles that can be interacted with.
    """

    def __init__(self, pos = (0, 0), size = (1, 1)):
        """
        Position is the top left tile that the game object occupies.
        """

        self.pos = pos
        self.size = size
    