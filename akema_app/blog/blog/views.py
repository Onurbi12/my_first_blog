from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse

import re
import io

from io import BytesIO
import base64
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def graphic(request):
##### Style des différents graphiques ######
    sns.set(style='whitegrid', palette='deep')
    sns.set_context("paper")

##### Import des données à partir d'un fichier ods (libre office) #####
    df = pd.read_csv('blog/data/donnée_tracking.csv')
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
    ax.set(xlim=(-30,30), ylim = (-15, 25))

    circle1 = plt.Circle((0, 0),rayon[1], fill=True)
    circle2 = plt.Circle((0, 20),rayon[0], fill=True)
    ax.add_artist(circle1)
    ax.add_artist(circle2)


##### Aucune idée de ce que ca fait mais ca affiche sur le template ...
##### peut etre pas la mailleure solution !
    #canvas=FigureCanvas(fig)
    buffer = io.BytesIO()
    plt.savefig(buffer, transparent=True, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    plt.close(fig)
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'blog/testGraph.html',{'graphic':graphic})
