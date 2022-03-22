"""

K-Means (EM Algo)

"""
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

#Import and classify the data
iris = datasets.load_iris()
X = pd.DataFrame(iris.data)
X.columns = ['Sepal_Length','Sepal_Width','Petal_Length','Petal_Width'] 
y = pd.DataFrame(iris.target)
y.columns = ['Targets']
 
#Create KMeans Model
model = KMeans(n_clusters=3)
model.fit(X)

#Plot Graph
plt.figure(figsize=(14,14))
colormap = np.array(['red','lime','black'])

#Graph for actual data
plt.subplot(2,2,1)
plt.scatter(X.Petal_Length, X.Petal_Width, c= colormap[y.Targets], s= 40)
plt.title("Real Clusters")
plt.xlabel("Peatal Length")
plt.ylabel("Petal Width")

#Graph for K-Means
plt.subplot(2,2,2)
plt.scatter(X.Petal_Length, X.Petal_Width, c= colormap[model.labels_], s= 40)
plt.title("Real Clusters")
plt.xlabel("Peatal Length")
plt.ylabel("Petal Width")

#For EM Algorithm
#Meand & SD
from sklearn import preprocessing
scaler = preprocessing.StandardScaler()
scaler.fit(X)
xsa = scaler.transform(X)
xs = pd.DataFrame(xsa, columns= X.columns)

#Gaussian Mixtures
from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(n_components=3)
gmm.fit(xs)
g_pred = gmm.predict(xs)

#Plot for EM clusters
plt.subplot(2,2,3)
plt.scatter(X.Petal_Length, X.Petal_Width, c= colormap[g_pred], s= 40)
plt.title("Real Clusters")
plt.xlabel("Peatal Length")
plt.ylabel("Petal Width")

print("It is observed that Gaussian based EM Cluster is closely related to Real cluster than K-Means Cluster")