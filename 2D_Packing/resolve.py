import datetime
import math
from model import *
from resolve_layer import *
import pandas as pd

###
# Main function of the algorithm. It firstly converts each row of the presents dataset into a Pack.
# Then, while there are packs available:
# - try to fill the layer as much as possiible
# - given the number of packs used, we call the resolve_function (see resolve_layer.py) which returns the result for each iteration coupled with the best one.
# - every two layers, the results are saved on a json file.
# At the end, a final dump contained the entire result is performed.
###
def resolve(presents: pd.DataFrame, use_genetic: bool, ordering: str, n_iter: int, n_chromosomes: int, elite: int, p_cross: float, p_mut: float, p_t: float) -> list:
    print('Converting from dataframe to packs at {}'.format(datetime.datetime.now()))
    available_packs = [Pack(p.Dimension1, p.Dimension2, p.Dimension3, p.PresentId) for _, p in presents.iterrows()] ### internalizing to Pack model
    print('Done at {}'.format(datetime.datetime.now()))
    packs_per_layer = []
    error_per_layer = []
    error_per_layer_pct = []
    average_error_per_layer = []
    best_error_per_layer = []
    time_per_layer = []
    count = 1
    print('Starting 3d packaging problem at {}'.format(datetime.datetime.now()))
    while len(available_packs) > 0:
        print('\n------- layer {} -------'.format(count))
        start_time_try = datetime.datetime.now()
        packs_used = fill_layer(available_packs)
        print('tried to fit layer. used {} packs'.format(len(packs_used)))
        start_time_genetic = datetime.datetime.now()
        used = None
        error = None 
        if (use_genetic):
            print('starting genetic algoritm at {}'.format(start_time_genetic))
            many_packs = math.ceil(len(packs_used) * 3)
            if(many_packs > len(available_packs)):
                many_packs = len(available_packs)
            (iteration_result, (best_used, best_error), average_error_per_iter, all_errors_per_iter, all_errors_pct_per_iter) = resolve_layer(available_packs[:many_packs], ordering, n_iter, n_chromosomes, elite, p_cross, p_mut, p_t) ### (error, packs) for each iteration
            end_time = datetime.datetime.now()
            print('done. resolved layer {} at time {}'.format(count, end_time))
            packs_per_layer.append({iteration: result[0] for iteration, result in iteration_result.items()}) # best packs for each iteration 
            error_per_layer.append(all_errors_per_iter) 
            error_per_layer_pct.append(all_errors_pct_per_iter)
            average_error_per_layer.append(average_error_per_iter)
            best_error_per_layer.append(best_error)
            time_per_layer.append((end_time-start_time_genetic).seconds)
            last_used = len(best_used)
            used = best_used
            error = best_error
        else:
            packs_per_layer.append(packs_used)
            ids_used = [x.rid for x in packs_used]
            heights = [x.z for x in available_packs if x.pack_id in ids_used]
            total_error = compute_error_sigma(packs_used, available_packs) + 2*max(heights)
            error_per_layer.append(str(total_error))
            error_per_layer_pct.append(str(total_error/len(packs_used)))
            time_per_layer.append(str((start_time_genetic-start_time_try).seconds))
            last_used = len(packs_used)
            used = packs_used
            error = total_error

        available_packs = available_packs[last_used:]
        print('Packs used in layer {}: {}'.format(count, len(used)))
        print('Error in layer {} ----> {}'.format(count, error))

        if count % 2 == 0:
            if use_genetic:
               dump_results(count -2, count, packs_per_layer[count-2:count], best_error_per_layer[count-2:count], error_per_layer[count-2:count],error_per_layer_pct[count-2:count],average_error_per_layer[count-2:count], time_per_layer[count-2:count])
            else: 
                dump_results_simple(count-2, count, packs_per_layer[count-2:count], error_per_layer[count-2:count], error_per_layer_pct[count-2:count], time_per_layer[count-2:count])
        count +=1

    if use_genetic:
        dump_results(0, count-1, packs_per_layer, best_error_per_layer, error_per_layer, error_per_layer_pct, average_error_per_layer,time_per_layer)
    else:
        dump_results_simple(0, count-1, packs_per_layer, error_per_layer, error_per_layer_pct, time_per_layer)
    print('Done at {}'.format(datetime.datetime.now()))
    return packs_per_layer