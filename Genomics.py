import  random

#ideas - genome 2 arrays, first expressions, second index pairs for parenthesis
#length interpolation - define step size instead of restlength(clamp stepsize and restlength independently) change integer list to include negatives, smaller range, maybe include floats

m = ["+", "-", "*", "<",">","==", " && ", " || ", " / ", " % "]
parenthesesIndices = []

pseuedoOps = [" min ", " max "]




values =  []
for p in range(0,9): values.append(p)

variables = ["@stiffness","@primnum","@Frame","error", "pOrient", "p1Hits", "p2Hits", "@restlength", "p1pos.x","p1pos.y","p2pos.z","p2pos.x","p2pos.y","p2pos.z","primCenter.x","primCenter.y","primCenter.z"]

newvariables = ["p1LocalX", "p2LocalX", "p1LocalY", "p2LocalY", "p1LocalZ", "p2LocalZ", "objX", "objY", "objZ", "vObjX", "vObjY", "vObjZ", "p1VX", "p2VX", "p1VY","p2VY", "p1VZ", "p2VZ", "p1Upside","p2Upside", "p1Down", "p2Down", "p1UpsideDown", "p2UpsideDown"]

newnewvariables = ["@flat", "@contact", "@legs", "@legsPrimErrorRank", "@flatPrimErrorRank", "@primproxy", "@errorRank"]

values += variables
values += newvariables
variables += newnewvariables

def initializePopulation(populationSize, minGenome,maxGenome, minPPairs, maxPPairs):
    population = []
    for x in range(0,populationSize):
        genome = []
        eGenes = []
        pGenes = []
        eGenes.append(str(values[random.randrange(0,len(values))]))
        for j in range(0,random.randrange(minGenome, maxGenome)):
            eGenes.append(m[random.randrange(0,len(m))])
            eGenes.append(str(values[random.randrange(0,len(values))]))
        for k in range(0,random.randrange(minPPairs, maxPPairs)):
            pGenes.append(random.randrange(0,len(eGenes), 2))
            pGenes.append(random.randrange(0,len(eGenes), 2))
        genome.append(eGenes)
        genome.append(pGenes)
        population.append(genome)
    return population

#print(initializePopulation(1,4,1,4))

def sortPgenes(genome):
    eGenes, Pgenes = genome
    exLen = len(eGenes)
    sortedGenes = []
    openPs= []
    closePs = []
    for x,y in zip(Pgenes[::2],Pgenes[1::2]): sortedGenes.append( [x,y]) if x < y else sortedGenes.append([y,x])
    for i in range(len(sortedGenes)): openPs.append(sortedGenes[i][0])
    for i in range(len(sortedGenes)): closePs.append(sortedGenes[i][1])
    openPs.sort()
    closePs.sort()
    sortedGenes = deleteriousdeletions(openPs, closePs,exLen)
    return sortedGenes

def deleteriousdeletions(openPs,closePs, exLen):
    cleanGenes = []
    openPs = [gene for gene in openPs if not gene in closePs or closePs.remove(gene)]
    for i in range(0, len(openPs)):
        if (openPs[i]< 0): openPs[i] = 0
        if (closePs[i]< 0): closePs[i] = 0
    cleanGenes = [openPs,closePs]
    while len(cleanGenes[0]) != len(cleanGenes[1]):
        max(cleanGenes[0], cleanGenes[1], key = len).pop(0)
    for i in range(0, len(cleanGenes[0])):
        if cleanGenes[0][i] > exLen*2:
            cleanGenes[0][i] = exLen*2
    for i in range(0, len(cleanGenes[1])): 
        if cleanGenes[1][i] > exLen*2:
            cleanGenes[1][i] = exLen*2
    cleanerGenes = []
    for i in range(0, len(cleanGenes[0])):
        cleanerGenes.append([cleanGenes[0][i],cleanGenes[1][i]])
    cleanestGenes = []
    for i in cleanerGenes:
        if i not in cleanestGenes:
            cleanestGenes.append(i)
    perfectOpenPs = []
    perfectClosePs = []

    for i in cleanestGenes:
        perfectOpenPs.append(i[0])
        perfectClosePs.append(i[1])

    perfectPs = [perfectOpenPs,perfectClosePs]

    return perfectPs

def geneCleaner(genome):
    eGenes, Pgenes = genome
    cleanedGenes = sortPgenes(genome)
    foldedGenes = []
    for i in range(0, len(cleanedGenes[0])):
        foldedGenes.append(cleanedGenes[0][i])
        foldedGenes.append(cleanedGenes[1][i])
    genome = [eGenes, foldedGenes]
    return genome


def genomeToString(genome):
    eGenes, pGenes = genome
    pGenes = sortPgenes(genome)
    p = ""
    for i in range(len(eGenes)):
        for j in range(pGenes[0].count(i)):
            p += "("
        p +=eGenes[i]
        for j in range(pGenes[1].count(i)):
            p += ")"
    for j in range(pGenes[1].count((len(eGenes)+1))):
        p += ")"
    
    return p

def populationToString(population):
    p = ""
    for x in population:
        p += genomeToString(x)
    return p

def evalPop(population):
    j = []
    for x in population:
        j.append(eval(genomeToString(x)))
    return j

def mutate(genome):
    eGenes, pGenes = genome
    e = random.randrange(0, len(eGenes))
    if e % 2 == 0:
        eGenes[e] = str(values[random.randrange(0,len(values))])
    else:
        eGenes[e] = m[random.randrange(0,len(m))]
    if (len(pGenes)>0):
        p = random.randrange(0, len(pGenes))
        pGenes[p] = random.randrange(0,len(eGenes), 2)
    genomes = [eGenes, pGenes]
    return genome

