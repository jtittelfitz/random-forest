# random-forest
Machine learning on a contact lens database using a random forest, 
  using the decision tree code from Peter Harrington's 'Machine Learning in Action'.

Functions calcEntropy, createDataSet, splitDataSet, chooseBestFeatureToSplit, majorityCnt, createTree 
  taken from MLiA by Peter Harrington
  
Funtion classify modified from Harrington's code 
  (to handle cases where tree has missing branches to to "bad" or limited random selection of training cases.
  
Functions createForest, classifyOnForest, voteOnForest, pickMyLenses are my own.

Usage:
load the module, then run pickMyLenses (specify number of trees in forest, and number of training examples per tree)

program will classify suggested lens type (by taking majority vote among trees in forest)
  for someone with attributes: age = 'pre', prescription = 'hyper', astigmatic = 'no', tear rate = 'normal'
  
(should return 'soft', but results may vary if the number of trees or samples is too small)

code can be easily modified to run on different attributes, or to learn and classify entirely different database, file should be tab separated, with one training example per line, listing all features followed by the proper classification 
