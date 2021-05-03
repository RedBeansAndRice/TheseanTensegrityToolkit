import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit
import Genomics
import houdiniExpressionizer as hE

subfolder = ""
results = os.getcwd() +"/results/" + subfolder
graphs = results +"/graphs/"

globalPredicTime = 0


def func(x, a, b, c):
    return a * np.exp(-b * x) + c


def getfitnessfiles():
    fitnessfiles = []
    files = os.listdir(results)
    for i in files:
        if "fitnessValues" in i:
            fitnessfiles.append(i)
    return fitnessfiles


def getlineagetrees():
    lineagetrees = []
    files = os.listdir(results)
    for i in files:
        if "LineageTree" in i:
           lineagetrees.append(i)
    return lineagetrees

def lineageClassify(lineageId):
    if (lineageId == 0):
        return lineageId
    if (lineageId < 5):
        return 1
    if (lineageId == 5):
        return 2
    if (lineageId < 10):
        return 3
    if (lineageId == 10):
        return 4
    if (lineageId < 15):
        return 5
    return 6  

def lineageClassify2(lineageId):
    if (lineageId == 0):
        return "a"
    if (lineageId < 5):
        return "b"
    if (lineageId == 5):
        return "c"
    if (lineageId < 10):
        return "d"
    if (lineageId == 10):
        return "e"
    if (lineageId < 15):
        return "f"
    return "g"  

def lineageClassifier(lineageTree):
    classifiedTree = lineageTree.copy()
    for i in range(0, lineageTree.shape[0]):
        classifiedTree[0][i]=lineageClassify(lineageTree[0][i])
        classifiedTree[1][i] = lineageClassify(lineageTree[1][i])
    return classifiedTree

def genStructureSort(scores):
    if(len(scores.columns)<12):
        return 0
    else:
        return 1

def commaCleaner(data):
    data = data.drop(columns = data.columns[-1])
    return data

def columnCleaner(scores):
    if(not genStructureSort(scores)):
        scores.rename(columns = {0:"Parent"}, inplace = True)
        scores = commaCleaner(scores)
        return scores
    else:
        scores.rename(columns = {0:"Parent One", 5: "Parent Two", 10: "Seeded Approximate Policy"}, inplace = True)
        scores = commaCleaner(scores)
        return scores


def lineFitter(unfit, filename, predicTime):
    if predicTime == 0: predicTime = unfit.shape[0]

    pseudodata = np.linspace(0,unfit.shape[0]-1,unfit.shape[0])
    model = LinearRegression().fit(pseudodata.reshape(-1, 1),unfit.to_numpy())

    r_sq = model.score(pseudodata.reshape(-1, 1),unfit.to_numpy())
    intercept = model.intercept_
    coef = model.coef_
    print(intercept)
    print(coef)
    pseudopredicdata = np.linspace(1,predicTime-1,predicTime)
    predictedscores = model.predict(pseudopredicdata.reshape(-1, 1))
    plt.plot( predictedscores, label = "Linear Regression of " + filename)

    
def curveFitter(unfit, filename, predicTime):
    if predicTime == 0: predicTime = unfit.shape[0]

    pseudodata = np.linspace(0,unfit.shape[0]-1,unfit.shape[0])

    pseudopredicdata = np.linspace(0,predicTime-1,predicTime)

    popt, pcov = curve_fit(func, pseudodata, unfit, maxfev = 5000)
    plt.plot( pseudopredicdata, func(pseudopredicdata, *popt), label = "Curve Regression of " + filename)




def quickgraphs(fitnessfiles):
    for i in fitnessfiles:
        scores = pd.read_csv(results + i, header = None)
        
        scores = columnCleaner(scores)
        scores.plot()
        plt.show()

def quicklineagegraphs(lineagetrees):
    for i in lineagetrees:
        scores = pd.read_csv(results + i, header = None)
        scores.plot()
        plt.show()

def quickclassifiedlineagegraphs(lineagetrees, autosave = False):
    for i in lineagetrees:
        scores = pd.read_csv(results + i, header = None)
        scores = commaCleaner(scores)
        newscores = lineageClassifier(scores)
        newscores.plot(kind = "bar")

        plt.title(i)

        if(autosave):
            plt.savefig(graphs + i +".png")
        plt.show()

