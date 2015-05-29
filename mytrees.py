from math import log
import operator
import random

def calcEntropy(dataSet):
	numEntries = len(dataSet)
	labelCounts = {}
	for featVec in dataSet:
		currentLabel = featVec[-1]
		if currentLabel not in labelCounts.keys():
			labelCounts[currentLabel] = 0
		labelCounts[currentLabel] += 1
	entropy = 0.0
	for key in labelCounts:
		prob = float(labelCounts[key])/numEntries
		print prob, labelCounts
		entropy -= prob*log(prob,2)
	return entropy
  
def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet, labels
	
def splitDataSet(dataSet, axis, value):
	retDataSet = []
	for featVec in dataSet:
		if featVec[axis] == value:
			reducedFeatVec = featVec[:axis]
			reducedFeatVec.extend(featVec[axis+1:])
			retDataSet.append(reducedFeatVec)
	return retDataSet
	
def chooseBestFeatureToSplit(dataSet):
	numFeatures = len(dataSet[0]) - 1
	baseEntropy = calcEntropy(dataSet)
	bestInfoGain = 0.0; bestFeature = -1
	for i in range(numFeatures):
		featList = [example[i] for example in dataSet]
		uniqueVals = set(featList)
		newEntropy = 0.0
		for value in uniqueVals:
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet)/float(len(dataSet))
			newEntropy += prob*calcEntropy(subDataSet)
		infoGain = baseEntropy - newEntropy
		if (infoGain > bestInfoGain):
			bestInfoGain = infoGain
			bestFeature = i
	return bestFeature
		
def majorityCnt(classList):
	classCount = {}
	for vote in classList:
		if vote not in classCount.keys(): classCount[vote] = 0
		classCount[vote] += 1
	sortedClassCount = sorted(classCount.iteritems(),key = operator.itemgetter(1), reverse = True)
	return sortedClassCount[0][0]

def createTree(dataSet,labels):	
	classList = [example[-1] for example in dataSet]
	if classList.count(classList[0]) == len(classList):
		return classList[0]
	if len(dataSet[0]) == 1:
		return majorityCnt(classList)
	bestFeat = chooseBestFeatureToSplit(dataSet)
	bestFeatLabel = labels[bestFeat]
	myTree = {bestFeatLabel:{}}
	del(labels[bestFeat])
	featValues = [example[bestFeat] for example in dataSet]
	uniqueVals = set(featValues)
	for value in uniqueVals:
		subLabels = labels[:]
		myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
	return myTree
	
def createForest(dataSet,labels,forestSize,numSamples):
	forest = {}
	for i in range(forestSize):
		newLabels = labels[:]
		newDat = random.sample(dataSet,numSamples)
		newTree = createTree(newDat,newLabels)
		forest[i] = newTree
	return forest
	
def classify(inputTree,featLabels,testVec):
	if type(inputTree) == dict:
		firstStr = inputTree.keys()[0]
		#print(firstStr)
		secondDict = inputTree[firstStr]
		#print(secondDict)
		featIndex = featLabels.index(firstStr)
		#print(featIndex)
		key = testVec[featIndex]
		#print(key)
		if key in secondDict:
			valueOfFeat = secondDict[key]
			if isinstance(valueOfFeat, dict): 
				classLabel = classify(valueOfFeat, featLabels, testVec)
			else: classLabel = valueOfFeat
		else: classLabel = 'unsure'
	else: classLabel = inputTree
	return classLabel
	
def classifyOnForest(forest,featLabels,testVec):
	results = {}
	for i in range(len(forest)):
		print('classifying on tree ' + str(i))
		#print(forest[i])
		results[i] = classify(forest[i],featLabels,testVec)		
	return results

def voteOnForest(forest,featLabels,testVec):
	results = classifyOnForest(forest,featLabels,testVec)
	classCount = {}
	for vote in results.values():
		if vote not in classCount.keys(): classCount[vote] = 0
		classCount[vote] += 1
	sortedClassCount = sorted(classCount.iteritems(),key = operator.itemgetter(1), reverse = True)
	print(sortedClassCount)
	return sortedClassCount[0][0]
		
def pickMyLenses(forestSize,numSamples):
	fr = open('lenses.txt')
	lenses = [inst.strip().split('\t') for inst in fr.readlines()]
	lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
	forest = createForest(lenses,lensesLabels,forestSize,numSamples)
	#print forest
	results = voteOnForest(forest,lensesLabels,['pre','hyper','no','normal'])
	print results #should be 'soft'
	return results
	
