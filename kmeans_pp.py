
import sys
import pandas as pd
import numpy as np
import math
import os
import mykmeanssp

def main():
    try:
        k = int(sys.argv[1])
    except:
        printInvalidInput()

    numOfArgs = len(sys.argv)

    if numOfArgs == 5:
        max_iter = 300
        eps = float(sys.argv[2])
        file_name_1 = sys.argv[3]
        file_name_2 = sys.argv[4]
    elif numOfArgs == 6:
        try:
            max_iter = int(sys.argv[2])
        except:
            printInvalidInput()
        eps = float(sys.argv[3])
        file_name_1 = sys.argv[4]
        file_name_2 = sys.argv[5]
    else:
        printInvalidInput()
    try:
        vectors1 = pd.read_csv(file_name_1, header = None)
        vectors2 = pd.read_csv(file_name_2, header = None)
        vectors = pd.merge(vectors1, vectors2, on = 0)
        vectors.sort_values(by = 0, inplace = True)
        # defines index collom to be intependant
        vectorsIndices = list(vectors.loc[:,0])
        vectors.set_index(0, inplace = True)
        vectors = vectors.to_numpy()
    except:
        print("here")
        printInvalidInput()

    numOfVec = vectors.shape[0]
    # checking values validity
    validity(k, numOfVec, max_iter)

    centroidsIndices, centroids = initializeCentroids(k, vectors, numOfVec, vectorsIndices)

    dim = len(vectors[0])
    
    # writing vectors, centroids to files for c code to read from 
    np.savetxt("vectorsFile", X = vectors.tolist(), fmt = '%.4f', delimiter=',', newline='\n')
    np.savetxt("centroidsFile", X = centroids, fmt = '%.4f', delimiter=',', newline='\n')

    outputFileName = mykmeanssp.fit(k, numOfVec, dim, max_iter, eps, "vectorsFile", "centroidsFile")
    
    # 1 row print
    print(",".join(str(vIndex) for vIndex in centroidsIndices))
    # 2 row print
    # reads file accepted from c 
    finalCentroids = pd.read_csv(outputFileName, header = None).to_numpy().tolist()
    for i in range(k):
        print(",".join(str(coordinate) for coordinate in finalCentroids[i]))
    # print empty row
    print("")


    # delete files 
    os.remove("vectorsFile")
    os.remove("centroidsFile")
    os.remove("outputFileName")
    
def initializeCentroids(k, vectors, numOfVec, vectorsIndices):
    np.random.seed(0)
    centroidsIndices = []
    centroids = []
    addToCentroids(vectorsIndices, numOfVec, centroidsIndices, centroids, vectors, None)
    i = 1
    while i < k:
        minDistances = []
        prob = []
        sumOfD = 0
        # loop over all vectors
        for l in range(numOfVec):
            Dl = sys.float_info.max
            # for each vector, find min distance by checking with all possible centroids
            for j in range(i):
                Dl  = min(Dl, Distance(vectors[l], centroids[j]))
            minDistances.append(Dl)
            sumOfD += Dl 
        # cala p for each vector  
        for l in range(numOfVec):
            p = minDistances[l]/sumOfD
            prob.append(p)
        i +=1
        addToCentroids(vectorsIndices, numOfVec, centroidsIndices, centroids, vectors, prob)
    return centroidsIndices, centroids

def addToCentroids(vectorsIndices, numOfVec, centroidsIndices, centroids, vectors, prob):
    randIndex = np.random.choice(numOfVec, p = prob)
    realIndex = vectorsIndices[randIndex]
    centroidsIndices.append(int(realIndex))
    centroids.append(list(vectors[randIndex]))

def printInvalidInput():
    print("Invalid Input!")
    sys.exit(1)

def validity(k, n, max_iter):
    if k <= 1 or k >= n:
        printInvalidInput()
    if (k % 1) != 0:
        printInvalidInput()
    if n <= 0:
        printInvalidInput()
    if (max_iter % 1) != 0:
        printInvalidInput()
    if max_iter <= 0:
        printInvalidInput()


def Distance(x,y):
    sumOfSquaredDiffrence = 0
    for i in range(len(x)):
        sumOfSquaredDiffrence += math.pow(float(x[i])-float(y[i]),2)
    return sumOfSquaredDiffrence

main()