def parentvavoffspringaverage(fitnessfiles, predicTime, showallseedlings = False, curvefit = True, linefit = True):
    if (showallseedlings):
        for i in fitnessfiles:
            scores = pd.read_csv(results + i, header = None)
            scores = columnCleaner(scores)
            if(genStructureSort(scores)):
                kinofkhan = scores[[1,2,3,4]]
                kinofminikhan = scores[[6,7,8,9]]
                sonsofadam = scores[[11,12,13,14]]
                johnnycomelatelys = scores[[15,16,17,18,19]]

                plt.plot(scores["Parent One"], label = "Parent One")
                plt.plot(scores["Parent Two"], label = "Parent Two")
                plt.plot(scores["Seeded Approximate Policy"], label = "Seeded Approximate Policy")
                plt.plot(kinofkhan.mean(axis=1), label = "average Parent One lineage fitness")
                plt.plot(kinofminikhan.mean(axis=1), label = "average Parent Two lineage fitness")
                plt.plot(johnnycomelatelys.mean(axis=1), label = "average approximate policy lineage fitness")
                plt.plot(johnnycomelatelys.mean(axis=1), label = "average randomly seeded individual fitness")

                if(curvefit):
                    curveFitter(scores["Parent One"], "Parent One", predicTime)
                    curveFitter(scores["Parent Two"], "Parent Two", predicTime)
                    curveFitter(kinofkhan.mean(axis=1), "average Parent One lineage", predicTime)
                    curveFitter(kinofminikhan.mean(axis=1), "average Parent Two lineage", predicTime)
                    curveFitter(sonsofadam.mean(axis=1), "average approximate policy lineage", predicTime)
                    curveFitter(johnnycomelatelys.mean(axis=1), "average randomly seeded individual", predicTime)

                
                if (linefit):
                    lineFitter(scores["Parent One"], "Parent One", predicTime)
                    lineFitter(scores["Parent Two"], "Parent Two", predicTime)
                    lineFitter(kinofkhan.mean(axis=1), "average Parent One lineage", predicTime)
                    lineFitter(kinofminikhan.mean(axis=1), "average Parent Two lineage", predicTime)
                    lineFitter(sonsofadam.mean(axis=1), "average approximate policy lineage", predicTime)
                    lineFitter(johnnycomelatelys.mean(axis=1), "average randomly seeded individual", predicTime)

                plt.title(i)
                plt.legend(loc = 'best')
                plt.show()
            else:
                kinofkhan = scores[[1,2,3,4]]
                johnnycomelatelys = scores[[5,6,7,8,9]]
                plt.plot(scores["Parent"], label = "Parent")
                plt.plot(kinofkhan.mean(axis=1), label = "average selected lineage fitness")
                plt.plot(johnnycomelatelys.mean(axis=1), label = "average randomly seeded individual fitness")

                if(curvefit):
                    curveFitter(scores["Parent"], "Parent", predicTime)
                    curveFitter(kinofkhan.mean(axis=1), "average selected lineage", predicTime)
                    curveFitter(johnnycomelatelys.mean(axis=1), "average randomly seeded individual", predicTime)

                
                if (linefit):
                    lineFitter(scores["Parent"], "Parent", predicTime)
                    lineFitter(kinofkhan.mean(axis=1), "average selected lineage", predicTime)
                    lineFitter(johnnycomelatelys.mean(axis=1), "average randomly seeded individual", predicTime)

                plt.title(i)
                plt.legend(loc = 'best')
                plt.show()



def lineagegraphs(fitnessfiles):
    for i in fitnessfiles:
        scores = pd.read_csv(results + i, header = None)
        scores.rename(columns = {0:"Parent"}, inplace = True)
        scores = scores.drop(columns = scores.columns[-1])
        kinofkhan = scores[[1,2,3,4]]
        johnnycomelatelys = scores[[5,6,7,8,9]]

        plt.plot("Parent", label = i, data = scores)
        plt.plot(kinofkhan.mean(axis=1), label = i + "average selected lineage fitness")
        plt.plot(johnnycomelatelys.mean(axis=1), label = i + "average seeded individual fitness")
        lineFitter(scores["Parent"],i)
        curveFitter(scores["Parent"],i)
        lineFitter(kinofkhan.mean(axis=1), i + "average selected lineage fitness")
        lineFitter(johnnycomelatelys.mean(axis=1), i + "average seeded individual fitness")
        plt.legend(loc = 'best')
        plt.show()



quickclassifiedlineagegraphs(getlineagetrees(), True)