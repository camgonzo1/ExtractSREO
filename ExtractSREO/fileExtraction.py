# Authors: Ryan Dunn and Cameron Gonzalez

#import csv
#import camelot
#from cmath import nan
#from fileinput import filename
#from lib2to3.pytree import convert
#from numpy import dtype
import os
import sys
#from pickle import FALSE
import pandas as pd
from prepareData import *
#from re import L
#import string
from trainModel import *
#from openpyxl import Workbook
import warnings
#import tkinter as tk
#from tkinter import filedialog
import tabula as tabula
import logging
import os.path
from zipfile import ZipFile
import json as json

from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_renditions_element_type import ExtractRenditionsElementType
from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
from adobe.pdfservices.operation.pdfops.options.extractpdf.table_structure_type import TableStructureType

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

ROW, COLUMN = 0, 1 # Values Indicating DataFrame Axis'
PERMITTED_FORMATS = ["csv", "xlsx", "pdf"]
HEADER_MODEL = 'Model/headerTest'
modelName = None

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
def extractSREO(curFilePath):
	# Determines File Type 
	splitPath = curFilePath.split(".")
	fileType = splitPath[len(splitPath) - 1]

	# Reads Data into Pandas DataFrame
	if fileType not in PERMITTED_FORMATS:
		raise TypeError("Error: Please input compatible file type!")
	elif fileType == "csv":
		#sreoData = pd.read_csv(curFilePath, header=None)
		sreoData = pd.read_csv(curFilePath, header=None, skiprows=1) # For Testing
	elif fileType == "xlsx":
		sreoData = pd.read_excel(curFilePath, header=None)
	elif fileType == "pdf":
		sreoDataList = tabula.read_pdf(curFilePath,pages='all',guess=False)
		if len(sreoDataList) < 1:
			print("Table Not Recognized")
			return
		sreoData = sreoDataList[0]
		for i in range(1, len(sreoDataList)):
			sreoData = pd.concat([sreoData, sreoDataList[i]], index=False)
		print(sreoData.to_string)

	# Removes Uneccessary Information from DataFrame and Formats Correctly
	sreoData.replace(to_replace='\n', value=' ', regex=True, inplace=True)
	sreoData.replace(to_replace='  ', value=' ', regex=True, inplace=True)
	sreoData.mask(sreoData == '', inplace=True)
	sreoData.dropna(axis=ROW, how='all', inplace=True)
	sreoData.dropna(axis=COLUMN, how='all', inplace=True)
	sreoData = sreoData.reset_index(drop=True).rename_axis(None, axis=COLUMN)
	sreoData = transposeVerticalRows(sreoData)
	# Reformat DataFrame to Apply Header
	index = getHeaderIndex(sreoData)
	sreoData = mergeHeaderRows(sreoData, index)
	if index == -1:
		raise IndexError("Error Downloading File: Please retry download or use different file format!")
	sreoData.columns = sreoData.iloc[index]
	sreoData = sreoData[(index + 1):].reset_index(drop=True).rename_axis(None, axis=COLUMN)
	return sreoData

def transposeVerticalRows(sreoData):
	transposedSreoData = sreoData.T
	transposedHeaderIndex = getHeaderIndex(transposedSreoData)
	sreoDataHeaderIndex = getHeaderIndex(sreoData)
	sreoDataCount = 0
	transposedCount = 0
	#print(sreoData.to_string())
	for cell in sreoData.iloc[sreoDataHeaderIndex]:
		if validColumnHeader(str(cell)):
			sreoDataCount += 1
	for cell in transposedSreoData.iloc[transposedHeaderIndex]:
		if validColumnHeader(str(cell)):
			transposedCount += 1
	if transposedCount > sreoDataCount:
		return transposedSreoData
	else:
		return sreoData

