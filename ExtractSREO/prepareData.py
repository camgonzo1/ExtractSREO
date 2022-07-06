from lib2to3.pytree import convert
from re import L
import os
import random
from tkinter.tix import COLUMN
from numpy import dtype
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))
COLUMN_DATA = {1: ("Units", 'units.txt'), 2: ("City", 'city.txt'), 3: ('State', 'state.txt'), 4: ("Address", 'address.txt'), 5: ("Rate Type", 'rate type.txt'), 6: ("Acquisition Date", 'acquisition date.txt'),
                 7: ("Maturity Date",'maturity date.txt'), 8: ("Property Name", 'property name.txt'), 9: ("Square Feet", 'square feet.txt'), 10: ("Occupancy", 'occupancy.txt'), 11: ("Loan Amount", 'loan amount.txt'), 
                 12: ("Debt Service", 'debt service.txt'), 13: ('NOI', 'noi.txt'), 14: ("DSCR", 'dscr.txt'), 15: ("Market Value", 'market value.txt'), 16: ("LTV", 'ltv.txt'), 17: ("Amort Start Date", 'amort start date.txt'), 
                 18: ("Property Type", "property type.txt"), 19: ("Current Balance", 'current balance.txt'), 20: ("All-In Rate", 'all in rate.txt'), 21: ("Lender", "lender.txt"), 22: ("Spread", 'spread.txt'), 23: ("Index", 'index.txt')}
HEADER_DATA = {2: ("Valid", 'validHeaderNames.txt')}
DATA_GROUP, FILE, HEADER_KEY, NUM_DATA = 0, 1, 2, 1000

def createData(columnOrHeader, fileName, numRepeats):
	print("Create Data Started!")
	trainingData = pd.DataFrame(columns=['label','text'])
	if(columnOrHeader == 1):
		if input("Would you like to repopulate training values in .txt files (Y/N): ") == 'Y':
			populateNecessaryFiles()
			print("Files populated!")
		print("|-----------------------|")
		print("|", end="")
		for i in range(len(COLUMN_DATA)):
			trainingData = generateAndRandomize(trainingData, True, i + 1, numRepeats)
			print("X", end="") # Loading Bar For Visuals
	elif(columnOrHeader == 2):
		trainingData = generateAndRandomize(trainingData, False, HEADER_KEY, numRepeats)
	print("|")
	print("Done Training!")
	trainingData.to_csv(fileName, index=False)
	return trainingData

def generateAndRandomize(trainingData, COLUMNS, dictIndex, numRepeats):
	# Determines SREO Header or SREO Data Training
	if COLUMNS:
		category = COLUMN_DATA[dictIndex]
		iterations = 2
	else:
		category = HEADER_DATA[dictIndex]
		iterations = random.randint(15, 25)

	# Executes Data Fabrication
	with open("Header data/" + category[FILE], "r") as headerFile:
		dataHeaders = headerFile.read().splitlines()
	with open("Training Data/" + category[FILE], "r") as trainingFile:
		dataValues = trainingFile.read().splitlines()
	exportString = ''
	for i in range(numRepeats):
		if(random.randint(0, 9)) != 0: exportString = dataHeaders[random.randint(0,len(dataHeaders) - 1)] + " "
		for j in range(iterations):
			if random.randint(0,9) == 0: exportString += "nan "
			exportString += dataValues[random.randint(0, len(dataValues) - 1)] + " "
		df2 = pd.DataFrame({'label' : category[DATA_GROUP], 'text' : exportString}, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index = True)
	return trainingData

