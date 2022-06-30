from lib2to3.pytree import convert
from re import L
import random
from numpy import dtype
import pandas as pd

#Takes inputted columnOrHeader value and calls corresponding functions, randomizes column function calls
def createData(columnOrHeader, fileName, numRepeats):
	trainingData = pd.DataFrame(columns=['label','text'])
	if(columnOrHeader == '1'):
		for i in range(numRepeats):
			rand = random.randint(0,3)
			if(rand == 0): trainingData = createAddresses(trainingData, 1)
			elif(rand == 1): trainingData = createCities(trainingData, 1)
			elif(rand == 2): trainingData = createStates(trainingData, 1)
			else: trainingData = createUnits(trainingData, 1)
	elif(columnOrHeader == '2'):
		trainingData = createHeaders(trainingData,numRepeats)
	trainingData.to_csv(fileName, index=False)

#Creates randomized Address column values numRepeats times and adds them to trainingData
def createAddresses(trainingData, numRepeats):
	with open('Training Data/addresses.txt') as f:
		streets = f.readlines()	
	f.close()
	streets = streets[0].split('/')
	ends = ["Road", "Rd.", "rd.", "Boulevard", "blvd.", "Street", "St.", "Way", "Circle", "Ave.", "Avenue", "Drive", "Dr."];
	addressHeaders = ["Property Location", "Location", "Address", "Street Location", "Street Address", "Property Address", "Street", "Full Property Address", "Property Street Address City State Zip"];
	exportString = ""
	for i in range(numRepeats):
		numVals = random.randint(1, 25)
		addEnd = random.randint(0, 5)
		if random.randint(0, 2) == 1: exportString = addressHeaders[random.randint(0,8)] + " "
		for j in range(numVals):
			exportString += str(random.randint(1,10000)) + " "
			exportString += streets[random.randint(0, len(streets) - 1)] + " "
			if(addEnd != 4): exportString += ends[random.randint(0,12)] + " "
		print("Address " + exportString)
		df2 = pd.DataFrame({ 'label' : "Address", 'text' : exportString }, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index = True)
	return trainingData
		
#Creates randomized Cities column values numRepeats times and adds them to trainingData
def createCities(trainingData, numRepeats):
	with open('Training Data/addresses.txt') as f:
		cities = f.readlines()	
	f.close()
	cities = cities[0].split('/')	
	cityHeaders = ["City", "Town"];
	exportString = ""
	for i in range(numRepeats):
		numVals = random.randint(1, 25)
		if random.randint(0, 2) == 1: exportString = cityHeaders[random.randint(0,1)] + " "
		for j in range(numVals):
			exportString += cities[random.randint(0, len(cities) - 1)] + " "
		print("City " + exportString)
		df2 = pd.DataFrame({ 'label' : "City", 'text' : exportString}, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index = True)
	return trainingData

#Creates randomized States column values numRepeats times and adds them to trainingData
def createStates(trainingData, numRepeats):
	states = ["AL", "AK", "AZ", "AR", "CA", "CZ", "CO", "CT", "DE", "DC", "FL", "GA", "GU", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VI", "WA", "WV", "WI", "WY", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Guam", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virgin Islands", "Virginia", "Washington", "Wisconsin", "Wyoming"];
	exportString = ""
	for i in range(numRepeats):
		numVals = random.randint(1, 25)
		if random.randint(0, 2) == 1: exportString = "State "
		for j in range(numVals):
			exportString += states[random.randint(0,106)] + " "
		print("State " + exportString)
		df2 = pd.DataFrame({ 'label' : "State", 'text' : exportString }, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index = True)
	return trainingData

#Creates randomized Units column values numRepeats times and adds them to trainingData
def createUnits(trainingData, numRepeats):
	unitsHeaders = ["Units", "#units", "# of Units", "Number of Units", "Unit Count"];
	exportString = ""
	for i in range(numRepeats):
		numVals = random.randint(1, 25)
		if random.randint(0, 2) == 1: exportString = unitsHeaders[random.randint(0,4)] + " "
		for j in range(numVals):
			exportString += str(random.randint(1, 1000)) + " "
		print("Units " + exportString)
		df2 = pd.DataFrame({ 'label' : "Units", 'text' : exportString }, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index = True)
	return trainingData

#Creates randomized valid or invalid header rows and adds them to trainingData
def createHeaders(trainingData, numRepeats):
	headers = ["Property Location", "Location", "Address", "Street Location", "Street Address", "Property Address", "Street", "Full Property Address", "Property Street Address City State Zip", "Property Name", "Name", "Property", "Property Number", "City", "Town", "State", "Territory", "Providence", "Units", "#units", "# of Units", "Number of Units", "Built", "Constructed", "Year Constructed", "Year Built", "Date Built", "Date Constructed", "Built (yr)", "Constructed (yr)", "Occupancy", "Current Occupancy (%)", "Current Occupancy", "Occupancy at end of quarter", "Acquisition Date", "Purchase Date", "Date of Acquisition", "Acquisition", "Year Acquired", "Origination Date", "Maturity Date", "Maturity", "Loan Matures", "Matures", "Loan Amount", "Outstanding Loan Amount", "Principle Balance", "OPB", "Outstanding Principal Balance", "O.P.B.", "Orig. Loan Amount", "Original Loan Amount", "Original Amount", "DSCR", "Debt Service Coverage", "Debt Service", "Total DCR", "DCR", "D.S.C.R.", "D.C.R", "Total D.C.R", "Total DSCR", "Total D.S.C.R.", "NOI", "Net Operating Income", "Net Income", "Current NOI", "N.O.I.", "Current N.O.I.", "Asset Type", "Type", "Country", "Nation", "Status", "Loan Type", "Fixed or Floating", "Type", "All-In Rate", "All In Rate", "I/O or Amort", "Interest Only or Amortizing Debt Service", "Value", "Market Value", "Cap Rate", "Rate", "LTV", "Loan-To-Value", "L.T.V.", "EGI", "Effective Gross Income", "E.G.I", "Lender"];
	for i in range(numRepeats):
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
		print(exportString)
	return trainingData
