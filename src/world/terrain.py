class Terrain(object):
    def __init__(self, map):
        self.map = map

    def width(self):
        return len(self.map[0])
    
    def height(self):
        return len(self.map)

    def center(self):
        w = len(self.map[0])
        h = len(self.map)
        return (w // 2, h // 2)
