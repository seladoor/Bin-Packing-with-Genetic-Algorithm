import numpy as np

###
# Function that finds the best couple (packs used, error) for each iteration done. 
# It also returns the final best couple and the average error per iteration.
###
def best(results: dict) -> (dict, tuple):
    bests = {}
    average_error_per_iter = {}
    all_errors_per_iter = {}
    all_errors_per_iter_pct = {}
    best_iter = None
    for iteration, chromosomes in results.items():
        best_chromosome = []
        best_error_iter = 99999999999999999999999999
        key = 'iteration-{}'.format(iteration)
        if (iteration == len(results) - 1):
                for chromosome in chromosomes:
                        if (chromosome.error < best_error_iter):
                                best_error_iter = chromosome.error
                                best_chromosome = chromosome.packs
                                best_iter = (best_chromosome, best_error_iter * len(chromosome.packs))
                        bests[key] = (best_chromosome, best_error_iter * len(chromosome.packs))
        average_error_per_iter[key] = sum([c.error *len(c.packs) for c in chromosomes])/len(chromosomes)
        all_errors_per_iter[key] = [c.error * len(c.packs) for c in chromosomes]
        all_errors_per_iter_pct[key] = [c.error for c in chromosomes]
    return (bests, best_iter, average_error_per_iter, all_errors_per_iter, all_errors_per_iter_pct)

###
# Function that returns the sigma error contribution for the evaluation function of the kaggle's challenge.
# see https://www.kaggle.com/c/packing-santas-sleigh/overview/evaluation
###
def compute_error_sigma(packs_used: list, total_packs: list) -> float:
    id_used = [x.rid for x in packs_used]
    elem_used = [pack for pack in total_packs if pack.pack_id in id_used]
    elem_used = sorted(elem_used, key=lambda p: p.z, reverse=True)
    order = [x for x in reversed(range(id_used[0] + 1-len(elem_used), id_used[0] + 1))]
    for i in range(0,len(elem_used)-1):
        if (elem_used[i].z == elem_used[i+1].z and elem_used[i].pack_id > elem_used[i+1].pack_id):
            tmp = elem_used[i+1]
            elem_used[i+1] = elem_used[i]
            elem_used[i] = tmp
    ids = [x.pack_id for x in elem_used]
    return abs(np.subtract(ids, order)).sum()  