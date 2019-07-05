from random import choice
import json

###
# Function which choose two random numbers from a list.
# The list is generated taking into account the input parameter length.
###
def random_couple(length: int) -> (int, int):
    indexes = [i for i in range(length)]
    i1 = choice(indexes)
    i2 = choice(indexes)
    while i1 == i2:
        i2 = choice(indexes)
    return i1,i2

###
# Function which choose two random numbers from a list and return the ordered couple.
# The list is generated taking into account the input parameter length.
###
def random_couple_ordered(length: int) -> (int, int):
    indexes = [i for i in range(length)]
    i1 = choice(indexes)
    i1, i2 = 0, 0
    if(i1==length):
        i2 = i1
        i1 -= 1
        return i1,i2
    indexes = [i for i in range(i1 + 1, length)] ### check this
    i2 = choice(indexes)
    return i1,i2
    
###
# Utility function which dumps the results (from layer l1 to layer l2) of the algorithm. 
# Used for debugging and for collecting final results.
###
def dump_results(l1: int, l2: int, packs_per_layer: list, best_error_per_layer:list, error_per_layer: list,error_per_layer_pct:list,  average_error_per_layer: list, time_per_layer: list):
    with open('results/results-{}-{}.json'.format(l1, l2), 'w') as f:
        json.dump(
                        {'packs_per_layer': [{_iter: len(packs) for _iter, packs in p.items()} for p in packs_per_layer], 
                        'best_error_per_layer': best_error_per_layer,
                        'error_per_layer': error_per_layer,
                        'error_per_layer_pct': error_per_layer_pct,
                        'average_error_per_layer': average_error_per_layer,
                        'max_height_per_layer': [{_iter: str(max(packs, key=lambda x: x.z).z) for _iter, packs in p.items()} for p in packs_per_layer], 
                        'time_per_layer': time_per_layer
                        }, 
                        f
                    )

###
# Utility function which dumps the results (from layer l1 to layer l2) of the algorithm without the genetic part.
# Used for debugging and for collecting final results.
###
def dump_results_simple(l1: int, l2: int, packs_per_layer: list, error_per_layer: list,error_per_layer_pct:list, time_per_layer: list):
    with open('results/results-no-genetic-{}-{}.json'.format(l1, l2), 'w') as f:
        json.dump(
                        {'packs_per_layer': [str(len(p)) for p in packs_per_layer], 
                        'error_per_layer': error_per_layer,
                        'error_per_layer_pct': error_per_layer_pct,
                        'time_per_layer': time_per_layer
                        }, 
                        f
                    )