def mergeHeaderRows(sreoData, headerIndex):
	row1 = sreoData.iloc[headerIndex]
	row2 = sreoData.iloc[headerIndex + 1]
	headers = open("headers.txt", "r")
	lines = headers.readlines()
	numCells = 0
	numCellsContainingHeaders = 0
	for cell in row2:
		if str(cell) != "nan":
			numCells += 1
		for line in lines:
			if str(cell) in line and len(str(cell)) > 1:
				numCellsContainingHeaders += 1
				continue
	if(float(numCellsContainingHeaders) / float(numCells)) > 0.8:
		for i in range(len(row1)):
			if(i in row2 and i < len(row2)):
				if str(row2[i]) != "nan" :
					if str(row1[i]) == "nan":
						row1[i] = str(row2[i])
					elif str(row1[i])[len(str(row1[i]))-1] != " " or str(row2[i])[0] != " ":
						row1[i] = str(row1[i]) + " " + str(row2[i])
					else:
						row1[i] = str(row1[i]) + str(row2[i])
		sreoData.iloc[headerIndex] = row1
		return sreoData.drop(index=headerIndex+1)
	else:
		return sreoData

	# Name: getHeaderIndex()
# Parameters: searchData (pandas DataFrame) --> conatins unfiltered data from an SREO
# Return: i (int) --> the index of the header row
#         -1 (int) --> Error: No header row found
# Description: Searches Data for Header Row
def getHeaderIndex(searchData):
	for i in range(len(searchData.index)):
		rowString = ((searchData.iloc[i])).apply(str).str.cat(sep=' ')
		confidence = outputConfidence(False,HEADER_MODEL,rowString)
		if confidence[0] == "Valid":
			return i
	return -1

# Name: fillTemplate()
# Parameters: sreoDataFrame (pandas DataFrame) --> conatins semi-filtered data from an SREO
# Return: sreoTemplate.to_excel() (.xlsx) --> contains the populated SREO standard template
# Description: Takes in a nonstandardized SREO and analyzes using a NLP model to restrusture 
#              data in a standardized model which it exports in a .xlsx format fllowing a 
#              notification to the abstraction team. 
def fillTemplate(sreoDataFrame):
	sreoTemplate = pd.DataFrame(columns=['Property Name','Address','City','State','Property Type','Units','Square Feet','Occupancy', 'Acquisition Date', 'Lender', 'Maturity Date', 'Loan Amount', 'Current Balance', 'Debt Service', 'NOI', 'DSCR', 'Market Value', 'LTV', 'Amort Start Date', 'Rate Type', 'All-In Rate', 'Spread', 'Index', 'Loan Type'])
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
		if type(modelName) is str:
			guess = outputConfidence(True, modelName, str(dataColumn))
		else:
			guess = outputConfidenceMultipleModels(True, modelName, str(dataColumn))
		if guess[0] != "N/A" and guess[0] != "Invalid" and guess[1] > bestIndex[guess[0]][1]:
			#print(dataColumn)
			#print(guess)
			#print()
			bestIndex[guess[0]][0] = str(dataColumn)
			bestIndex[guess[0]][1] = guess[1]

	for entry in bestIndex:
		if bestIndex[entry][0] != -1 and bestIndex[entry][0] in sreoDataFrame:
			if(type(sreoDataFrame[bestIndex[entry][0]]) is pd.core.series.Series):
				dataFrameColumn = sreoDataFrame[bestIndex[entry][0]]
			elif(len(sreoDataFrame[bestIndex[entry][0]].columns) > 1):
				dataFrameColumn = sreoDataFrame[bestIndex[entry][0]].iloc[:,0]	
			else:
				dataFrameColumn = sreoDataFrame[bestIndex[entry][0]]
			sreoTemplate[entry] = dataFrameColumn

	for row in range(sreoDataFrame.shape[0]):
		for column in sreoDataFrame.columns:
			if "Fannie Mae" in str(sreoDataFrame.at[row, column]) or "fannie mae" in str(sreoDataFrame.at[row, column]):
				sreoTemplate.at[row,'Loan Type'] = "Fannie Mae"
			elif "Freddie Mac" in str(sreoDataFrame.at[row, column]) or "freddie mac" in str(sreoDataFrame.at[row, column]):
				sreoTemplate.at[row,'Loan Type'] = "Freddie Mac"
	#Workbook.save(filename = "Standardized-" + newName + ".xlsx")
	
	return sreoTemplate


