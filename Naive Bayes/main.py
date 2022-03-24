"""

Naive Bayes algorithm

"""
import math, csv, random
import statistics as st

def loadCsv(filename):
    lines = csv.reader(open(filename, "r"))
    dataset = list(lines)
    for i in range(len(dataset)):
        dataset[i]= [float(x) for x in dataset[i]]
    return dataset

def splitDataset(dataset, splitratio):
    testSize = int(len(dataset)*splitratio)
    testSet = []
    trainSet = list(dataset)
    
    while len(testSet) < testSize:
        index = random.randrange(len(trainSet))
        testSet.append(trainSet.pop(index))
        
    return [trainSet, testSet]

def seperateByClass(dataset):
    seperated = {}
    
    for i in range(len(dataset)):
        x = dataset[i]
        if (x[-1] not in seperated):
            seperated[x[-1]] = []
        seperated[x[-1]].append(x)
    
    return seperated


def compute_mean_std(dataset):
    mean_std = [ (st.mean(attribute) , st.stdev(attribute)) for attribute in zip(*dataset)]
    del mean_std[-1]
    return mean_std

def summarizeByClass(dataset):
    summary = {}
    seperated = seperateByClass(dataset)
    
    for classValue, instance in seperated.items():
        summary[classValue] = compute_mean_std(instance)
        
    return summary

def estimateProbability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
    return (1/(math.sqrt(2*math.pi)* stdev)) * exponent

def calcClassProbability(summaries, testVector):
    p = {}
    for classValue, classSummary in summaries.items():
        p[classValue] = 1
        for i in range(len(classSummary)):
            mean, stdev = classSummary[i]
            x= testVector[i]
            p[classValue] *= estimateProbability(x, mean, stdev)
    return p

def predict(summaries, testVector):
    all_p = calcClassProbability(summaries, testVector)
    bestLabel, bestProb = None, -1
    
    for lbl, p in all_p.items():
        if bestLabel == None or p > bestProb:
            bestLabel = lbl
            bestProb = p
            
    return bestLabel

def perform_classification(summaries, testSet):
    predictions = []
    for i in range(len(testSet)):
        result = predict(summaries, testSet[i])
        predictions.append(result)
        
    return predictions

def getAccuracy(predictions, testSet):
    correct = 0
    
    for i in range(len(testSet)):
        if testSet[i][-1] == predictions[i]:
            correct += 1
            
    return (correct/float(len(testSet)))*100

dataset = loadCsv("pima.csv")
print("Pima Indian Diabetes dataset is loaded ....")
print(f"Total instances in dataset: {len(dataset)}")
print(f"No. of attributes : {len(dataset[0])-1}")

splitratio = 0.2
trainingSet, testSet = splitDataset(dataset, splitratio)
print("Dataset is split into Training and Testing....")
print(f"Total instance is training: {len(trainingSet)} \n Total instance in Testing: {len(testSet)}")

summaries = summarizeByClass(trainingSet)
predictions = perform_classification(summaries, testSet)

accuracy = getAccuracy(predictions, testSet)
print(f"The accuracy of the model is : {accuracy}")
