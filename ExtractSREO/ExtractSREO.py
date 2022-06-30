from cmath import nan
from fileinput import filename
from lib2to3.pytree import convert
import os
from re import L
import string
from numpy import dtype
import pandas as pd
import camelot
from prepareData import *
from trainModel import *

ROW, COLUMN = 0, 1
PERMITTED_FORMATS = ["csv", "xlsx"]
HEADER_MODEL, DATA_MODEL = 'headerTest', ''
DATA_ANALYSIS, HEADER_ANALYSIS  = 1, 2
NO_PRINT, PRINT = 0, 1
modelName = None
totalCorrect, totalNum = 0, 0

# Name: extractSREO()
# Parameters: curFilePath (string) --> conatins the current path to the desired file for importation
# Return: sreoData (pandas DataFrame) --> conatins data from file
# Description: Pulls data from csv or excel sheet and stores in pandas dataframe
def extractSREO(curFilePath):
    #Determines File Type 
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
    elif fileType == "pdf":
        tables = camelot.read_pdf(curFilePath, flavor='stream', row_tol=7)
        tables.export(curFilePath, f='csv', compress=True)
        sreoData = tables[0].df
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
    sreoTemplate = pd.DataFrame(columns=['1','2','3','4','5','6','7','8'])
    for dataColumn in sreoDataFrame.columns:
        myString = str(dataColumn[0]) + " " + (sreoDataFrame[dataColumn]).apply(str).str.cat(sep=' ')
        relevantCategory = testInput(modelName, DATA_ANALYSIS, myString, NO_PRINT)
        if relevantCategory != "N/A":
            sreoTemplate.insert(column=relevantCategory)
    print(sreoTemplate)

    # Notify Abstraction Here
    return sreoTemplate.to_excel()

# Name: standardizeSREO()
# Parameters: sreoFilePath (string) --> conatins the current path to the desired file for importation
# Return: fillTemplate(extractSREO(sreoFilePath)) (.xlsx) --> contains the populated SREO standard template
# Description: Takes in a file path, pulls and analyzes data and restrustures
#              data in a standardized model which it exports in a .xlsx format fllowing a 
#              notification to the abstraction team. 
def standardizeSREO(sreoFilePath):
    return fillTemplate(extractSREO(sreoFilePath))

#################### For Testing ############################

def testConfidence(data):
    global totalCorrect
    global totalNum
    compare = pd.read_excel("Header Data/DataGroups.xlsx")
    correct = 0
    for column in data.columns:
        myString = str(column[0]) + " " + (data[column]).apply(str).str.cat(sep=' ')
        guess = outputConfidence(modelName, DATA_ANALYSIS, myString, NO_PRINT)
        if guess[0] in compare.columns:
            if str(column[0]) in compare[guess[0]].apply(str).str.cat(sep=' '):
                correct += 1
        print(str(column[0]) + ' --> ' + guess[0] + ' ' + str(guess[1]))
    totalCorrect += correct
    totalNum += getNumLabels()
    print("Accuracy of Trained Categories = " + str("{:.2%}".format(correct/getNumLabels())))
    print("Total Accuracy = " + str("{:.2%}".format(correct/len(data.columns))))


FILES = ["SREOs/2022 Lawrence S Connor REO Schedule.csv", "SREOs/2022 Lawrence S Connor REO Schedule.xlsx", "SREOs/AP - REO excel 202112.csv", "SREOs/AP - REO excel 202112.xlsx", "SREOs/NorthBridge.csv", "SREOs/NorthBridge.xlsx", "SREOs/RPA REO Schedule - 01.31.2022.csv", "SREOs/RPA REO Schedule - 01.31.2022.xlsx", "SREOs/Simpson REO Schedule (12-31-21).csv", "SREOs/Simpson REO Schedule (12-31-21).xlsx", "SREOs/SREO Export Template v2 - final.csv", "SREOs/SREO Export Template v2 - final.xlsx"]
CUR_FILE = "SREOs/2022 Lawrence S Connor REO Schedule.csv"
def main():
    global modelName
    columnOrHeader = input("1 for Column training, 2 for Header training, 3 for testing existing model, 4 to test SREOs, 5 to quit: ")
    while(int(columnOrHeader) != 5):
        if columnOrHeader == "4":
            modelName = input("Model Name: ")
            if input("Test All Files (Y/N): ") == 'Y':
                for file in FILES:
                    print('------------------------------------------------------------')
                    data = extractSREO(file)
                    print(data)
                    testConfidence(data)
                    print('------------------------------------------------------------')
                print("Total Accuracy of Trained Categories = " + str("{:.2%}".format(totalCorrect/totalNum)))
            elif input("Test Current File (Y/N): ") == 'Y':
                print('------------------------------------------------------------')
                data = extractSREO(CUR_FILE)
                print(data)
                testConfidence(data)
                print('------------------------------------------------------------')
        elif columnOrHeader == "3":
            columnOrHeader = input("1 for Column model, 2 for Header model: ")
            modelName = input("Model Name: ")
            print(outputConfidence(modelName, columnOrHeader, input("Input test string: ")))
        else:
            numRepeats = input("Number of Repeats: ")
            createData(columnOrHeader, 'trainingData.csv', int(numRepeats))
            print()
            trainModel(columnOrHeader, "trainingData.csv", "testingData.csv")
        columnOrHeader = input("\n1 for Column training, 2 for Header training, 3 for testing existing model, 4 to test SREOs, 5 to quit: ")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()