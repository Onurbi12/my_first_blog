import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from collections import Counter


##### Style des différents graphiques ######
sns.set(style='whitegrid', palette='deep')
sns.set_context("paper")

##### Import des données à partir d'un fichier ods (libre office) #####
df = pd.read_csv('/home/kat/Documents/Python/Bruno_project/project/blog/data/donnée_tracking.csv')

#### permet de compter les occurrences et d'ajouter le nombre de cliques correspondant
link = df.groupby(["lien cliquer"], as_index=False).sum()
nbr_click=link["total clique"]


##### ajoute tous les nombre de la colone nombre de cliques pour les %
tot=sum(nbr_click)

##### calcul le pourcentage de cliques et divise par 2 pour avoir le rayon
rayon = (nbr_click *100/tot)/2


##### afficher le graphique
fig = plt.figure()
ax = fig.add_subplot(111)
ax.axis('off')
ax.axis('scaled')
ax.set(xlim=(-50,50), ylim = (-50, 50))

circle1 = plt.Circle((0, 0),rayon[1], fill=True)
circle2 = plt.Circle((0, 20),rayon[0], fill=True)
ax.add_artist(circle1)
ax.add_artist(circle2)

plt.show()
