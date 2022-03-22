# -*- coding: utf-8 -*-
"""

ID3 Algorithm

"""

import math, csv


def loadCsv(filename):
    lines = csv.reader(open(filename,"r"))
    dataset = list(lines)
    headers = dataset.pop(0)
    return dataset , headers


class Node:
    
    def __init__(self,attribute):
        self.attribute = attribute
        self.children = []
        self.answer = ""
     
        
def subtable(col,data,delete):
    dic = {}
    coldata = [ row[col] for row in data]
    attr = list(set(coldata))
    
    for k in attr:
        dic[k] = []
        
    for y in range(len(data)):
        key = data[y][col]
        if delete:
            del data[y][col]
        dic[key].append(data[y])
        
    return attr, dic


def entropy(S):
    attr = list(set(S))
    if len(attr) == 1:
        return 0
    
    count = [0,0]
    for i in range(2):
        count[i] = sum([1 for x in S if attr[i] == x] )/ (len(S) * 1.0)
        
    sums = 0
    for cnt in count:
        sums += -1 * cnt * math.log(cnt,2)
        
    return sums


def compute_gain(col, data):
    
    attValues, dic = subtable(col, data, delete=False)
    
    total_entropy = entropy([row[-1] for row in data])
    for x in range(len(attValues)):
        ratio = len(dic[attValues[x]])/(len(data)*1.0)
        entro = entropy([row[-1] for row in dic[attValues[x]]])
        total_entropy -= ratio * entro
    return total_entropy


def build_tree(data, features):
    
    lastcol = [row[-1] for row in data]
    if len(set(lastcol)) == 1:
        node = Node("")
        node.answer = lastcol[0]
        return node
    
    n = len(data[0]) - 1
    gains = [compute_gain(col, data) for col in range(n)]
    
    split = gains.index(max(gains))
    node = Node(features[split])
    fea = features[:split]+features[split+1:]
    
    attr, dic = subtable(split, data, delete=True)
    for x in range(len(attr)):
        child = build_tree(dic[attr[x]],fea)
        node.children.append((attr[x],child))
    
    return node
        
        
def print_tree(node,level):
    if node.answer != "":
        print("    "*level, node.answer)
        return
    
    print("    "*level,node.attribute)
    for value, n in node.children:
        print("    "*(level+1), value)
        print_tree(n,level+2)
        
        
def classify(node, x_test, features):
    
    if node.answer != "":
        print(node.answer)
        return 
    
    pos = features.index(node.attribute)
    for value, n in node.children:
        if x_test[pos] == value:
            classify(n, x_test, features)
    

dataset, features = loadCsv("tennis.csv")
node = build_tree(dataset, features)

print("The DT using ID3 algoritm is :")
print_tree(node, 0)

testdata, features = loadCsv("test.csv")
for xtest in testdata:
    print(f"The test instance : {xtest}")
    print("Predicted label: ",end="")
    classify(node,xtest,features)
    
