# File Name: ExtractSREO.py
# Authors: Ryan Dunn and Cam Gonzalez
# Description: This file executes the SREO importation, information extraction, and notificication for 
#              the LoanBoss online application on the back end.
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

ROW, COLUMN = 0, 1 # Values Indicating DataFrame Axis'
PERMITTED_FORMATS = ["csv", "xlsx"]
HEADER_MODEL, DATA_MODEL = 'headerTest', '' # Trained AI Models for Data Interpretation
DATA_ANALYSIS, HEADER_ANALYSIS = 1, 2 
NO_PRINT, PRINT = 0, 1
modelName = None # For testing
totalCorrect, totalNum = 0, 0

# Name: extractSREO()
# Parameters: curFilePath (string) --> conatins the current path to the desired file for importation
# Return: sreoData (pandas DataFrame) --> conatins data from file
# Description: Pulls data from csv or excel sheet and stores in pandas dataframe
def extractSREO(curFilePath):
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
        if testInput(HEADER_MODEL, HEADER_ANALYSIS, rowString, NO_PRINT) == "Valid":
            return i
    return -1

# Name: fillTemplate()
# Parameters: sreoDataFrame (pandas DataFrame) --> conatins semi-filtered data from an SREO
# Return: sreoTemplate.to_excel() (.xlsx) --> contains the populated SREO standard template
# Description: Takes in a nonstandardized SREO and analyzes using a NLP model to restrusture 
#              data in a standardized model which it exports in a .xlsx format fllowing a 
#              notification to the abstraction team. 
def fillTemplate(sreoDataFrame):
    sreoTemplate = pd.DataFrame(columns=['Property Name','Street Address','City','State','Property Type','Units','Square Footage','Occupancy', 'Acquisition Date', 'Lender', 'Maturity', 'Loan Amount', 'Current Balance', 'Debt Service', 'NOI', 'DSCR', 'Market Vaue', 'LTV', 'Amort Start', 'Rate Type', 'All-In', 'Spread', 'Index'])
    for dataColumn in sreoDataFrame.columns:
        # old
        #myString = str(dataColumn[0]) + " " + (sreoDataFrame[dataColumn].apply(str).str.cat(sep=' ')

        #new
        data = sreoDataFrame[dataColumn].dropna()
        if len(data) > 3:
            myString = str(dataColumn[0]) + " " + (data.apply(str)[:3]).str.cat(sep=' ')
        else :
            myString = str(dataColumn[0]) + " " + data.apply(str).str.cat(sep=' ')

        relevantCategory = testInput(modelName, DATA_ANALYSIS, myString, NO_PRINT)
        if relevantCategory != "N/A":
            sreoTemplate.insert(column=relevantCategory)

    # For Testing
    print(sreoTemplate)
    # Notify Abstraction Here
    return sreoTemplate.to_excel()

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
def testConfidence(data):
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
        myString = str(column[0]) + " " + ((data[column]).dropna().apply(str)[:3]).str.cat(sep=' ')
        guess = outputConfidence(modelName, DATA_ANALYSIS, myString, NO_PRINT)
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
def runTests():
    global modelName
    columnOrHeader = int(input("1 for Column training, 2 for Header training, 3 for testing existing model, 4 to test SREOs, 5 to quit: "))
    while(int(columnOrHeader) != 5):
        if columnOrHeader == 4:
            modelName = input("Model Name: ")
            if input("Test All Files (Y/N): ") == 'Y':
                for file in FILES:
                    print('------------------------------------------------------------')
                    data = extractSREO(file)
                    print(data.to_string())
                    testConfidence(data)
                    print('------------------------------------------------------------')
                print("Total Accuracy of Trained Categories = " + str("{:.2%}".format(totalCorrect/totalNum)))
            elif input("Test Current File (Y/N): ") == 'Y':
                print('------------------------------------------------------------')
                data = extractSREO(CUR_FILE)
                print(data)
                testConfidence(data)
                print('------------------------------------------------------------')
        elif columnOrHeader == 3:
            columnOrHeader = int(input("1 for Column model, 2 for Header model: "))
            modelName = input("Model Name: ")
            print(outputConfidence(modelName, columnOrHeader, input("Input test string: "), 1))
        else:
            numRepeats = input("Number of Repeats: ")
            createData(columnOrHeader, 'trainingData.csv', int(numRepeats))
            print()
            trainModel(columnOrHeader, "trainingData.csv", "testingData.csv")
        columnOrHeader = int(input("\n1 for Column training, 2 for Header training, 3 for testing existing model, 4 to test SREOs, 5 to quit: "))

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    runTests()