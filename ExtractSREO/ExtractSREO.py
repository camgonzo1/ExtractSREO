# File Name: ExtractSREO.py
# Authors: Ryan Dunn and Cam Gonzalez
# Description: This file executes the SREO importation, information extraction, and notificication for 
#              the LoanBoss online application on the back end.
import csv
import camelot
from cmath import nan
from fileinput import filename
from lib2to3.pytree import convert
from numpy import dtype
import os
import pandas as pd
from prepareData import *
from re import L
import string
from trainModel import *
<<<<<<< HEAD
from openpyxl import Workbook
=======
>>>>>>> parent of 3fca60e (UI tweaks)

ROW, COLUMN = 0, 1 # Values Indicating DataFrame Axis'
PERMITTED_FORMATS = ["csv", "xlsx"]
HEADER_MODEL, DATA_MODEL = 'Model/headerTest', '' # Trained AI Models for Data Interpretation
DATA_ANALYSIS, HEADER_ANALYSIS = 1, 2 
NO_PRINT, PRINT = 0, 1
modelName = None
totalCorrect, totalNum = 0, 0

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def setModelName(name):
    global modelName
    modelName = name
def getModelName():
    return modelName

# Name: extractSREO()
# Parameters: curFilePath (string) --> conatins the current path to the desired file for importation
# Return: sreoData (pandas DataFrame) --> conatins data from file
# Description: Pulls data from csv or excel sheet and stores in pandas dataframe
def extractSREO(trainColumn, curFilePath):
	# Determines File Type 
	path = curFilePath.split("/")
	print(path[len(path) - 1]) 
	splitPath = curFilePath.split(".")
	fileType = splitPath[len(splitPath) - 1]

	# Reads Data into Pandas DataFrame
	if fileType not in PERMITTED_FORMATS:
		raise TypeError("Error: Please input compatible file type!")
	elif fileType == "csv":
		sreoData = pd.read_csv(curFilePath, header=None)
	elif fileType == "xlsx":
		sreoData = pd.read_excel(curFilePath, header=None)
	elif fileType == "pdf": # still in trial stage (unreliable)
		tables = camelot.read_pdf(curFilePath, flavor='stream', row_tol=7)
		tables.export(curFilePath, f='csv', compress=True)
		sreoData = tables[0].df

	# Removes Uneccessary Information from DataFrame and Formats Correctly
	sreoData.replace('\n', '', regex=True, inplace=True)
	sreoData.mask(sreoData == '', inplace=True)
	sreoData.dropna(axis=ROW, how='all', inplace=True)
	sreoData.dropna(axis=COLUMN, how='all', inplace=True)
	sreoData = sreoData.reset_index(drop=True).rename_axis(None, axis=COLUMN)

	# Reformat DataFrame to Apply Header
	index = getHeaderIndex(sreoData)
	if index == -1:
		raise IndexError("Error Downloading File: Please retry download or use different file format!")
	sreoData.columns = [sreoData.iloc[index]]
	sreoData = sreoData[(index + 1):].reset_index(drop=True).rename_axis(None, axis=COLUMN)
	return sreoData

# Name: getHeaderIndex()
# Parameters: searchData (pandas DataFrame) --> conatins unfiltered data from an SREO
# Return: i (int) --> the index of the header row
#         -1 (int) --> Error: No header row found
# Description: Searches Data for Header Row
def getHeaderIndex(searchData):
	for i in range(len(searchData.index)):
		rowString = ((searchData.iloc[i])).apply(str).str.cat(sep=' ')
		if testInput(False, HEADER_MODEL, rowString, NO_PRINT) == "Valid":
			return i
	return -1

