"""

Locally Weighted Regression

"""

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

#Define Kernel Function for weights calculation
def kernel(point,xmat,k):
    m,n = np.shape(xmat) #m,n=rows,colums
    weights = np.mat(np.eye(m)) #initialize weights to identity matrix
    for i in range(m):
        diff = point - X[i] #calculate diff for each point in X
        weights[i,i] = np.exp(diff*diff.T/(-2*k**2)) #weights for each instance
    return weights

#Calculation of localWeight
def localWeight(point, xmat, ymat, k):
    wei = kernel(point, xmat, k) 
    W = (X.T*(wei*X)).I * (X.T*(wei*ymat.T))
    return W

#Regression func
def localWeightRegression(xmat,ymat,k):
    m,n = np.shape(xmat) #Take the shape
    ypred = np.zeros(m) #Initialize to a matrix of zeros 
    for j in range(m):
        ypred[j] = xmat[j] * localWeight(xmat[j], xmat, ymat, k) 
    return ypred

#Plot the graph
def graphPlot(X,ypred,k):
    sortindex = X[:,1].argsort(0) #Sort the 1st column from index 0
    xsort = X[sortindex][:,0] #Respective sorted index value against col 0
    fig = plt.figure() #Instance of figure
    ax = fig.add_subplot(1,1,1) #Single plot object
    ax.scatter(bill,tip,color="red") #Scatterplot
    ax.plot(xsort[:,1],ypred[sortindex],color="green",linewidth=5) #Lineplot
    plt.title(f"Regression when k: {k}") #Title of graph
    plt.xlabel("Total Bill")
    plt.ylabel("Tip")
    plt.show()
    
#Take data from csv file, using pandas
data = pd.read_csv("tips.csv")
bill = np.array(data.total_bill) 
tip = np.array(data.tip)

#Conver the arrayed data into 2D matrix 
mbill = np.mat(bill)
mtip = np.mat(tip)
m = np.shape(mbill)[1] #Take the column 1 length 
ones = np.mat(np.ones(m)) #Initialize ones to matrix of Ones
X = np.hstack((ones.T,mbill.T)) #Stack the arrays horizontally in squence 

k = 9 #Specify smoothening parameter
ypred = localWeightRegression(X, mtip, k) 
graphPlot(X, ypred, k)