def extractFromPDF(filePath):
	logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
	try:
		for f in os.listdir("pdfExtraction/"):
			os.remove(os.path.join("pdfExtraction/", f))
		#Initial setup, create credentials instance.
		credentials = Credentials.service_account_credentials_builder().from_file("pdfservices-api-credentials.json").build()
		
		#Create an ExecutionContext using credentials and create a new operation instance.
		execution_context = ExecutionContext.create(credentials)
		extract_pdf_operation = ExtractPDFOperation.create_new()
		
		#Set operation input from a source file.
		source = FileRef.create_from_local_file(filePath)
		extract_pdf_operation.set_input(source)
		
		#Build ExtractPDF options and set them into the operation
		extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder().with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
        .with_element_to_extract_renditions(ExtractRenditionsElementType.TABLES) \
        .with_table_structure_format(TableStructureType.CSV) \
        .build()
		extract_pdf_operation.set_options(extract_pdf_options)
		#Execute the operation.
		result: FileRef = extract_pdf_operation.execute(execution_context)
		#Save the result to the specified location.
		zipFilePath = "pdfExtraction/extract" + str(filePath).split("/")[len(str(filePath).split("/"))-1].split(".")[0] + ".zip"
		result.save_as(zipFilePath)

		with ZipFile(zipFilePath, 'r') as zipObject:
			for fileName in zipObject.namelist():
				if fileName.endswith('.json'):
					zipObject.extract(fileName, 'pdfExtraction')

		f = open('pdfExtraction/structuredData.json')
		data = json.load(f)
		dataframe = pd.DataFrame()
		if False:
			if 'Text' in element and 'Table' in element['Path']:	
				print(element['Text'])
				path = element['Path']
				print(path)
				row = 1
				column_names = []
				if path.split('/')[6] not in column_names:
					column_names.append(path.split('/')[6])
				print(path.split("/")[6])
				if '/P[' in path:
					row += int(path.split('/P[')[1].split(']')[0])
					print('/P[ ' + path.split('/P[')[1].split(']')[0])
				if '/TR[' in path:
					row += int(path.split('/TR[')[1].split(']')[0])
					print("/TR[ " + str(path.split('/TR[')[1].split(']')[0]))
				if 'TH' in path:
					column += 1
				if ']/P' in path:
					column += int(path.split(']/P')[0].split('[')[len(path.split(']/P')[0].split('['))-1])

				print("row: " + str(row))
				print("col: " + str(column))
				print()
				dataframe.at[row,column] = element['Text']

		print(dataframe.to_string())
	except (ServiceApiException, ServiceUsageException, SdkException):
		logging.exception("Exception encountered while executing operation")



