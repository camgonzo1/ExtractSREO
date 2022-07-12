"""
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
		for i in range(numRepeats):
			trainingData = generateAndRandomize(trainingData, True, random.randint(1, len(COLUMN_DATA)), 1)
			if (numRepeats - (i + 1)) % numRepeats / 23 == 0: print("X", end="") # Loading Bar For Visuals
		#for i in range(len(COLUMN_DATA)):
			#trainingData = generateAndRandomize(trainingData, True, i + 1, numRepeats)
			#print("X", end="") # Loading Bar For Visuals
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
"""
"""
from lib2to3.pytree import convert
from re import L
import os
import random
from numpy import dtype
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open("Training Data/property name.txt", "w") as curFile:
		with open("Training Data/address.txt", "r") as addys:
			addyData = addys.read().splitlines()
		for i in range(10000):
			randInt = random.randint(0,9)
			if randInt == 0: exportString = "nan"
			else:
				exportString = ""
				if random.randint(0, 2) == 0: exportString += str(random.randint(1, 10000)) + " "
				elif random.randint(0, 2) == 0: exportString += addyData[random.randint(0, len(addyData) - 1)] + " at "
				exportString += addyData[random.randint(0, len(addyData) - 1)]
			curFile.write(exportString + "\n")
with open('Training Data/address.txt') as f: address = f.read().splitlines()	
with open('Training Data/city.txt') as f: city = f.read().splitlines()	
with open('Training Data/property type.txt') as f: propertyType = f.read().splitlines()
with open('Training Data/state.txt') as f: state = f.read().splitlines()
with open('Training Data/index.txt') as f: index = f.read().splitlines()	
with open('Training Data/lender.txt') as f: lender = f.read().splitlines()
with open('Training Data/property name.txt') as f: propertyName = f.read().splitlines()
with open('Training Data/rate type.txt') as f: rateType = f.read().splitlines()
with open('Training Data/validHeaderNames.txt') as f: valid = f.read().splitlines()
with open('Training Data/invalidHeaderNames.txt') as f: invalid = f.read().splitlines()

CATEGORY, HEADERS, CHOICES = 0, 1, 2
COLUMN_INFO = {1: ("Loan Amount", ["Loan Amount", "Orig. Loan Amount", "Original Loan Amount", "OG Loan Amount"]), 
				 2: ("Debt Service", ["Debt Service", "Debt Service Value", "Total Debt Service", "Annual Debt Service"]),
				 3: ("NOI", ["NOI", "Net Operating Income", "Net Income", "Current NOI", "N.O.I.", "Current N.O.I.", "Current Net Operating Income"]),
				 4: ("Market Value", ["Market Value", "MV", "Value"]), 
				 5: ("Current Balance", ["Loan Amount", "Outstanding Loan Amount", "Principal Balance", "OPB", "Outstanding Principal Balance", "Current Balance", "Balance", "Current Debt"]),
				 6: ("Occupancy", ["Occupancy", "Current Occupancy", "Occupancy Status", "Current Occupancy (%)", "% Occupied", "% Occupancy", "Occupancy %", "Occupancy at end of quarter"]),
				 7: ("LTV", ["LTV", "Loan-To-Value", "Loan To Value"]),
				 8: ("All-In Rate", ["All-In", "All-In Rate", "Rate", "All In", "All In Rate", "All-in"]),
				 9: ("Acquisition Date", ["Acquisition Date", "Purchase Date", "Date of Acquisition", "Acquistion", "Acquired", "Year Acquired", "Date Acquired", "Origination Date", "Origination", "Year Originated", "Acquisition Date (yr)"]),
				 10: ("Maturity Date", ["Maturity Date", "Maturity", "Loan Matures", "Matures", "Date of Maturity", "Date Matures", "Maturation Date"]),
				 11: ("Amort Start Date", ["Amort Start Date", "Amortization Start Date", "Amort Date", "Amortization Date", "Amort Start", "Amortization Start"]),
				 12: ("DSCR", ["DSCR", "Debt Service Coverage", "Total DCR", "DCR", "Total DSCR", "Debt Coverage Ratio", "Debt Service Ratio", "Debt Coverage"], 10),
				 13: ("Units", ["Units", "#units", "# of Units", "Number of Units", "Unit Count"], 1000),
				 14: ("Square Feet", ["Square Footage", "Square Feet", "Sq. Feet", "Sq. Ft.", "Feet", "Sq. Footage"]),
				 15: ("Spread", ["Spread", "Credit Spread"]),
				 16: ("Address", ["Property Location", "Location", "Address", "Street Location", "Street Address", "Property Address", "Street", "Full Property Address", "Property Street Address City State Zip"], address),
				 17: ("City", ["City", "Town"], city),
				 18: ("Property Type", ["Property Type", "Type of Property", "Type", "Asset Type"], propertyType),
				 19: ("State", ["State", "Providence", "Territory"], state),
				 20: ("Index", ["Index", "Interest Rate Index", "Rate Index"], index),
				 21: ("Lender", ["Lender", "Mortgage Holder", "Mortgage Lender"], lender),
				 22: ("Property Name", ["Property Name", "Name", "Property", "Property Number", "ID", "Property ID"], propertyName),
				 23: ("Rate Type", ["Loan Type", "Type of Loan", "Fixed or Floating", "Type", "Rate Type", "Type of Rate", "Interest Rate Type", "Type of Interest Rate"], rateType)}
HEADER_INFO = {1: ("Valid", valid, valid),
			   2: ("Invalid", invalid, invalid)}


def createData(columnOrHeader, fileName, numRepeats):
	trainingData = pd.DataFrame(columns=['label','text'])
	if(columnOrHeader == 1):
		for i in range(numRepeats):
			rand = random.randint(1,len(COLUMN_INFO))
			if(random.randint(0,15) == 0): trainingData = genData(16, trainingData, COLUMN_INFO, stringGen(choices=COLUMN_INFO[16][CHOICES]), iterations=2)
			if(random.randint(0,15) == 0): trainingData = genData(22, trainingData, COLUMN_INFO, stringGen(choices=COLUMN_INFO[22][CHOICES]), iterations=2)
			if rand <= 5: trainingData = genData(rand, trainingData, COLUMN_INFO, moneyGen(minAmnt=0, maxAmnt=10000000), iterations=2)
			elif rand <= 8:
				if rand == 8: trainingData = genData(rand, trainingData, COLUMN_INFO, percentGen(minP=0, maxP=5), iterations=2)
				else: trainingData = genData(rand, trainingData, COLUMN_INFO, percentGen(minP=0, maxP=100), iterations=2)
			elif rand <= 11: trainingData = genData(rand, trainingData, COLUMN_INFO, dateGen(minYr=1950, maxYr=2050), iterations=2)
			elif rand == 12: trainingData = genData(rand, trainingData, COLUMN_INFO, numGen(minNum=0, maxNum=10, units=None), iterations=2)
			elif rand == 13: trainingData = genData(rand, trainingData, COLUMN_INFO, numGen(minNum=0, maxNum=1000, units=None), iterations=2)
			elif rand == 14: trainingData = genData(rand, trainingData, COLUMN_INFO, numGen(minNum=0, maxNum=100000, units=["", "ft", "ft.", "feet", " feet", " ft", " ft."]), iterations=2)
			elif rand == 15: trainingData = genData(rand, trainingData, COLUMN_INFO, numGen(minNum=0, maxNum=250, units=["", "BPs", " BPs"]), iterations=2)
			else: trainingData = genData(rand, trainingData, COLUMN_INFO, stringGen(choices=COLUMN_INFO[rand][CHOICES]), iterations=2)
			if((numRepeats - (i + 1)) % (numRepeats / 50) == 0): print("X", end="")
	elif(columnOrHeader == 2): 
		for i in range(numRepeats):
			rand = random.randint(1,len(HEADER_INFO))
			trainingData = genData(rand, trainingData, HEADER_INFO, stringGen(choices=COLUMN_INFO[rand][CHOICES]), iterations=random.randint(15,25))
	print()
	trainingData.to_csv(fileName, index=False)

def genData(dictIndex, trainingData, columnHeader, function, iterations):
	headers = columnHeader[dictIndex][HEADERS]
	exportString = ""
	if random.randint(0, 10) != 0: exportString += headers[random.randint(0,len(headers) - 1)] + " "
	for j in range(iterations):
		if random.randint(0, 10) == 0: exportString += "nan "
		else:
			exportString += function + " "
	df2 = pd.DataFrame({ 'label' : columnHeader[dictIndex][CATEGORY], 'text' : exportString}, index=[1])
	trainingData = pd.concat([trainingData, df2],ignore_index=True)
	return trainingData

def moneyGen(minAmnt, maxAmnt):
	exportString = ""
	if random.randint(0, 2) == 0: exportString += "$"
	if random.randint(0, 2) == 0: exportString += str(random.randint(minAmnt, maxAmnt + 1))
	else: exportString += "{:,}".format(random.randint(minAmnt, maxAmnt + 1))
	if random.randint(0, 2) == 0: exportString += "." + str(random.randint(0, 100))
	return exportString

def dateGen(minYr, maxYr):
	randInt = random.randint(0,3)
	if randInt == 0: exportString = str(random.randint(minYr, maxYr + 1))
	elif randInt == 1: exportString = str(random.randint(1, 13)) + "/" + str(random.randint(1, 32)) + "/" + str(random.randint(minYr, maxYr + 1))
	else: exportString = str(random.randint(1, 13)) + "-" + str(random.randint(1, 32)) + "-" + str(random.randint(minYr, maxYr + 1)) + " 00:00:00"
	return exportString

def percentGen(minP, maxP):
	exportString = str(random.randint(minP, maxP))
	if random.randint(0,2) == 0: exportString += "." + str(random.randint(0,100))
	if random.randint(0,2) == 0: exportString += "%"
	return exportString

def numGen(minNum, maxNum, units):
	exportString = str(random.randint(minNum, maxNum + 1))
	if units != None and random.randint(0, 10) != 0: exportString += units[random.randint(0, len(units) - 1)]
	return exportString

def stringGen(choices):
	return choices[random.randint(0, len(choices) - 1)]

"""
from lib2to3.pytree import convert
from re import L
import os
import random
from numpy import dtype
import pandas as pd
from ExtractSREO import *
import userInterface as userInterface
from PyQt5 import QtCore, QtGui, QtWidgets

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('Training Data/address.txt') as f: streets = f.read().splitlines()	
with open('Training Data/city.txt') as f: cities = f.read().splitlines()
with open('Training Data/property type.txt') as f: propertyTypes = f.read().splitlines()	

