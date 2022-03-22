"""

Backpropagation

"""


import numpy as np

#Define dataset
X = np.array(([2,8],[4,6],[3,2]), dtype= float) 
y = np.array(([89],[67],[88]), dtype = float)

#Normalize
X = X/(np.amax(X, axis=0))
y = y/100

def sigmoid(x):
    return 1/(1 + np.exp(-x))

def sigmoid_grad(x):
    return x*(1-x)

epoch = 1000
eta = 0.2
hidden_neurons = 3
input_neurons = 2
output_neurons = 1

wh = np.random.uniform(size=(input_neurons,hidden_neurons)) #2x3
bh = np.random.uniform(size=(1,hidden_neurons)) #1x3
wout = np.random.uniform(size=(hidden_neurons,output_neurons)) #3x1
bout = np.random.uniform(size=(1,output_neurons)) #1x1

for i in range(epoch):
    #Forward propagation
    #Input layer
    h_ip = np.dot(X,wh) + bh
    h_act = sigmoid(h_ip)
    #Output Layer
    o_ip = np.dot(h_act,wout) + bout
    output = sigmoid(o_ip)
    
    #Error at output
    Eo = y - output
    outgrad = sigmoid_grad(output)
    d_output = Eo * outgrad
    
    #Error at hidden layer
    Eh = d_output.dot(wout.T)
    hiddengrad = sigmoid_grad(h_act)
    d_hidden = Eh * hiddengrad
    #Update the weights
    wout += h_act.T.dot(d_output) * eta
    wh += X.T.dot(d_hidden) * eta
    
print(f"Normalized: {X} \n Actual: {y} \n Predicted: {output}")