def outputConfidenceMultipleModels(testColumn, modelName, textInput):
	outputCounts = {}
	for model in modelName:
		output = outputConfidence(testColumn, model, textInput)
		if output[0] in outputCounts.keys():
			outputCounts[output[0]] = outputCounts[output[0]] + 1
		else:
			outputCounts[output[0]] = 1

	maxCount = 0
	highestOutput = ""
	for key in outputCounts.keys():
		if outputCounts[key] > maxCount:
			maxCount = outputCounts[key]
			highestOutput = key
	if float(maxCount) / float(len(outputCounts)) >= 0.5:
		return highestOutput, float(maxCount) / float(len(outputCounts))
	else:
		return "N/A", float(maxCount) / float(len(outputCounts))

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
	global modelName
	totalCorrect, totalNum = 0, 0
	compare = pd.read_excel("Header Data/DataGroups.xlsx")
	correct = 0
	COLUMN_LABELS = {1: "Units", 2: "City", 3: "State", 4: "Address", 5: "Rate Type", 6: "Acquisition Date", 
					 7: "Maturity Date", 8: "Property Name", 9: "Square Feet", 10: "Occupancy", 11: "Loan Amount",
					 12: "Debt Service", 13: "NOI", 14: "DSCR", 15: "Market Value", 16: "LTV", 17: "Amort Start Date", 
					 18: "Property Type", 19: "Current Balance", 20: "All-In Rate", 21: "Lender", 22: "Spread", 23: "Index"}
	confidences = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	columnHeaders = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
	for column in data.columns:
		myString = str(column[0])
		if type(modelName) is str:
			guess = outputConfidence(trainColumn, modelName, myString)
		else: 
			guess = outputConfidenceMultipleModels(True, modelName, myString)
		labelIndex = get_column_label(guess[0])
		if confidences[labelIndex - 1] < guess[1]:
			confidences[labelIndex - 1] = guess[1]
			columnHeaders[labelIndex - 1] = str(column[0])
		if guess[0] in compare.columns:
			if str(column) in compare[guess[0]].apply(str).str.cat(sep=' '):
				correct += 1
		print(str(column) + ' --> ' + guess[0] + ' ' + str(guess[1]))
	print("----------------- Highest Values --------------------")
	for i in range(len(COLUMN_LABELS)):
		print(columnHeaders[i] + " --> " + COLUMN_LABELS[i + 1] + " " + str(confidences[i]))
	totalCorrect += correct
	totalNum += get_num_labels()
	print("Accuracy of Trained Categories = " + str("{:.2%}".format(correct/get_num_labels())))
	print("Total Accuracy = " + str("{:.2%}".format(correct/len(data.columns))))

COLUMN_CHECK = ['Property Name','Address','City','State','Property Type','Units','Square Feet','Occupancy', 'Acquisition Date', 'Lender', 'Maturity Date', 'Loan Amount', 'Current Balance', 'Debt Service', 'NOI', 'DSCR', 'Market Value', 'LTV', 'Amort Start Date', 'Rate Type', 'All-In Rate', 'Spread', 'Index', 'Loan Type']
def testOnSolvedCSV(goal=sys.maxsize):
	totalCorrect, totalNum = 0, 0
	missingDict, noMatchDict, unnecessaryColDict = {}, {}, {}
	for file in os.listdir("SREOs/CSVs/"):
		testFrame = standardizeSREO("SREOs/CSVs/" + file)
		testFrame.dropna(axis=COLUMN, how='all', inplace=True)

		answerCSV = pd.read_csv("SREOs/CSVs/" + file, header=0).drop(index=0).reset_index(drop=True).rename_axis(None, axis=COLUMN).replace(to_replace='\n', value=' ', regex=True)
		answerCSV.replace(to_replace='  ', value=' ', regex=True, inplace=True)
		missing = []
		for column in answerCSV.columns:
			if column not in COLUMN_CHECK:
				answerCSV.drop(columns=column, inplace=True)
			else:
				missing.append(column)

		numerator, denominator = 0, 0
		unnecessaryCol, noMatch = [], []
		for column in testFrame:
			if column in answerCSV.columns:
				if (testFrame[column]).dropna().apply(str).str.cat(sep=' ') == (answerCSV[column]).dropna().apply(str).str.cat(sep=' '):
					numerator += 1
				else:
					#print((testFrame[column]).dropna().apply(str).str.cat(sep=' '))
					#print((answerCSV[column]).dropna().apply(str).str.cat(sep=' '))
					noMatch.append(column)
				missing.remove(column)
			elif column != "Loan Type":
				denominator += 1
				unnecessaryCol.append(column)
		denominator += len(answerCSV.columns)
		
		totalCorrect += numerator
		totalNum += denominator
		if totalNum - totalCorrect > goal:
			print("Greater errors than goal, generating new model")
			return totalNum - totalCorrect
		print(file)
		if denominator != 0:
			print("Required Headers Accuracy --> " + str("{:.2%}".format(numerator/denominator)))
		if len(missing) != 0:
			print()
			print("Headers Missing:")
			for elem in missing:
				print(elem)
				if elem in missingDict:
					missingDict[elem] += 1
				else:
					missingDict[elem] = 1
		if len(noMatch) != 0:
			print()
			print("Correct Header w/ Incorrectly Matched Data:")
			for elem in noMatch:
				print(elem)
				if elem in noMatchDict:
					noMatchDict[elem] += 1
				else:
					noMatchDict[elem] = 1
		if len(unnecessaryCol) != 0:
			print()
			print("Unnecessary Incorrect Header:")
			for elem in unnecessaryCol:
				print(elem)
				if elem in unnecessaryColDict:
					unnecessaryColDict[elem] += 1
				else:
					unnecessaryColDict[elem] = 1
		print("----------------------------------------------------------------------------------------")
	print("----------------------------------------------------------------------------------------")
	totalErrors = 0
	print("Headers Missing:")
	for elem in missingDict:
		print(elem + " = " + str(missingDict[elem]))
		totalErrors += missingDict[elem]
	print()
	print("Correct Header w/ Incorrectly Matched Data:")
	for elem in noMatchDict:
		print(elem + " = " + str(noMatchDict[elem]))
		totalErrors += noMatchDict[elem]
	print()
	print("Unnecessary Incorrect Header:")
	for elem in unnecessaryColDict:
		print(elem + " = " + str(unnecessaryColDict[elem]))
		totalErrors += unnecessaryColDict[elem]
	print()
	print("Total Required Headers Accuracy --> " + str("{:.2%}".format(totalCorrect/totalNum)))
	print("Total Errors --> " + str(totalErrors))
	print("----------------------------------------------------------------------------------------")
	return totalErrors
	#return float(totalCorrect/totalNum)

