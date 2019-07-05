from random import shuffle
from model import*

###
# Simple function that add the 2d pack to the packer object.
###
def add_pack(pack: Pack, packer: object):
    rectangle = (pack.x, pack.y)
    rid = pack.pack_id
    packer.add_rect(*rectangle, rid=rid)

###
# Function that given a pack and a dimension, swap the position between the Z dimension and the input dimension
# if the value of z is greater than the value of that dimension for the considered Pack.
###
def swap_dimensions(elem: Pack, dimension: str ='x') -> Pack:
    elem_new = Pack(elem.x,elem.y,elem.z, elem.pack_id)
    if (dimension == 'x'):
        to_swap = elem_new.x
    elif dimension == 'y':
        to_swap = elem_new.y
    else:
        return elem
    if (elem.z > to_swap):
        tmp = elem_new.z
        elem_new.z = to_swap
        if (dimension == 'x'):
            elem_new.x = tmp 
        elif dimension == 'y':
            elem_new.y = tmp 
        
    return elem_new

###
# Function that given a pack, randomly swap the dimension of that pack.
###
def swap_random(elem: Pack) -> Pack:
    elem_new = Pack(elem.x,elem.y,elem.z, elem.pack_id)
    shuffled = [elem_new.x, elem_new.y, elem_new.z]
    shuffle(shuffled)
    elem_new.x = shuffled[0]
    elem_new.y = shuffled[1]
    elem_new.z = shuffled[2]
    return elem_new

