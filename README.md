# Packaging Santa's Sleigh
## Requirements
* installare conda https://conda.io/projects/conda/en/latest/user-guide/install/index.html
* creazione environment virtuale con: `conda create --name decision-models`
* attivazione environment: `conda activate decision-models`
* installazione pip: ` conda install pip `
*  navigazione alla root del progetto `cd ..\Gruppo 3\santas_sleigh`
* installazione librerie necessarie `pip install -r requirements.txt`
* navigazione nella root di rectpack `cd rectpack_modified`
* installazione rectpack `python setup.py install`
* navigazione alla root del progetto `cd ..`
* pulizia della console `cls()`

* modifica dei parametri di controllo dell'algoritmo aprendo il file main.py. Di default:
	- filepath = presents.csv
	- packs_number = None (si utilizzano tutti i pacchi presenti nel file)
	- use_genetic = True (si utilizza l'algoritmo genetico)
	- ordering = id (variante -> area)
	- n_iter = 3 (tre iterazioni per l'algoritmo genetico)
	- n_chromosomes = 20
	- elite = 5 (numero di cromosomi che passa direttamente alla generazione successiva)
	- p_cross = 0.5 (probabilità di crossover)
	- p_mut = 0.3 (probabilità di mutazione)
	- p_sel = 0.5 (probabilità di selezione)

* start dello script (da root progetto) con `python main.py`

* eliminazione dell'environment `conda env remove -n decision-models`