def iMutate(genome, numMs):
    for i in range(0,numMs):
        genome = mutate(genome)
    return genome

def mutatePop(population):
    mutatedPop = []
    for p in population:
        mutatedPop.append(mutate(p))
    return mutatedPop

def delete(genome):
    eGenes, pGenes = genome
    if (len(pGenes)==0):
        p = 0
    else:
        p = random.randrange(0, max(1,round(len(pGenes)/2)))
    e = random.randrange(0, max(1,round(len(eGenes)/2)))
    if e == 0:
        eGenes = eGenes[2:]
    else:
        eGenes= eGenes[:e*2-1] + eGenes[e*2+1:]
    if p == 0:
        pGenes = pGenes[2:]
    else:
        pGenes= pGenes[:p*2] + pGenes[p*2+2:]
    genome = [eGenes, pGenes]
    return genome

def iDelete(genome,numDs):
    eGenes, pGenes = genome
    omi = len(eGenes)

    if((numDs*2)> omi):
        numDs = (omi-1)/2

    for i in range(0, numDs):
        genome = delete(genome)
    eGenes, pGenes = genome
    fixedpGenes = []
    for x in pGenes:
        if (x >= omi - numDs):
            x -= 2* numDs
        fixedpGenes.append(x)
    genome = [eGenes, fixedpGenes]
    return genome

def deletePop(population):
    deletedPop = []
    for p in population:
        deletedPop.append(delete(p))
    return deletedPop

def add(genome):
    eGenes, pGenes = genome
    e = random.randrange(0, max(1, round(len(eGenes)+1/2)))
    if (len(pGenes)==0):
        p = 0
    else:
        p = random.randrange(0, round(len(pGenes)+1/2))
    if e == 0:
        eGenes = [str(values[random.randrange(0,len(values))])] + [m[random.randrange(0,len(m))]] + eGenes
    else:
        eGenes= eGenes[:e*2-1] + [m[random.randrange(0,len(m))]] + [str(values[random.randrange(0,len(values))])] + eGenes[e*2-1:]
    if p == 0:
        pGenes = [random.randrange(0, len(eGenes),2)] + [random.randrange(0, len(eGenes),2)] + pGenes
    else:
        pGenes= pGenes[:p*2] + [random.randrange(0, len(eGenes),2)] + [random.randrange(0, len(eGenes),2)] + pGenes[e*2:]
    genome = [eGenes,pGenes]
    return genome

def iAdd(genome, numAs):
    for i in range(0,numAs):
        genome = add(genome)
    return genome

def addPop(population):
    addedPop = []
    for p in population:
        addedPop.append(add(p))
    return addedPop

def genghify(genghis, broodsize):
    brood = []
    brood.append(genghis)
    for b in range(0,broodsize-1):
        lilGenghis = mutate(add(delete(genghis)))
        brood.append(lilGenghis)
    
    return brood

def genghify2(genghis, broodsize,babyjesi, minGenome,maxGenome, minPPairs, maxPPairs, maxDs, maxAs, maxMs):
    numDs = random.randrange(0, maxDs)
    numAs = random.randrange(0, maxAs)
    numMs = random.randrange(0, maxMs)
    brood = []
    brood.append(genghis)
    for b in range(0,broodsize-1):
        lilGenghis = iMutate(iAdd(iDelete(genghis, numDs), numAs), numMs)
        brood.append(lilGenghis)
    brood += initializePopulation(babyjesi, minGenome,maxGenome, minPPairs, maxPPairs)
    return brood

def genghify3(genghis, minigenghis, adam, broodsize,babyjesi, minGenome,maxGenome, minPPairs, maxPPairs, maxDs, maxAs, maxMs):
    numDs = random.randrange(0, maxDs)
    numAs = random.randrange(0, maxAs)
    numMs = random.randrange(0, maxMs)
    brood = []
    brood.append(genghis)
    for b in range(0,broodsize-1):
        lilGenghis = iMutate(iAdd(iDelete(genghis, numDs), numAs), numMs)
        brood.append(lilGenghis)
    brood.append(minigenghis)
    for b in range(0,broodsize-1):
        lilGenghis = iMutate(iAdd(iDelete(minigenghis, numDs), numAs), numMs)
        brood.append(lilGenghis)
    brood.append(adam)
    for b in range(0,broodsize-1):
        lilGenghis = iMutate(iAdd(iDelete(adam, numDs), numAs), numMs)
        brood.append(lilGenghis)
    brood += initializePopulation(babyjesi, minGenome,maxGenome, minPPairs, maxPPairs)

    for i in range(0, len(brood)):
        brood[i] = geneCleaner(brood[i])
    return brood

        
    


#print(populationToString(initializePopulation(1,4,1,4)))

#testpop = initializePopulation(1,4,1,4)
#print(evalPop(testpop))
#print(testpop)
#newPop = mutatePop(testpop)
#print(newPop)
#print(evalPop(newPop))
#deletepop = deletePop(newPop)
#print(deletepop)
#addpop = addPop(deletepop)
#print(addpop)
#print (genghify(addpop[0], 8))


#j = str(i[random.randrange(0,20)])
#for p in range(0, random.randrange(0,20)):
#    j += m[random.randrange(0,len(m))] + str(i[random.randrange(0,20)])

#print(eval(j))