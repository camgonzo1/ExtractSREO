from cmath import nan
from fileinput import filename
from lib2to3.pytree import convert
from re import L
import string
from numpy import dtype
import pandas as pd
import camelot
from prepareData import *
from trainModel import *

ROW, COLUMN = 0, 1
PERMITTED_FORMATS = ["csv", "xlsx", "pdf"]
HEADER_MODEL, DATA_MODEL = 'headerTest', ''
DATA_ANALYSIS, HEADER_ANALYSIS  = 1, 2
NO_PRINT, PRINT = 0, 1
modelName = None

# extractSREO()
# Parameters: curFilePath (string) --> conatins the current path to the desired file for importation
# Return: sreoData (pandas DataFrame) --> conatins data from file
# Description: Pulls data from csv or excel sheet and stores in pandas dataframe
def extractSREO(curFilePath):
    #Determines File Type
    splitPath = curFilePath.split(".")
    fileType = splitPath[len(splitPath) - 1]

    # Reads Data into Pandas DataFrame
    if fileType not in PERMITTED_FORMATS:
        raise TypeError("Please input compatible file type!")
    elif fileType == "csv":
        sreoData = pd.read_csv(curFilePath, header=None)
    elif fileType == "xlsx":
        sreoData = pd.read_excel(curFilePath, header=None)
    elif fileType == "pdf":
        tables = camelot.read_pdf(curFilePath, flavor='stream')
        tables.export(curFilePath, f='csv', compress=True)
        sreoData = tables[0].df
    print(sreoData)
    sreoData.mask(inplace=True)
    sreoData.dropna(axis=ROW, how='all', inplace=True)
    sreoData.dropna(axis=COLUMN, how='all', inplace=True)
    sreoData = sreoData.reset_index(drop=True).rename_axis(None, axis=COLUMN)
    print(sreoData)

    # Reformat DataFrame to Apply Header
    index = getHeaderIndex(sreoData)
    if index == -1:
        raise IndexError("No header row found in " + curFilePath + "! Please try again or enter file in different compatible format.")
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
        if testInput(modelName, HEADER_ANALYSIS, rowString, NO_PRINT) == "Valid":
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
    for dataColumn in sreoDataFrame:
        relevantCategory = testInput(modelName, DATA_ANALYSIS, sreoDataFrame[dataColumn][0], NO_PRINT)
        if relevantCategory != "N/A":
            sreoTemplate.insert(column=relevantCategory)

    # Notify Abstraction Here
    return sreoTemplate.to_excel()


#################### For Testing ############################
FILES = ["SREOs/2022 Lawrence S Connor REO Schedule.csv", "SREOs/2022 Lawrence S Connor REO Schedule.xlsx", "SREOs/AP - REO excel 202112.csv", "SREOs/AP - REO excel 202112.xlsx", "SREOs/NorthBridge.csv", "SREOs/NorthBridge.xlsx", "SREOs/RPA REO Schedule - 01.31.2022.csv", "SREOs/RPA REO Schedule - 01.31.2022.xlsx"]
CUR_FILE = "SREOs/2022 Lawrence S Connor REO Schedule.pdf"
def main():
    global modelName
    columnOrHeader = input("1 for Column training, 2 for Header training, 3 for testing existing model, 4 to test SREOs, 5 to quit: ")
    while(int(columnOrHeader) != 5):
        if columnOrHeader == "4":
            modelName = input("Model Name: ")
            if input("Test All Files (Y/N): ") == 'Y':
                for file in FILES:
                    print(extractSREO(file))
            elif input("Test Current File (Y/N): ") == 'Y':
                print(extractSREO(CUR_FILE))
        elif columnOrHeader == "3":
            columnOrHeader = input("1 for Column model, 2 for Header model: ")
            modelName = input("Model Name: ")
            testInput(modelName, columnOrHeader, input("Input test string: "), 1)
        else:
            numRepeats = input("Number of Repeats: ")
            createData(columnOrHeader, 'trainingData.csv', int(numRepeats))
            createData(columnOrHeader, 'testingData.csv', int(int(numRepeats) / 5))
            print()
            trainModel(columnOrHeader, "trainingData.csv", "testingData.csv")
        columnOrHeader = input("1 for Column training, 2 for Header training, 3 for testing existing model, 4 to test SREOs, 5 to quit: ")

if __name__ == "__main__":
    main()