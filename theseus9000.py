import os
import csv
import time
import Genomics
import houdiniExpressionizer as hE
import ast

from datetime import datetime

pSize = 20
minGenome = 2
maxGenome = 24
minPPairs = 1
maxPPairs = 8

generations = 200

maxDs = 8
maxAs = 8
maxMs = 8
crash = 0
crashGen = 0

evalFrame = '100'

adam = [["@legsPrimErrorRank", "==", "1", "||", "@flatPrimErrorRank", "==", "1", "&&", "1", "*", "(-20)"], [0,6,0,8]]

toolkitPath = os.getcwd() 

hrenderPath = '"C:\\Program Files\\Side Effects Software\\Houdini 18.5.499\\bin\\hrender.py"'

command = 'hython ' + hrenderPath + ' '+ toolkitPath + '\\TesterTesnegrities.hipnc -d mantra_ipr -F ' + evalFrame + ' -I'

def printlineage(genghybirthsteppe, minigenghybirthsteppe):
    with file(toolkitPath + "\\LineageTree.csv", "a") as f:
        f.write("%s,%s,\n" % (genghybirthsteppe, minigenghybirthsteppe))
        f.close()


def min2(ranks):
    copy = list(ranks)
    copy.remove(min(copy, key = float))
    return min(copy, key = float)

def mindex2(ranks):
    return [i for i, n in enumerate(ranks) if n == min(ranks, key = float)][1]

