###
# Class that represents the element to be placed in the santa's sleigh. 
# It is provided with 3 dimensions (x, y, z) and a pack_id.
# There is also an utility method which computes the 2d area (x * y) of the pack.
###
class Pack:
    def __init__(self, x: int, y: int, z: int, pack_id: int):
        self.x = x
        self.y = y
        self.z = z
        self.pack_id = pack_id

    def area(self):
        return self.x * self.y

###
# Class that represents a single chromosome. 
# It is provided with the list of packs, and the error gathered (which is initialized at 0).
###
class Chromosome:
    def __init__(self, packs: list, error: float = 0):
        self.packs = packs
        self.error = error