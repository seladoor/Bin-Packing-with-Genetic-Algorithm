from utilities_chromosomes import *
from error import *
from model import *
from next_generation import *
from utilities_pack import *
from rectpack import newPacker

###
# Function which is responsible of resolving an entire layer using the genetic algorithm together with its control paramenters.
###
def resolve_layer(packs: list, ordering: str, n_iter: int, n_chromosomes: int, n_elite: int, p_cross: float, p_mut: float, p_sel: float) -> tuple:
    
    k = 0.8/3

    # first_generation
    chromosomes = generate_custom(packs)
    random_chromosomes = generate_random(packs, n=n_chromosomes - 2)
    chromosomes.extend(random_chromosomes) ### in place
    
    # calculate_fitness
    result_for_iteration = {}
    for _iter in range(n_iter):
        results = []
        chromosomes = order_by(chromosomes, by=ordering, k=k) ## eventually area
        print('iteration {}, chromosomes: {}'.format(_iter,len(chromosomes)))
        for i, chromosome in enumerate(chromosomes):
            print('chromosome {}'.format(i))
            rect_used = fill_layer(chromosome.packs)
            ### The algorithm could potentially insert more packs than the used ones. 
            if (len(rect_used) == len(packs)):
                print('WARNING: empty space not used')

            if (len(rect_used) < int(len(chromosome.packs) * k) and ordering == 'area'):
                print('not enough packs inserted to use the sort by area: using sort by id instead')
                chromosome.packs = sorted(chromosome.packs, key=lambda p: p.pack_id, reverse=True)
                rect_used = fill_layer(chromosome.packs)
                
            print('finish fill_layer, used {}'.format(len(rect_used)))
            ids = [x.rid for x in rect_used]
            packs_used = [x for x in chromosome.packs if x.pack_id in ids]
            heights = [x.z for x in packs_used]
            total_error = compute_error_sigma(rect_used, chromosome.packs) + 2*max(heights)
            total_error_pct = total_error / len(rect_used)
            results.append(Chromosome(packs_used, total_error_pct))
        
        result_for_iteration[_iter] = results

        print('iteration {} done. evolving to next generation'.format(_iter))
        
        result_copy = []
        for c in results:
            chrom_copy = Chromosome(c.packs[:], c.error)
            result_copy.append(chrom_copy)
        
        chromosomes = next_generation(result_copy, packs, n_elite, p_cross, p_mut, p_sel)
        
    return best(result_for_iteration)

###
# Given an initial list of packs (population), that function generates two chromosomes:
# the first one contains the population itself.
# the second one contains the packs rotated in a way the z dimension is the smallest of the three.
###
def generate_custom(population: list) -> list:
    ### d3 <= d2
    custom1 = Chromosome([swap_dimensions(pack, 'x') for pack in population])
    # d3 <= d1
    custom2 = Chromosome([swap_dimensions(pack, 'y') for pack in custom1.packs])
    return [Chromosome(population), custom2]
    
###
# Given an initial list of packs (population), that function generates n chromosomes 
# provided with random swap of dimension of its packs.
###
def generate_random(population: list, n: int) -> list:
    chromosomes = [Chromosome([swap_random(pack) for pack in population]) for i in range(n)]
    return chromosomes

###
# Function that resolve the 2d layer using the 2d resolver.
# It first add the 1000x1000 bin to the packer, then add the input packs to it using the add_pack function (see utilities_pack.add_pack).
# returns the list of used packs.
###
def fill_layer(packs: list) -> list:
    layer = (1000, 1000) # 1000x1000 rectangle
    packer = newPacker(sort_algo=None)
    packer.add_bin(*layer)
    for pack in packs:
        add_pack(pack, packer)
    packer.pack() ## try fit as elements as possible into the layer
    return packer[0] # packs used