def testOnSolvedCSVMultiModel(numModels=None, models=None):
	global modelName
	totalCorrect, totalNum = 0, 0
	missingDict, noMatchDict, unnecessaryColDict = {}, {}, {}
	if numModels == None:
		numModels = int(input("How many models: "))
	if models == None:
		models = []
		for i in range(numModels):
			models.append(input("Model Name: "))
	for file in os.listdir("SREOs/CSVs/"):
		testFrame = []
		for model in models:
			modelName = model
			curFrame = standardizeSREO("SREOs/CSVs/" + file)
			curFrame.dropna(axis=COLUMN, how='all', inplace=True)
			testFrame.append(curFrame)

		columnDict = {}
		for dataFrame in testFrame:
			for column in dataFrame.columns:
				if column in columnDict:
					if tuple(dataFrame[column]) in columnDict[column]:
						columnDict[column][tuple(dataFrame[column])] += 1
					else:
						columnDict[column][tuple(dataFrame[column])] = 1
				else:
					columnDict[column] = {tuple(dataFrame[column]) : 1}

		newDict = {}
		for internalDict in columnDict:
			for answer in columnDict[internalDict]:
				if columnDict[internalDict][answer] > .5 * len(models):
					newDict[internalDict] = answer
		finalDF = pd.DataFrame(newDict)

		answerCSV = pd.read_csv("SREOs/CSVs/" + file, header=0).drop(index=0).reset_index(drop=True).rename_axis(None, axis=COLUMN).replace(to_replace='\n', value=' ', regex=True)
		answerCSV.replace(to_replace='  ', value=' ', regex=True, inplace=True)

		missing = []
		for column in answerCSV.columns:
			if column not in COLUMN_CHECK:
				answerCSV.drop(columns=column, inplace=True)
			else:
				missing.append(column)

		numerator, denominator = 0, 0
		unnecessaryCol, noMatch = [], []
		for column in finalDF:
			if column in answerCSV.columns:
				if (finalDF[column]).dropna().apply(str).str.cat(sep=' ') == (answerCSV[column]).dropna().apply(str).str.cat(sep=' '):
					numerator += 1
				else:
					#print((testFrame[column]).dropna().apply(str).str.cat(sep=' '))
					#print((answerCSV[column]).dropna().apply(str).str.cat(sep=' '))
					noMatch.append(column)
				missing.remove(column)
			elif column != "Loan Type":
				denominator += 1
				unnecessaryCol.append(column)
		denominator += len(answerCSV.columns)
		
		totalCorrect += numerator
		totalNum += denominator
		
		print(file)
		if denominator != 0:
			print("Required Headers Accuracy --> " + str("{:.2%}".format(numerator/denominator)))
		if len(missing) != 0:
			print()
			print("Headers Missing:")
			for elem in missing:
				print(elem)
				if elem in missingDict:
					missingDict[elem] += 1
				else:
					missingDict[elem] = 1
		if len(noMatch) != 0:
			print()
			print("Correct Header w/ Incorrectly Matched Data:")
			for elem in noMatch:
				print(elem)
				if elem in noMatchDict:
					noMatchDict[elem] += 1
				else:
					noMatchDict[elem] = 1
		if len(unnecessaryCol) != 0:
			print()
			print("Unnecessary Incorrect Header:")
			for elem in unnecessaryCol:
				print(elem)
				if elem in unnecessaryColDict:
					unnecessaryColDict[elem] += 1
				else:
					unnecessaryColDict[elem] = 1
		print("----------------------------------------------------------------------------------------")
	print("----------------------------------------------------------------------------------------")
	totalErrors = 0
	print("Headers Missing:")
	for elem in missingDict:
		print(elem + " = " + str(missingDict[elem]))
		totalErrors += missingDict[elem]
	print()
	print("Correct Header w/ Incorrectly Matched Data:")
	for elem in noMatchDict:
		print(elem + " = " + str(noMatchDict[elem]))
		totalErrors += noMatchDict[elem]
	print()
	print("Unnecessary Incorrect Header:")
	for elem in unnecessaryColDict:
		print(elem + " = " + str(unnecessaryColDict[elem]))
		totalErrors += unnecessaryColDict[elem]
	print()
	print("Total Required Headers Accuracy --> " + str("{:.2%}".format(totalCorrect/totalNum)))
	print("Total Errors --> " + str(totalErrors))
	print("----------------------------------------------------------------------------------------")
	return totalCorrect

