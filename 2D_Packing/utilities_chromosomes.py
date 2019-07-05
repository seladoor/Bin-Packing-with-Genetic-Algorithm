from model import *

###
# Function that sorts the packs contained in the input chromosomes by descending pack_id (PresentId).
###
def order_by_id(chromosomes: list) -> list:
    for c in chromosomes:
        c.packs = sorted(c.packs, key=lambda p: p.pack_id, reverse=True)
    return chromosomes
        
###
# Function that sorts the packs of the input chromosomes in two different ways:
# it the value of by paramenter is 'id', then it calls the above function.
# otherwise, sorts the first k elem of the packs in each chromosome by area and the latter part by id.
###
def order_by(chromosomes: list, by: str = 'id', k: float = 2/3) -> list:
    if (by == 'id'):
        return order_by_id(chromosomes)
    if (by == 'area'):
        ordered = []
        for c in chromosomes:
            split_point = int(len(c.packs) * k)
            last_part = Chromosome(sorted(c.packs[split_point:], key=lambda p: p.pack_id, reverse=True))
            
            first_part = Chromosome(c.packs[:split_point])
            first_part.packs = sorted(first_part.packs, key=lambda p: p.area(), reverse=True)
            first_part.packs.extend(last_part.packs)
            
            ordered.append(Chromosome(first_part.packs, error=c.error))
        
        return ordered
    else:
        return chromosomes