import matplotlib.pyplot as p
from sklearn.cluster import KMeans
from sklearn import datasets
import numpy as np 

# take data from iris and plot the inertia's
iris = datasets.load_iris()
observations = iris.data
inertias = []
for i in range(1, 11):
    k_means = KMeans(n_clusters = i, init = "k-means++", random_state = 0)
    k_means.fit(observations)    # Compute k_means clustering
    inertia = k_means.inertia_
    inertias.append(inertia)

# build the chart
p.plot(range(1, 11), inertias)
p.title('Elbow Method for selection of optimal "K" clusters', fontsize = 14, weight = 'bold' ,color = "brown")
p.xlabel("K")
p.ylabel("Average Dispersion")
# adds the arrow and title elbow
# xy = arrowHead
p.annotate('Elbow Point', xy = (3.2, 155), xytext = (4.2, 250), arrowprops = dict(arrowstyle = '->', ls = "--"))
# circles the elbow 
# o = circle, s = size
p.scatter(x = 2.5, y = 115, marker = 'o', s = 2600, facecolors = 'none', edgecolors = 'k', ls = "--")
p.savefig("elbow.png")