#Creates randomized Address column values numRepeats times and adds them to trainingData
def createAddresses():
	ends = ["Road", "Rd.", "rd.", "Rd", "Boulevard", "blvd.", "Blvd", "Street", "St.", "St", "Way", "Circle", "Ave.", "Ave", "Avenue", "Drive", "Dr.", "Dr"];
	addressHeaders = ["Property Location", "Location", "Address", "Street Location", "Street Address", "Property Address", "Street", "Full Property Address", "Property Street Address City State Zip"];
	exportString = ""
	if(random.randint(0, 10)) != 0: exportString = addressHeaders[random.randint(0,8)] + " "
	for j in range(2):
		if random.randint(0,10) == 0: exportString += "nan "
		exportString += str(random.randint(1,10000)) + " "
		exportString += streets[random.randint(0, len(streets) - 1)] + " "
		exportString += ends[random.randint(0,len(ends) - 1)] + " "
	df2 = pd.DataFrame({ 'label' : "Address", 'text' : exportString }, index=[1])
	return df2
		
#Creates randomized Cities column values numRepeats times and adds them to trainingData
def createCity():
	cityHeaders = ["City", "Town"];
	exportString = ""
	if(random.randint(0, 10)) != 0: exportString = cityHeaders[random.randint(0,1)] + " "
	for j in range(2):
		if random.randint(0,10) == 0: exportString += "nan "
		exportString += cities[random.randint(0, len(cities) - 1)] + " "
	df2 = pd.DataFrame({ 'label' : "City", 'text' : exportString}, index=[1])
	return df2