# Name: fillTemplate()
# Parameters: sreoDataFrame (pandas DataFrame) --> conatins semi-filtered data from an SREO
# Return: sreoTemplate.to_excel() (.xlsx) --> contains the populated SREO standard template
# Description: Takes in a nonstandardized SREO and analyzes using a NLP model to restrusture 
#              data in a standardized model which it exports in a .xlsx format fllowing a 
#              notification to the abstraction team. 
def fillTemplate(sreoDataFrame):
    sreoTemplate = pd.DataFrame(columns=['Property Name','Address','City','State','Property Type','Units','Square Feet','Occupancy', 'Acquisition Date', 'Lender', 'Maturity Date', 'Loan Amount', 'Current Balance', 'Debt Service', 'NOI', 'DSCR', 'Market Value', 'LTV', 'Amort Start Date', 'Rate Type', 'All-In Rate', 'Spread', 'Index'])
    bestIndex = {'Property Name': [-1, 0],
                 'Address': [-1, 0],
                 'City': [-1, 0],
                 'State':[-1, 0],
                 'Property Type': [-1, 0],
                 'Units': [-1, 0],
                 'Square Feet': [-1, 0],
                 'Occupancy': [-1, 0],
                 'Acquisition Date': [-1, 0],
                 'Lender': [-1, 0],
                 'Maturity Date': [-1, 0],
                 'Loan Amount': [-1, 0],
                 'Current Balance': [-1, 0],
                 'Debt Service': [-1, 0],
                 'NOI': [-1, 0],
                 'DSCR': [-1, 0],
                 'Market Value': [-1, 0],
                 'LTV': [-1, 0],
                 'Amort Start Date': [-1, 0],
                 'Rate Type': [-1, 0],
                 'All-In Rate': [-1, 0],
                 'Spread': [-1, 0],
                 'Index': [-1, 0]}
    for dataColumn in sreoDataFrame.columns:
        guess = outputConfidence(modelName, DATA_ANALYSIS, str(dataColumn[0]), NO_PRINT)
        if guess[0] != "N/A" and guess[0] != "Invalid" and guess[1] > bestIndex[guess[0]][1]:
           bestIndex[guess[0]][0] = str(dataColumn[0])
           bestIndex[guess[0]][1] = guess[1]

    for entry in bestIndex:
        if bestIndex[entry][0] != -1:
            sreoTemplate[entry] = sreoDataFrame[bestIndex[entry][0]]

    Workbook().save(filename = "Standardized-" + newName + ".xlsx")
    sreoTemplate.to_excel("Standardized-" + newName + ".xlsx", index=False)
    return sreoTemplate

# Name: standardizeSREO()
# Parameters: sreoFilePath (string) --> conatins the current path to the desired file for importation
# Return: fillTemplate(extractSREO(sreoFilePath)) (.xlsx) --> contains the populated SREO standard template
# Description: Takes in a file path, pulls and analyzes data and restrustures
#              data in a standardized model which it exports in a .xlsx format following a 
#              notification to the abstraction team.
def standardizeSREO(sreoFilePath):
    return fillTemplate(extractSREO(sreoFilePath))

######################## For Testing #################################
FILES = ["SREOs/2022 Lawrence S Connor REO Schedule.csv", "SREOs/2022 Lawrence S Connor REO Schedule.xlsx", "SREOs/AP - REO excel 202112.csv", "SREOs/AP - REO excel 202112.xlsx", "SREOs/NorthBridge.csv", "SREOs/NorthBridge.xlsx", "SREOs/RPA REO Schedule - 01.31.2022.csv", "SREOs/RPA REO Schedule - 01.31.2022.xlsx", "SREOs/Simpson REO Schedule (12-31-21).csv", "SREOs/Simpson REO Schedule (12-31-21).xlsx", "SREOs/SREO Export Template v2 - final.csv", "SREOs/SREO Export Template v2 - final.xlsx"]
CUR_FILE = "SREOs/2022 Lawrence S Connor REO Schedule.csv"

# Name: testConfidence()
# Parameters: data (pandas DataFrame) --> conatins data from SREO file
# Return: None --> prints to screen and updates global variables directly
# Description: This function test how well the data AI program would be categorizing into the template
def testConfidence(trainColumn, data):
	global totalCorrect
	global totalNum
	compare = pd.read_excel("Header Data/DataGroups.xlsx")
	correct = 0
	COLUMN_LABELS = {1: "Units", 2: "City", 3: "State", 4: "Address", 5: "Rate Type", 6: "Acquisition Date", 
					 7: "Maturity Date", 8: "Property Name", 9: "Square Feet", 10: "Occupancy", 11: "Loan Amount",
					 12: "Debt Service", 13: "NOI", 14: "DSCR", 15: "Market Value", 16: "LTV", 17: "Amort Start Date", 
					 18: "Property Type", 19: "Current Balance", 20: "All-In Rate", 21: "Lender", 22: "Spread", 23: "Index"}
	confidences = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	columnHeaders = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
	for column in data.columns:
		#myString = str(column[0]) + " " + (data[column]).apply(str).str.cat(sep=' ')
		myString = str(column[0]) + " " + ((data[column]).dropna().apply(str)[:2]).str.cat(sep=' ')
		guess = outputConfidence(trainColumn, modelName, myString, NO_PRINT)
		labelIndex = get_column_label(guess[0])
		if confidences[labelIndex - 1] < guess[1]:
			confidences[labelIndex - 1] = guess[1]
			columnHeaders[labelIndex - 1] = str(column[0])
		if guess[0] in compare.columns:
			if str(column[0]) in compare[guess[0]].apply(str).str.cat(sep=' '):
				correct += 1
		print(str(column[0]) + ' --> ' + guess[0] + ' ' + str(guess[1]))
	print("----------------- Highest Values --------------------")
	for i in range(len(COLUMN_LABELS)):
		print(columnHeaders[i] + " --> " + COLUMN_LABELS[i + 1] + " " + str(confidences[i]))
	totalCorrect += correct
	totalNum += getNumLabels()
	print("Accuracy of Trained Categories = " + str("{:.2%}".format(correct/getNumLabels())))
	print("Total Accuracy = " + str("{:.2%}".format(correct/len(data.columns))))