def trainAgainstSolvedCSV(isNewModel, newModelName):
	global modelName 
	modelName = "Model/9errors"
	trainingData = pd.DataFrame(columns=['label','text'])
	if isNewModel:
		for file in os.listdir("SREOs/CSVs/"):
			testFrame = extractSREO("SREOs/CSVs/" + file)
			answerRow = pd.read_csv("SREOs/CSVs/" + file, header=0).drop(index=0).reset_index(drop=True).rename_axis(None, axis=COLUMN).replace(to_replace='\n', value=' ', regex=True)
			tempTrainingData = pd.DataFrame(columns=['label','text'])

			for i in range(len(testFrame.columns)):
				if "." in answerRow.columns[i]:
					tempTrainingData.at[i,'label'] = str(answerRow.columns[i]).split(".")[0]
				else:
					tempTrainingData.at[i,'label'] = str(answerRow.columns[i])
				if "." in testFrame.columns[i]:
					tempTrainingData.at[i, 'text'] = str(testFrame.columns[i][0]).split(".")[0]
				else:
					tempTrainingData.at[i,'text'] = str(testFrame.columns[i][0])
			tempTrainingData.dropna(axis=ROW, how='all', inplace=True)
			tempTrainingData.dropna(axis=COLUMN, how='all', inplace=True)
			trainingData = pd.concat([trainingData, tempTrainingData], ignore_index=True)
		trainingData.to_csv("trainingData.csv", index=False)
	else:
		trainingData = pd.read_csv("trainingData.csv")
		trainingData = trainingData.sample(frac=1)
		trainingData.to_csv("trainingData.csv",index=False)
	trainModel(True, isNewModel, newModelName, "trainingData.csv", 1)
