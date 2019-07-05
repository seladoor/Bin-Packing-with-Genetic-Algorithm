import numpy.random as rnd
import math
from random import *
from utilities import *
from utilities_pack import * 
from model import *

###
# Function that generates the new population given the old population and all the control parameter of the genetic algorithm.
###
def next_generation(results: list, packs: list, n_elite: int, p_cross: float, p_mut: float, p_sel: float) -> list:
    results_error_sorted = sorted(results, key=lambda x: x.error)    
    elite = results_error_sorted[0:n_elite]
    rest = results_error_sorted[n_elite:]  
    shuffle(rest)
    
    next_gen = []
    offsprings = []
     

    ### elite
    for c in elite:
        all_ids = set([p.pack_id for p in packs])
        elite_ids = set([p.pack_id for p in c.packs])
        diff = list(all_ids.difference(elite_ids))
        to_add = [p for p in packs if p.pack_id in diff]
        if to_add:
            c.packs.extend(to_add)       
        
    ### parents
    parents = generate_parents(rest, p_sel, packs)
    ## crossover with prob p_cross
    rnd.seed(123)
    
    len_parents=len(parents)
    cross_y = rnd.binomial(1, p_cross, size=math.ceil(len_parents/2)).astype(bool)
    
    if (len_parents % 2 == 1 and cross_y[-1] == True):
        for i, prob in enumerate(cross_y):
            if not prob:
                cross_y[i] = True
                cross_y[-1] = False
                break
    
    i = 0
    while(len(parents)>1):
        i1,i2 = random_couple(len(parents))
        p1 = parents[i1]
        p2 = parents[i2]
        if(cross_y[i]):
            chromosomes = cross_over(parents)
            offsprings.append(chromosomes[0])
            offsprings.append(chromosomes[1])
        else:
            offsprings.append(p1)
            offsprings.append(p2)
        parents.remove(p1)
        parents.remove(p2)
        i += 1
    if(len(parents)==1):
        chromosome = parents[0]
        offsprings.append(chromosome)
    
    len_off = len(offsprings)
    rnd.seed(123)
    mut_y = rnd.binomial(1, p_mut, size=len_off).astype(bool) 
    
    for i in range(len_off):
        if(mut_y[i]):
              offsprings[i]=mutation(offsprings[i])  
    
    elite.extend(offsprings)
    
    return elite

###
# Function that generates parents from a list of initial chromosomes.
###
def generate_parents(chromosomes: list, p_sel: float, initial_packs: list) -> list:
    parents = []    
    len_result = len(chromosomes)
    gen_y = rnd.binomial(1, p_sel, size=len_result).astype(bool) 
    for i in range(len_result): 
        i1,i2 = random_couple(len_result)
        c1 = chromosomes[i1]
        c2 = chromosomes[i2]
        if (c1.error >= c2.error):
            if (gen_y[i]):
                parents.append(c2)
            else:
                parents.append(c1)
        else:
            if (gen_y[i]):
                parents.append(c1)
            else:
                parents.append(c2)
    for c in parents:
        all_ids = set([p.pack_id for p in initial_packs])
        parents_ids = set([p.pack_id for p in c.packs])
        diff = list(all_ids.difference(parents_ids))
        to_add = [p for p in initial_packs if p.pack_id in diff]
        if to_add:
            c.packs.extend(to_add)        

    return parents

###
# Function that given two parents, generates two offsprings (children).
###
def cross_over(parents: list) -> list:
    p1 = parents[0]
    p2 = parents[1]
    offsprings = []
    offspring1 = Chromosome(packs=[])
    offspring2 = Chromosome(packs=[])
    i1,j1 = random_couple_ordered(len(p1.packs))
    off_ids = []
    
    k = i1
    while(k <= j1):
        offspring1.packs.append(p1.packs[k])                      
        off_ids.append(p1.packs[k].pack_id)
        k+=1    
    for s in range(len(p2.packs)):
        if(p2.packs[s].pack_id not in off_ids):
            offspring1.packs.append(p2.packs[s])
            off_ids.append(p2.packs[s].pack_id)
    offsprings.append(offspring1)
    
    off_ids = []
    k = i1
    while(k <= j1):
        offspring2.packs.append(p2.packs[k])                      
        off_ids.append(p2.packs[k].pack_id)
        k+=1    
    for s in range(len(p1.packs)):
        if(p1.packs[s].pack_id not in off_ids):
            offspring2.packs.append(p1.packs[s])
            off_ids.append(p1.packs[s].pack_id)
    offsprings.append(offspring2)
        
    return offsprings
    
###
# Function that given a chromosome, mutates it by alterating (swapping) the dimensions of two of its packs.
###
def mutation(chromosome: Chromosome) -> Chromosome:
    i1,i2 = random_couple(len(chromosome.packs))
    chromosome.packs[i1] = swap_random(chromosome.packs[i1])
    chromosome.packs[i2] = swap_random(chromosome.packs[i2])
    return chromosome