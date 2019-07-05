import pandas as pd
from resolve import * 

###
# Algorithm entrypoint. It basically loads the dataset, sort it by PresentId in descendng order, then calls the resolve function.
###
def start(filepath, packs_number=50000, use_genetic=False, ordering='id', n_iter=2, n_chromosomes = 3, elite = 1, p_cross = 0.6, p_mut = 0.3, p_sel = 0.5):
    print('Launch algorithm with: \n  packs_number={}, use_genetic={}, ordering={}, \n  n_iter={}, n_chromosomes={}, elite={}, \n  pCross={}, pMut={}, pSel={}'.format(packs_number,use_genetic, ordering, n_iter, n_chromosomes , elite , p_cross , p_mut , p_sel))
    print('Loading data from {}'.format(filepath))
    presents = pd.read_csv(filepath)
    presents_ordered = presents.sort_values(by='PresentId', ascending=False)
    if packs_number is not None:
         presents_ordered = presents_ordered[:packs_number]
    resolve(presents_ordered, use_genetic, ordering, n_iter, n_chromosomes, elite, p_cross, p_mut, p_sel)

if __name__ == '__main__':
    start('../presents.csv')