def createAllInRate():
	allInRateHeaders = ["All-In", "All-In Rate", "Rate", "All In", "All In Rate", "All-in"]
	exportString = ""
	if(random.randint(0, 10)) != 0: exportString = allInRateHeaders[random.randint(0,len(allInRateHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0,10) == 0: exportString += "nan "
		if random.randint(0,1) == 0:
			exportString += str(float(random.randint(0,500)/10000)) + " "
		else:
			exportString += str(float(random.randint(0,500)/100)) + "%" + " "
	df2 = pd.DataFrame({ 'label' : "All-In Rate", 'text' : exportString}, index=[1])
	return df2

def createLender():
	lenderHeaders = ["Lender", "Mortgage Holder", "Mortgage Lender"]
	lenderValues = open('Training Data/lender.txt').readlines()
	exportString = ""
	if(random.randint(0, 10)) != 0: exportString = lenderHeaders[random.randint(0,len(lenderHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0,10) == 0: exportString += "nan "
		exportString += lenderValues[random.randint(0, len(lenderValues) - 1)] + " "
	df2 = pd.DataFrame({ 'label' : "Lender", 'text' : exportString}, index=[1])
	return df2

def createSpread():
	spreadHeaders = ["Spread", "Credit Spread"]
	exportString = ""
	if(random.randint(0, 10)) != 0: exportString = spreadHeaders[random.randint(0,len(spreadHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0,10) == 0: exportString += "nan "
		exportString += str(random.randint(0, 25) * 10) + " BPs" + " "
	df2 = pd.DataFrame({ 'label' : "Spread", 'text' : exportString}, index=[1])
	return df2

def createIndex():
	indexHeaders = ["Index", "Interest Rate Index", "Rate Index"]
	indexValues = ["Libor", "LIBOR", "Libor", "LIBOR", "Libor", "LIBOR", "ICE LIBOR", "BBA LIBOR", "Bond Buyers", "FNMA", "Call Money"]
	exportString = ""
	if(random.randint(0, 10)) != 0: exportString = indexHeaders[random.randint(0,len(indexHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0,10) == 0: exportString += "nan "
		exportString += indexValues[random.randint(0,len(indexValues) - 1)] + " "
	df2 = pd.DataFrame({ 'label' : "Index", 'text' : exportString}, index=[1])
	return df2

#Creates randomized States column values numRepeats times and adds them to trainingData
def createState():
	states = ["AL", "AK", "AZ", "AR", "CA", "CZ", "CO", "CT", "DE", "DC", "FL", "GA", "GU", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VI", "WA", "WV", "WI", "WY", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Guam", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virgin Islands", "Virginia", "Washington", "Wisconsin", "Wyoming"];
	exportString = ""
	if(random.randint(0, 10)) != 0: exportString = "State "
	for j in range(2):
		if random.randint(0,10) == 0: exportString += "nan "
		exportString += states[random.randint(0,len(states) - 1)] + " "
	df2 = pd.DataFrame({ 'label' : "State", 'text' : exportString }, index=[1])
	return df2

#Creates randomized Units column values numRepeats times and adds them to trainingData
def createUnits():
	unitsHeaders = ["Units", "#units", "# of Units", "Number of Units", "Unit Count"];
	exportString = ""
	if(random.randint(0, 10)) != 0: exportString = unitsHeaders[random.randint(0,len(unitsHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0,10) == 0: exportString += "nan "
		exportString += str(random.randint(1, 1000)) + " "
	df2 = pd.DataFrame({ 'label' : "Units", 'text' : exportString }, index=[1])
	return df2

def createRateTypes():
	rateTypeHeaders = ["Loan Type", "Type of Loan", "Fixed or Floating", "Type", "Rate Type", "Type of Rate", "Interest Rate Type", "Type of Interest Rate"]
	rateTypes = ["Fixed", "Floating", "Other", "Variable"]
	exportString = ""
	if(random.randint(0, 10)) != 0: exportString = rateTypeHeaders[random.randint(0,len(rateTypeHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0,10) == 0: exportString += "nan "
		exportString += rateTypes[random.randint(0, len(rateTypes) - 1)] + " "
	df2 = pd.DataFrame({ 'label' : "Rate Type", 'text' : exportString }, index=[1])
	return df2

def createAcquisitionDate():
	ADHeaders = ["Acquisition Date", "Purchase Date", "Date of Acquisition", "Acquistion", "Acquired", "Year Acquired", "Date Acquired", "Origination Date", "Origination", "Year Originated", "Acquisition Date (yr)"];
	exportString = ""
	if(random.randint(0, 10)) != 0: exportString = ADHeaders[random.randint(0,4)] + " "
	yearOrDate = random.randint(0, 3)
	for j in range(2):
		if random.randint(0,10) == 0: exportString += "nan "
		if yearOrDate == 1: exportString += str(random.randint(1950, 2030)) + " "
		elif yearOrDate == 2: exportString += str(random.randint(1, 13)) + "/" + str(random.randint(1, 32)) + "/" + str(random.randint(1950, 2050)) + " "
		else: exportString += str(random.randint(1, 13)) + "-" + str(random.randint(1, 32)) + "-" + str(random.randint(1950, 2050)) + " 00:00:00 "
	df2 = pd.DataFrame({ 'label' : "Acquisition Date", 'text' : exportString }, index=[1])
	return df2

def createMaturityDate():
	MDHeaders = ["Maturity Date", "Maturity", "Loan Matures", "Matures", "Date of Maturity", "Date Matures", "Maturation Date"]
	exportString = ""
	if random.randint(0, 10) != 0: exportString = MDHeaders[random.randint(0,4)] + " "
	for j in range(2):
		if random.randint(0, 10) == 0: exportString += "nan "
		if(random.randint(0,2) == 1): exportString += str(random.randint(1, 13)) + "/" + str(random.randint(1, 32)) + "/" + str(random.randint(1950, 2050)) + " "
		else: exportString += str(random.randint(1, 13)) + "-" + str(random.randint(1, 32)) + "-" + str(random.randint(1950, 2050)) + " 00:00:00 "
	df2 = pd.DataFrame({ 'label' : "Maturity Date", 'text' : exportString }, index=[1])
	return df2

def createPropertyName():
	propertyNameHeaders = ["Property Name", "Name", "Property", "Property Number", "ID", "Property ID"]
	exportString = ""
	if random.randint(0, 10) != 0: exportString = propertyNameHeaders[random.randint(0, len(propertyNameHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0, 10) == 0: exportString += "nan "
		else:
			if random.randint(0, 2) == 0: exportString += str(random.randint(1, 10000))
			elif random.randint(0, 2) == 0: exportString += streets[random.randint(0, len(streets) - 1)] + " at "
			exportString += streets[random.randint(0, len(streets) - 1)] + " "
	df2 = pd.DataFrame({ 'label' : "Property Name", 'text' : exportString }, index=[1])
	return df2

def createSqFootage():
	sqFootageHeaders = ["Square Footage", "Square Feet", "Sq. Feet", "Sq. Ft.", "Feet", "Sq. Footage"]
	ends = ["", "ft", "ft.", "feet", " feet", " ft", " ft."]
	exportString = ""
	if random.randint(0, 10) != 0: exportString = sqFootageHeaders[random.randint(0, len(sqFootageHeaders) - 1)] + " "
	for j in range(2):
		if(random.randint(0, 10) == 0): exportString += "nan "
		else: 
			exportString += str(random.randint(1, 100000)) + ends[random.randint(0, len(ends) - 1)] + " "
	df2 = pd.DataFrame({ 'label' : "Square Feet", 'text' : exportString }, index=[1])
	return df2

def createOccupancy():
	occupancyHeaders = ["Occupancy", "Current Occupancy", "Occupancy Status", "Current Occupancy (%)", "% Occupied", "% Occupancy", "Occupancy %", "Occupancy at end of quarter"]
	exportString = ""
	if random.randint(0, 10) != 0: exportString = occupancyHeaders[random.randint(0, len(occupancyHeaders) - 1)] + " "
	for j in range(2):
		if(random.randint(0, 10) == 0): exportString += "nan "
		else: 
			exportString += str(random.randint(1, 100))
			if random.randint(0,2) == 0: exportString += "." + str(random.randint(1,100))
			if(random.randint(0,2) == 0): exportString += "%"
			exportString += " "
	df2 = pd.DataFrame({ 'label' : "Occupancy", 'text' : exportString }, index=[1])
	return df2

def createLoanAmount():
	loanAmountHeaders = ["Loan Amount", "Orig. Loan Amount", "Original Loan Amount", "OG Loan Amount"]
	exportString = ""
	if random.randint(0, 10) != 0: exportString += loanAmountHeaders[random.randint(0,len(loanAmountHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0, 10) == 0: exportString += "nan "
		else:
			if random.randint(0, 2) == 0: exportString += "$"
			if random.randint(0, 2) == 0: exportString += str(random.randint(0, 10000000))
			else: exportString += "{:,}".format(random.randint(0, 100000000))
			if random.randint(0, 2) == 0: exportString += "." + str(random.randint(0, 10000))
			exportString += " "
	df2 = pd.DataFrame({ 'label' : "Loan Amount", 'text' : exportString }, index=[1])
	return df2

def createDebtService():
	debtServiceHeaders = ["Debt Service", "Debt Service Value", "Total Debt Service", "Annual Debt Service"]
	exportString = ""
	if random.randint(0, 10) != 0: exportString += debtServiceHeaders[random.randint(0,len(debtServiceHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0, 10) == 0: exportString += "nan "
		else:
			if random.randint(0, 2) == 0: exportString += "$"
			if random.randint(0, 2) == 0: exportString += str(random.randint(0, 10000000))
			else: exportString += "{:,}".format(random.randint(0, 100000000))
			if random.randint(0, 2) == 0: exportString += "." + str(random.randint(0, 10000))
			exportString += " "
	df2 = pd.DataFrame({ 'label' : "Debt Service", 'text' : exportString }, index=[1])
	return df2

def createNOI():
	NOIHeaders = ["NOI", "Net Operating Income", "Net Income", "Current NOI", "N.O.I.", "Current N.O.I.", "Current Net Operating Income"]
	exportString = ""
	if random.randint(0, 10) != 0: exportString += NOIHeaders[random.randint(0,len(NOIHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0, 10) == 0: exportString += "nan "
		else:
			if random.randint(0, 2) == 0: exportString += "$"
			if random.randint(0, 2) == 0: exportString += str(random.randint(0, 10000000))
			else: exportString += "{:,}".format(random.randint(0, 100000000))
			if random.randint(0, 2) == 0: exportString += "." + str(random.randint(0, 10000))
			exportString += " "
	df2 = pd.DataFrame({ 'label' : "NOI", 'text' : exportString }, index=[1])
	return df2

def createDSCR():
	DSCRHeaders = ["DSCR", "Debt Service Coverage", "Total DCR", "DCR", "Total DSCR", "Debt Coverage Ratio", "Debt Service Ratio", "Debt Coverage"]
	exportString = ""
	if random.randint(0, 10) != 0: exportString += DSCRHeaders[random.randint(0,len(DSCRHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0, 10) == 0: exportString += "nan "
		else:
			exportString += str(random.randint(0,10)) + "." + str(random.randint(1,10000))
	df2 = pd.DataFrame({ 'label' : "DSCR", 'text' : exportString }, index=[1])
	return df2

def createMV():
	MVHeaders = ["Market Value", "MV", "Value"]
	exportString = ""
	if random.randint(0,10) != 0: exportString += MVHeaders[random.randint(0,len(MVHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0, 10) == 0: exportString += "nan "
		else:
			if random.randint(0, 2) == 0: exportString += "$"
			if random.randint(0, 2) == 0: exportString += str(random.randint(0, 10000000))
			else: exportString += "{:,}".format(random.randint(0, 100000000))
			if random.randint(0, 2) == 0: exportString += "." + str(random.randint(0, 10000))
			exportString += " "
	df2 = pd.DataFrame({ 'label' : "Market Value", 'text' : exportString }, index=[1])
	return df2

def createLTV():
	LTVHeaders = ["LTV", "Loan-To-Value", "Loan To Value"]
	exportString = ""
	if random.randint(0,10) != 0: exportString += LTVHeaders[random.randint(0,len(LTVHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0, 10) == 0: exportString += "nan "
		else:
			exportString += str(random.randint(0, 10)) + "."
			if random.randint(0, 2) == 0: exportString += str(random.randint(0, 1000000))
			else: exportString += str(random.randint(0, 100))
			if random.randint(0, 2) == 0: exportString += "% "
			else: exportString += " "
	df2 = pd.DataFrame({ 'label' : "LTV", 'text' : exportString }, index=[1])
	return df2

def createAmortStartDate():
	ADHeaders = ["Amort Start Date", "Amortization Start Date", "Amort Date", "Amortization Date", "Amort Start", "Amortization Start"]
	exportString = ""
	if random.randint(0, 10) != 0: exportString = ADHeaders[random.randint(0,len(ADHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0, 10) == 0: exportString += "nan "
		else:
			if(random.randint(0,2) == 1): exportString += str(random.randint(1, 13)) + "/" + str(random.randint(1, 32)) + "/" + str(random.randint(1950, 2050)) + " "
			else: exportString += str(random.randint(1, 13)) + "-" + str(random.randint(1, 32)) + "-" + str(random.randint(1950, 2050)) + " 00:00:00 "
	df2 = pd.DataFrame({ 'label' : "Amort Start Date", 'text' : exportString }, index=[1])
	return df2

def createPropertyType():
	propertyTypeHeaders = ["Property Type", "Type of Property", "Type", "Asset Type"]
	exportString = ""
	if random.randint(0, 10) != 0: exportString = propertyTypeHeaders[random.randint(0,len(propertyTypeHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0, 10) == 0: exportString += "nan "
		else:
			exportString += propertyTypes[random.randint(0,len(propertyTypes) - 1)] + " "
	df2 = pd.DataFrame({ 'label' : "Property Type", 'text' : exportString }, index=[1])
	return df2
			
def createCurrentBalance():
	balanceHeaders = ["Loan Amount", "Outstanding Loan Amount", "Principal Balance", "OPB", "Outstanding Principal Balance", "Current Balance", "Balance", "Current Debt"]
	exportString = ""
	if random.randint(0, 10) != 0: exportString = balanceHeaders[random.randint(0, len(balanceHeaders) - 1)] + " "
	for j in range(2):
		if random.randint(0, 10) == 0: exportString += "nan "
		else:
			if random.randint(0, 2) == 0: exportString += "$"
			if random.randint(0, 2) == 0: exportString += str(random.randint(0, 10000000))
			else: exportString += "{:,}".format(random.randint(0, 100000000))
			if random.randint(0, 2) == 0: exportString += "." + str(random.randint(0, 10000))
			exportString += " "
	df2 = pd.DataFrame({ 'label' : "Current Balance", 'text' : exportString }, index=[1])
	return df2

		#Creates randomized valid or invalid header rows and adds them to trainingData
def createValidHeaders():
	headers = ["Property Location", "Location", "Address", "Street Location", "Street Address", "Property Address", "Street", "Full Property Address", "Property Street Address City State Zip", "Property Name", "Name", "Property", "Property Number", "City", "Town", "State", "Territory", "Providence", "Units", "#units", "# of Units", "Number of Units", "Built", "Constructed", "Year Constructed", "Year Built", "Date Built", "Date Constructed", "Built (yr)", "Constructed (yr)", "Occupancy", "Current Occupancy (%)", "Current Occupancy", "Occupancy at end of quarter", "Acquisition Date", "Purchase Date", "Date of Acquisition", "Acquisition", "Year Acquired", "Origination Date", "Maturity Date", "Maturity", "Loan Matures", "Matures", "Loan Amount", "Outstanding Loan Amount", "Principle Balance", "OPB", "Outstanding Principal Balance", "O.P.B.", "Orig. Loan Amount", "Original Loan Amount", "Original Amount", "DSCR", "Debt Service Coverage", "Debt Service", "Total DCR", "DCR", "D.S.C.R.", "D.C.R", "Total D.C.R", "Total DSCR", "Total D.S.C.R.", "NOI", "Net Operating Income", "Net Income", "Current NOI", "N.O.I.", "Current N.O.I.", "Asset Type", "Type", "Country", "Nation", "Status", "Loan Type", "Fixed or Floating", "Type", "All-In Rate", "All In Rate", "I/O or Amort", "Interest Only or Amortizing Debt Service", "Value", "Market Value", "Cap Rate", "Rate", "LTV", "Loan-To-Value", "L.T.V.", "EGI", "Effective Gross Income", "E.G.I", "Lender"];
	numVals = random.randint(10, 25)
	exportString = ""
	for j in range(numVals):
			exportString += headers[random.randint(0, 91)] + " "
	df2 = pd.DataFrame({ 'label' : "Valid", 'text' : exportString }, index = [1])
	return df2

def createInvalidHeaders():
	headers = ["Property Location", "Location", "Address", "Street Location", "Street Address", "Property Address", "Street", "Full Property Address", "Property Street Address City State Zip", "Property Name", "Name", "Property", "Property Number", "City", "Town", "State", "Territory", "Providence", "Units", "#units", "# of Units", "Number of Units", "Built", "Constructed", "Year Constructed", "Year Built", "Date Built", "Date Constructed", "Built (yr)", "Constructed (yr)", "Occupancy", "Current Occupancy (%)", "Current Occupancy", "Occupancy at end of quarter", "Acquisition Date", "Purchase Date", "Date of Acquisition", "Acquisition", "Year Acquired", "Origination Date", "Maturity Date", "Maturity", "Loan Matures", "Matures", "Loan Amount", "Outstanding Loan Amount", "Principle Balance", "OPB", "Outstanding Principal Balance", "O.P.B.", "Orig. Loan Amount", "Original Loan Amount", "Original Amount", "DSCR", "Debt Service Coverage", "Debt Service", "Total DCR", "DCR", "D.S.C.R.", "D.C.R", "Total D.C.R", "Total DSCR", "Total D.S.C.R.", "NOI", "Net Operating Income", "Net Income", "Current NOI", "N.O.I.", "Current N.O.I.", "Asset Type", "Type", "Country", "Nation", "Status", "Loan Type", "Fixed or Floating", "Type", "All-In Rate", "All In Rate", "I/O or Amort", "Interest Only or Amortizing Debt Service", "Value", "Market Value", "Cap Rate", "Rate", "LTV", "Loan-To-Value", "L.T.V.", "EGI", "Effective Gross Income", "E.G.I", "Lender"];
	numVals = random.randint(10, 25)
	exportString = ""
	for j in range(numVals):
			rand = random.randint(0,10)
			if(rand == 0): exportString += str(random.randint(1,12)) + "/" + str(random.randint(1,31)) + "/" + str(random.randint(2000,2022)) + " "
			elif(rand == 1): exportString += headers[random.randint(0,91)] + " "
			else: exportString += "nan "
	df2 = pd.DataFrame({'label' : "Invalid", 'text' : exportString }, index = [1])
	return df2

def createHeaders():
	headers = ["Property Location", "Location", "Address", "Street Location", "Street Address", "Property Address", "Street", "Full Property Address", "Property Street Address City State Zip", "Property Name", "Name", "Property", "Property Number", "City", "Town", "State", "Territory", "Providence", "Units", "#units", "# of Units", "Number of Units", "Built", "Constructed", "Year Constructed", "Year Built", "Date Built", "Date Constructed", "Built (yr)", "Constructed (yr)", "Occupancy", "Current Occupancy (%)", "Current Occupancy", "Occupancy at end of quarter", "Acquisition Date", "Purchase Date", "Date of Acquisition", "Acquisition", "Year Acquired", "Origination Date", "Maturity Date", "Maturity", "Loan Matures", "Matures", "Loan Amount", "Outstanding Loan Amount", "Principle Balance", "OPB", "Outstanding Principal Balance", "O.P.B.", "Orig. Loan Amount", "Original Loan Amount", "Original Amount", "DSCR", "Debt Service Coverage", "Debt Service", "Total DCR", "DCR", "D.S.C.R.", "D.C.R", "Total D.C.R", "Total DSCR", "Total D.S.C.R.", "NOI", "Net Operating Income", "Net Income", "Current NOI", "N.O.I.", "Current N.O.I.", "Asset Type", "Type", "Country", "Nation", "Status", "Loan Type", "Fixed or Floating", "Type", "All-In Rate", "All In Rate", "I/O or Amort", "Interest Only or Amortizing Debt Service", "Value", "Market Value", "Cap Rate", "Rate", "LTV", "Loan-To-Value", "L.T.V.", "EGI", "Effective Gross Income", "E.G.I", "Lender"];
	rand = random.randint(0,1)
	numVals = random.randint(15, 25)
	exportString = ""
	if rand == 0:
		for j in range(numVals):
			exportString += headers[random.randint(0, 91)] + " "
		df2 = pd.DataFrame({ 'label' : "Valid", 'text' : exportString }, index = [1])
	else:
		for j in range(0,numVals):
			rand = random.randint(0,10)
			if(rand == 0): exportString += str(random.randint(1,12)) + "/" + str(random.randint(1,31)) + "/" + str(random.randint(2000,2022)) + " "
			elif(rand == 1): exportString += headers[random.randint(0,91)] + " "
			else: exportString += "nan "
		df2 = pd.DataFrame({'label' : "Invalid", 'text' : exportString }, index = [1])
	trainingData = pd.concat([trainingData, df2], ignore_index = True)
	print()
	return trainingData