if crash == 0:

    #initialize population
    initPop = Genomics.initializePopulation(pSize, minGenome, maxGenome, minPPairs, maxPPairs)

    ranks = []

    with file(toolkitPath + "\\Tensegrigene.csv", "a") as f:
        f.write("%s" % initPop)
        f.write(",\n")
        f.close()


    for individual in initPop:
        hE.expressionize(Genomics.genomeToString(individual))
        os.system("%s" % command)
        print("done")

    with open(toolkitPath + '\\fitnessValues.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            ranks = row
        f.close()

    ranks = ranks[:-1]
    print(ranks)
    genghy = initPop[ranks.index(min(ranks, key = float))]

    print("Best score:" + str(min(ranks, key = float)))
    print("Best score index:" + str(ranks.index(min(ranks, key = float))))
        
    print("Second Best score:" + str(min2(ranks)))

    if (min(ranks, key = float) == min2(ranks)):
        minigenghy = initPop[mindex2(ranks)]
        print("Second Best score index:" + str(mindex2(ranks)))
        printlineage( str(ranks.index(min(ranks, key = float))), str(mindex2(ranks)))
    else:
        minigenghy = initPop[ranks.index(min2(ranks))]
        print("Second Best score index:" + str(ranks.index(min2(ranks))))
        printlineage(str(ranks.index(min(ranks, key = float))), str(ranks.index(min2(ranks))))

    print(genghy)
    print(minigenghy)

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Time Of Completion =", current_time)

    genNum = 1

    for gen in range(0,generations):


        with file(toolkitPath + "\\FitnessValues.csv", "a") as f:
            f.write("\n")
            f.close()

        newBrood = Genomics.genghify3(genghy,minigenghy, adam, pSize/4,pSize/4, minGenome, maxGenome, minPPairs, maxPPairs, maxDs, maxAs, maxMs)
        ranks = []

        with file(toolkitPath + "\\Tensegrigene.csv", "a") as f:
            f.write("%s" % newBrood)
            f.write(",\n")
            f.close()


        for individual in newBrood:
            hE.expressionize(Genomics.genomeToString(individual))
            os.system("%s" % command)        
            print("done")
        
        with open(toolkitPath + '\\fitnessValues.csv') as f:
            reader = csv.reader(f)
            i= 0
            for row in reader:
                if (i==genNum):
                    ranks = row
                i += 1
            f.close()
        print(genNum)
        genNum += 1

        ranks = ranks[:-1]

        print(ranks)

        genghy = newBrood[ranks.index(min(ranks, key = float))]

        print("Best score:" + str(min(ranks, key = float)))
        print("Best score index:" + str(ranks.index(min(ranks, key = float))))
            
        print("Second Best score:" + str(min2(ranks)))

        if (min(ranks, key = float) == min2(ranks)):
            minigenghy = newBrood[mindex2(ranks)]
            print("Second Best score index:" + str(mindex2(ranks)))
            printlineage(str(ranks.index(min(ranks, key = float))), str(mindex2(ranks)))
        else:
            minigenghy = newBrood[ranks.index(min2(ranks))]
            print("Second Best score index:" + str(ranks.index(min2(ranks))))
            printlineage(str(ranks.index(min(ranks, key = float))), str(ranks.index(min2(ranks))))


        print(genghy)
        print(minigenghy)

        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Time Of Completion =", current_time)
    
else:
    with open(toolkitPath + '\\fitnessValues.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            ranks = row
            crashGen += 1
        f.close()
    ranks = ranks[:-1]

    with open(toolkitPath + "\\Tensegrigene.csv") as f:
        reader = csv.reader(f)
        i= 1
        for row in reader:
            if (i==crashGen):
                crashPop = ', '.join(row)
            i += 1
        f.close()

    crashPop = crashPop[:-2]
    crashPop = ast.literal_eval(crashPop)
    

    
    for individual in crashPop[len(ranks):]:
        hE.expressionize(Genomics.genomeToString(individual))
        os.system("%s" % command)        
        print("done")

    with open(toolkitPath + '\\fitnessValues.csv') as f:
        reader = csv.reader(f)
        i = 1
        for row in reader:
            if (i==crashGen):
                ranks = row
            i += 1
        f.close()
    ranks = ranks[:-1]
    print("Best score:" + str(min(ranks, key = float)))
    print("Best score index:" + str(ranks.index(min(ranks, key = float))))
    print(ranks)
    genghy = crashPop[ranks.index(min(ranks, key = float))]

    print("Second Best score:" + str(min2(ranks)))

    if (min(ranks, key = float) == min2(ranks)):
        minigenghy = crashPop[mindex2(ranks)]
        print("Second Best score index:" + str(mindex2(ranks)))
        printlineage(str(ranks.index(min(ranks, key = float))), str(mindex2(ranks)))
    else:
        minigenghy = crashPop[ranks.index(min2(ranks))]
        print("Second Best score index:" + str(ranks.index(min2(ranks))))
        printlineage(str(ranks.index(min(ranks, key = float))), str(ranks.index(min2(ranks))))

    
    print(genghy)
    print(minigenghy)

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Time Of Completion =", current_time)


    genNum = crashGen

    for gen in range(crashGen,generations):

        with file(toolkitPath + "\\Tensegrigene.csv", "a") as f:
            f.write("\n")
            f.close()

        with file(toolkitPath + "\\FitnessValues.csv", "a") as f:
            f.write("\n")
            f.close()

        newBrood = Genomics.genghify3(genghy, minigenghy, adam, pSize/4,pSize/4, minGenome, maxGenome, minPPairs, maxPPairs, maxDs, maxAs, maxMs)
        ranks = []

        with file(toolkitPath + "\\Tensegrigene.csv", "a") as f:
            f.write("%s," % newBrood)
            f.close()


        for individual in newBrood:
            hE.expressionize(Genomics.genomeToString(individual))
            os.system("%s" % command)       
            print("done")
        
        with open(toolkitPath + '\\fitnessValues.csv') as f:
            reader = csv.reader(f)
            i= 0
            for row in reader:
                if (i==genNum):
                    ranks = row
                i += 1
            f.close()

        print(genNum)
        genNum += 1

        ranks = ranks[:-1]
        genghy = newBrood[ranks.index(min(ranks, key = float))]
        print("Best score:" + str(min(ranks, key = float)))
        print("Best score index:" + str(ranks.index(min(ranks, key = float))))
        print(ranks)


        
        print("Second Best score:" + str(min2(ranks)))

        if (min(ranks, key = float) == min2(ranks)):
            minigenghy = newBrood[mindex2(ranks)]
            print("Second Best score index:" + str(mindex2(ranks)))
            printlineage(str(ranks.index(min(ranks, key = float))), str(mindex2(ranks)))
        else:
            minigenghy = newBrood[ranks.index(min2(ranks))]
            print("Second Best score index:" + str(ranks.index(min2(ranks))))
            printlineage(str(ranks.index(min(ranks, key = float))), str(ranks.index(min2(ranks))))

        print(genghy)
        print(minigenghy)

        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Time Of Completion =", current_time)



    