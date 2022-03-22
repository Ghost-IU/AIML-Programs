"""

K-Nearest Neighbors

"""

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets

#Load Data
iris = datasets.load_iris()
print("Iris datatset is loaded....")

#Variables for training and Testing
x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.1)
print(f"Size of training data and label: {x_train.shape}, {y_train.shape}")
print(f"Size of testing data and label: {x_test.shape}, {y_test.shape}")

#Print the labels
for i in range(len(iris.target_names)):
    print(f"Label {i} : {iris.target_names[i]}")

#Classifier
classifier = KNeighborsClassifier(n_neighbors=1)

#Training
classifier.fit(x_train,y_train)
#Testing
y_pred = classifier.predict(x_test)

for i in range(0,len(x_test)):
    print(f"Sample: {x_test[i]}, Actual Label: {y_test[i]}, Predicted Label: {y_pred[i]} ")

#Accuracy
print(f"Classifier accuracy: {classifier.score(x_test,y_test)}")
