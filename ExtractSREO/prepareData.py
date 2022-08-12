import os
import random
import pandas as pd
import json as json

os.chdir(os.path.dirname(os.path.abspath(__file__)))
f = open('columnHeaderData.json')
data = json.load(f)

def isValidColumnHeader(label):
	for headerList in data["headers"]:
		if label in headerList:
				return True
	return False

def generateData(numRepeats):
	df = pd.DataFrame(columns=['label','text'])
	for i in range(numRepeats):
		headerList = random.choice(data["headers"])
		df.loc[i, 'label'] = headerList[0]
		df.loc[i, 'text'] = random.choice(headerList)
	return df

def generateHeaderData(numRepeats):
	df = pd.DataFrame(columns=['label','text'])
	for i in range(numRepeats):
		validOrInvalid = random.randint(0,1)
		if validOrInvalid == 1:
			df = pd.concat([df, generateValidHeader()], ignore_index=True)
		else:
			df = pd.concat([df, generateInvalidHeader()], ignore_index=True)
	return df

def generateValidHeader():
	numVals = random.randint(15, 25)
	exportString = ""
	for j in range(numVals):
		rand = random.randint(0,3)
		if(rand == 0):
			exportString += "nan "
		else:
			randomHeaderList = random.choice(data["headers"])
			exportString += random.choice(randomHeaderList) + " "
	df = pd.DataFrame({ 'label' : "Valid", 'text' : exportString }, index = [1])
	return df


def generateInvalidHeader():
	rand = random.randint(0,1)
	numVals = random.randint(15, 25)
	exportString = ""
	for j in range(0,numVals):
			rand = random.randint(0,10)
			if(rand == 0): exportString += str(random.randint(1,12)) + "/" + str(random.randint(1,31)) + "/" + str(2000 + random.randint(0,25)) + " "
			elif(rand == 1): 
				randomHeaderList = random.choice(data["headers"])
				exportString += random.choice(randomHeaderList) + " "
			else: exportString += "nan "
	df = pd.DataFrame({'label' : "Invalid", 'text' : exportString }, index = [1])
	return df