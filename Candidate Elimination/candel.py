"""

Candidate Elimination Algorithm


"""

import csv

def get_domains(examples):
    d = [set() for i in examples[0]]
    
    for x in examples:
        for i, xi in enumerate(x):
            d[i].add(xi)
    
    return [list(sorted(x)) for x in d]

def more_general(h1, h2):
    more_general_part = []
    
    for x, y in zip(h1, h2):
        mg = x == "?" or (x!="0" and (x==y or y== "0"))
        more_general_part.append(mg)
        
    return all(more_general_part)


def fulfills(example,hypo):
    return more_general(hypo, example)


def min_general(h,x):
    h_new = list(h)
    
    for i in range(len(h)):
        if not fulfills(x[i:i+1], h[i:i+1]):
            h_new[i] = "?" if h[i]!="0" else x[i]
    
    return [tuple(h_new)]


def min_specialize(h, domains, x):
    results = []
    
    for i in range(len(h)):
        if h[i] == "?":
            for val in domains[i]:
                if x[i] != val:
                    h_new = h[:i] + (val,) + h[i+1:]
                    results.append(h_new)
                
        elif h[i] != "0":
            h_new = h[:i] + ("0",) + h[i+1:]
            results.append(h_new)
    
    return results


def generalize_S(x, G, S):
    Sprev = list(S)
    
    for s in Sprev:
        if s not in S:
            continue
        
        if not fulfills(x, s):
            
            S.remove(s)
            Splus = min_general(s, x)
            
            S.update([h for h in Splus if any([more_general(g,h) for g in G])])
            S.difference_update([h for h in S if any([more_general(h, h1) for h1 in S if h1!= h])])
    
    return S


def specialize_G(x, domain, G, S):
    Gprev = list(G)
    
    for g in Gprev:
        if g not in G:
            continue
        if fulfills(x, g):
            
            G.remove(g)
            Gminus = min_specialize(g, domain, x)

            G.update([h for h in Gminus if any([more_general(h,s) for s in S])])
            G.difference_update([h for h in G if any([more_general(g1, h) for g1 in G if g1!=h])])

    return G

def candidate_elimination(examples):
    domains = get_domains(examples)[:-1]
    
    n = len(domains)
    G = set([("?",)*n])
    S = set([("0",)*n])
    
    print(f"\nG0: {str(G)} \nS0: {str(S)} \n")
    
    i = 0
    for xcx in examples:
        i = i+1
        x, cx = xcx[:-1], xcx[-1]
        
        if cx == "Y":
            G = {g for g in G if fulfills(x,g)}
            S = generalize_S(x, G,S)
        else:
            S = {s for s in S if not fulfills(x,s)}
            G = specialize_G(x, domains, G, S)
        
        print(f"G{i}: {str(G)} \nS{i}: {str(S)}")
    
    return 


with open("sports.csv") as csvfile:
    examples = [tuple(lines) for lines in csv.reader(csvfile)]
    
candidate_elimination(examples)