def populateNecessaryFiles():
	print("|----------------|")
	print("|", end="")
	with open("Training Data/units.txt", "w") as curFile:
		for i in range(NUM_DATA):
			if random.randint(0,9) == 0: exportString = "nan"
			else: exportString = str(random.randint(1, 1000))
			curFile.write(exportString + "\n")
	print("X", end="")
	
	dateFiles = ["acquisition date.txt", "maturity date.txt", "amort start date.txt"]
	for file in dateFiles:
		with open("Training Data/" + file, "w") as curFile:
			for i in range(NUM_DATA):
				randInt = random.randint(0,9)
				if randInt == 0: exportString = "nan"
				elif randInt < 4: exportString = str(random.randint(1950, 2030))
				elif randInt < 7: exportString = str(random.randint(1, 13)) + "/" + str(random.randint(1, 32)) + "/" + str(random.randint(1950, 2050))
				else: exportString = str(random.randint(1, 13)) + "-" + str(random.randint(1, 32)) + "-" + str(random.randint(1950, 2050)) + " 00:00:00"
				curFile.write(exportString + "\n")
		print("X", end="")

	with open("Training Data/property name.txt", "w") as curFile:
		with open("Training Data/address.txt", "r") as addys:
			addyData = addys.read().splitlines()
		for i in range(NUM_DATA):
			randInt = random.randint(0,9)
			if randInt == 0: exportString = "nan"
			else:
				exportString = ""
				if random.randint(0, 2) == 0: exportString += str(random.randint(1, 10000)) + " "
				elif random.randint(0, 2) == 0: exportString += addyData[random.randint(0, len(addyData) - 1)] + " at "
				exportString += addyData[random.randint(0, len(addyData) - 1)]
			curFile.write(exportString + "\n")
	print("X", end="")

	sqFeetEnds = ["", "ft", "ft.", "feet", " feet", " ft", " ft."]
	with open("Training Data/square feet.txt", "w") as curFile:
		for i in range(NUM_DATA):
			if(random.randint(0, 10) == 0): exportString += "nan"
			else: exportString = str(random.randint(1, 100000)) + sqFeetEnds[random.randint(0, len(sqFeetEnds) - 1)]
			curFile.write(exportString + "\n")
	print("X", end="")

	percentageFiles = ["occupancy.txt", "ltv.txt", "all in rate.txt"]
	for file in percentageFiles:
		with open("Training Data/" + file, "w") as curFile:
			for i in range(NUM_DATA):
				if(random.randint(0, 9) == 0): exportString = "nan"
				else: 
					exportString = str(random.randint(1, 100))
					if random.randint(0,2) == 0: exportString += "." + str(random.randint(1,100))
					if random.randint(0,3) < 2: exportString += "%"
				curFile.write(exportString + "\n")
		print("X", end="")
	
	moneyFiles = ["loan amount.txt", "debt service.txt", "noi.txt", "market value.txt", "current balance.txt"]
	for file in moneyFiles:
		with open("Training Data/" + file, "w") as curFile:
			for i in range(NUM_DATA):
				if random.randint(0, 9) == 0: exportString = "nan"
				else:
					exportString = ""
					if random.randint(0, 4) < 3: exportString += "$"
					if random.randint(0, 2) == 0: exportString += str(random.randint(0, 10000000))
					else: exportString += "{:,}".format(random.randint(0, 100000000))
					if random.randint(0, 2) == 0: exportString += "." + str(random.randint(0, 100))
				curFile.write(exportString + "\n")
		print("X", end="")

	with open("Training Data/dscr.txt", "w") as curFile:
		for i in range(NUM_DATA):
			if random.randint(0, 9) == 0: exportString += "nan"
			else: exportString = str(random.randint(0,10)) + "." + str(random.randint(1,10000))
			curFile.write(exportString + "\n")
	print("X", end="")

	with open("Training Data/spread.txt", "w") as curFile:
		for i in range(NUM_DATA):
			if random.randint(0, 9) == 0: exportString += "nan"
			else: exportString = exportString = str(random.randint(0, 25) * 10) + " BPs"
			curFile.write(exportString + "\n")
	print("X|")
	return

##############################################################################################################################################################################################################################################################

FILE_LIST = ["2021 12 14_MWest_Debt Schedule.csv", "2022 Lawrence S Connor REO Schedule.csv", "AP - REO excel 202112.csv", "Copy of Carlos & Vera Koo - RE Schedule - March 2022 v.2.csv", "David T. Matheny and Susan Matheny - RE Schedule 5.19.21.csv", 
			 "Mark Johnson - RE Schedule September 2020.csv", "NorthBridge.csv", "RPA REO Schedule - 01.31.2022.csv", "Simpson REO Schedule (12-31-21).csv",
			 "SimpsonHousingLLLP-DebtSummary-2021-09-07.csv", "SP Inc., SP II and SP III - RE Schedule 11.20.2019.csv", "SREO Export Template v2 - final.csv", "Stoneweg.csv", "TCG - 2022 Fund XI REO Schedule.csv"]

def trainOnCSV():
	csvTrainingData = pd.DataFrame(columns=['label','text'])
	#for file in os.listdir("SREOs/CSVs/"):
	for file in FILE_LIST:
		curCSV = pd.read_csv("SREOs/CSVs/" + file, header=None)
		answerRow = ((curCSV.iloc[0])).apply(str)
		for i in range(len(answerRow)):
			if answerRow[i] == "nan":
				answerRow[i] = "N/A"
		curCSV.replace('\n', '', regex=True, inplace=True)
		curCSV.mask(curCSV == '', inplace=True)
		curCSV.dropna(axis=0, how="all", inplace=True)
		curCSV.dropna(axis=1, how="all", inplace=True)
		curCSV = curCSV.reset_index(drop=True).rename_axis(None, axis=1)
		curCSV.columns = [curCSV.iloc[1]]
		curCSV = curCSV[2:].reset_index(drop=True).rename_axis(None, axis=1)


		for row in range(int(len(curCSV.index)/2)):
			index, count, exportString = row*2, 0, ''
			for col in curCSV.columns:
				exportString = str(col[0]) + " " + str(curCSV.loc[:,col][index]) + " " + str(curCSV.loc[:,col][index + 1])
				df2 = pd.DataFrame({'label' : str(answerRow[count]), 'text' : exportString.strip('"')}, index=[1])
				csvTrainingData = pd.concat([csvTrainingData, df2],ignore_index = True)
				count += 1
	print("Done Training")
	csvTrainingData.to_csv("extractedTrainingData.csv", index=False)

if __name__ == "__main__":
	populateNecessaryFiles()