# Name: runTests()
# Parameters:None
# Return: None --> prints to screen and updates global variables directly
# Description: This function allows the user to create models and test said models against SREOs
def runTests(trainColumn):
	global modelName
	startOption = int(input("1 for Column training, 2 for Header training, 3 for testing existing model, 4 to test SREOs, 5 to quit: "))
	if startOption == 2: trainColumn = False
	while(startOption != 5):
		if startOption == 4:
			modelName = "Model/" + input("Model Name: ")
			if input("Test All Files (Y/N): ") == 'Y':
				for file in FILES:
					print('------------------------------------------------------------')
					data = extractSREO(trainColumn, file)
					print(data.to_string())
					testConfidence(trainColumn, data)
					print('------------------------------------------------------------')
				print("Total Accuracy of Trained Categories = " + str("{:.2%}".format(totalCorrect/totalNum)))
			elif input("Test Current File (Y/N): ") == 'Y':
				print('------------------------------------------------------------')
				data = extractSREO(trainColumn, CUR_FILE)
				print(data)
				testConfidence(trainColumn, data)
				print('------------------------------------------------------------')
		elif startOption == 3:
			startOption = int(input("1 for Column model, 2 for Header model: "))
			modelName = input("Model Name: ")
			print(outputConfidence(trainColumn, modelName, startOption, input("Input test string: "), 1))
		else:
			if(input("Create new dataset (Y/N) ") == "Y"): 
				numRepeats = input("Number of Repeats per Category: ")
				createData(trainColumn, 'trainingData.csv', int(numRepeats))
				trainModel(trainColumn, "trainingData.csv")
			elif(input("1 to use generated data 2 to use existing files: ") == "2"):
				#trainOnCSV()
				trainModel(trainColumn, "extractedTrainingData.csv")
			else: trainModel(trainColumn, "trainingData.csv")
		startOption = int(input("\n1 for Column training, 2 for Header training, 3 for testing existing model, 4 to test SREOs, 5 to quit: "))

FILE_LIST = ["2021 12 14_MWest_Debt Schedule.csv", "2022 Lawrence S Connor REO Schedule.csv", "AP - REO excel 202112.csv", "Copy of Carlos & Vera Koo - RE Schedule - March 2022 v.2.csv", "David T. Matheny and Susan Matheny - RE Schedule 5.19.21.csv", 
			 "Mark Johnson - RE Schedule September 2020.csv", "NorthBridge.csv", "RPA REO Schedule - 01.31.2022.csv", "Simpson REO Schedule (12-31-21).csv",
			 "SimpsonHousingLLLP-DebtSummary-2021-09-07.csv", "SP Inc., SP II and SP III - RE Schedule 11.20.2019.csv", "SREO Export Template v2 - final.csv", "Stoneweg.csv", "TCG - 2022 Fund XI REO Schedule.csv"]
def testOnSolvedCSV():
    totalCorrect = 0
    totalNum = 0
    for file in FILE_LIST:
        curCSV = pd.read_csv("SREOs/CSVs/" + file, header=None)
        answerRow = ((curCSV.iloc[0])).apply(str)
        testFrame = standardizeSREO("SREOs/CSVs/" + file)
        testFrame.dropna(axis=COLUMN, how='all', inplace=True)
        correct, total = 0, 0
        for i in range(len(answerRow)):
            if answerRow[i] != "nan":
                total += 1
            if answerRow[i] in testFrame.columns:
                correct += 1
        totalCorrect += correct
        totalNum += total
        print()
        print(file)
        print("Required Headers Accuracy --> " + str("{:.2%}".format(correct/total)))
        print("Total Number of Headers Accuracy --> " + str("{:.2%}".format(len(testFrame.columns)/total)))
        print()
    print("-----------------------------------------------------------------------------------------------")
    print("Total Required Headers Accuracy --> " + str("{:.2%}".format(totalCorrect/totalNum)))

	