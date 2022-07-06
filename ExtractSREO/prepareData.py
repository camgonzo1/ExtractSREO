from lib2to3.pytree import convert
from re import L
import os
import random
from numpy import dtype
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('Training Data/addresses.txt') as f: streets = f.readlines()	
streets = streets[0].split('/')
with open('Training Data/cities.txt') as f: cities = f.readlines()	
cities = cities[0].split('/')
with open('Training Data/asset types.txt') as f: propertyTypes = f.readlines()	
propertyTypes = propertyTypes[0].split('/')

#Takes inputted columnOrHeader value and calls corresponding functions, randomizes column function calls
def createData(columnOrHeader, fileName, numRepeats):
	trainingData = pd.DataFrame(columns=['label','text'])
	if(columnOrHeader == 1):
		for i in range(numRepeats):
			rand = random.randint(1,22)
			if(random.randint(0,10) == 0): trainingData = createAddresses(trainingData, 1)
			if(random.randint(0,10) == 0): trainingData = createPropertyName(trainingData, 1)
			if(rand == 1): trainingData = createCities(trainingData, 1)
			elif(rand == 2): trainingData = createStates(trainingData, 1)
			elif(rand == 3): trainingData = createUnits(trainingData, 1)
			elif(rand == 4): trainingData = createRateTypes(trainingData, 1)
			elif(rand == 5): trainingData = createAcquisitionDate(trainingData, 1)
			elif(rand == 6): trainingData = createMaturityDate(trainingData, 1)
			elif(rand == 7): trainingData = createSqFootage(trainingData, 1)
			elif(rand == 8): trainingData = createOccupancy(trainingData, 1)
			elif(rand == 9): trainingData = createLoanAmount(trainingData, 1)
			elif(rand == 10): trainingData = createDebtService(trainingData, 1)
			elif(rand == 11): trainingData = createNOI(trainingData, 1)
			elif(rand == 12): trainingData = createDSCR(trainingData, 1)
			elif(rand == 13): trainingData = createMV(trainingData, 1)
			elif(rand == 14): trainingData = createLTV(trainingData, 1)
			elif(rand == 15): trainingData = createAmortStartDate(trainingData, 1)
			elif(rand == 16): trainingData = createPropertyType(trainingData, 1)
			elif(rand == 17): trainingData = createCurrentBalance(trainingData, 1)
			elif(rand == 18): trainingData = createAllInRate(trainingData, 1)
			elif(rand == 19): trainingData = createLender(trainingData, 1)
			elif(rand == 20): trainingData = createSpread(trainingData, 1)
			elif(rand == 21): trainingData = createIndex(trainingData, 1)
			if((numRepeats - (i + 1)) % (numRepeats / 50) == 0): print("X", end="")
	elif(columnOrHeader == 2):
		trainingData = createHeaders(trainingData,numRepeats)
	print()
	trainingData.to_csv(fileName, index=False)

#Creates randomized Address column values numRepeats times and adds them to trainingData
def createAddresses(trainingData, numRepeats):
	ends = ["Road", "Rd.", "rd.", "Rd", "Boulevard", "blvd.", "Blvd", "Street", "St.", "St", "Way", "Circle", "Ave.", "Ave", "Avenue", "Drive", "Dr.", "Dr"];
	addressHeaders = ["Property Location", "Location", "Address", "Street Location", "Street Address", "Property Address", "Street", "Full Property Address", "Property Street Address City State Zip"];
	exportString = ""
	for i in range(numRepeats):
		#numVals = random.randint(1, 25)
		if(random.randint(0, 10)) != 0: exportString = addressHeaders[random.randint(0,8)] + " "
		for j in range(2):
			if random.randint(0,10) == 0: exportString += "nan "
			exportString += str(random.randint(1,10000)) + " "
			exportString += streets[random.randint(0, len(streets) - 1)] + " "
			exportString += ends[random.randint(0,len(ends) - 1)] + " "
		#print("Address " + exportString)
		df2 = pd.DataFrame({ 'label' : "Address", 'text' : exportString }, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index = True)
	return trainingData
		
#Creates randomized Cities column values numRepeats times and adds them to trainingData
def createCities(trainingData, numRepeats):
	cityHeaders = ["City", "Town"];
	exportString = ""
	for i in range(numRepeats):
		#numVals = random.randint(1, 25)
		if(random.randint(0, 10)) != 0: exportString = cityHeaders[random.randint(0,1)] + " "
		for j in range(2):
			if random.randint(0,10) == 0: exportString += "nan "
			exportString += cities[random.randint(0, len(cities) - 1)] + " "
		#print("City " + exportString)
		df2 = pd.DataFrame({ 'label' : "City", 'text' : exportString}, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index = True)
	return trainingData

def createAllInRate(trainingData, numRepeats):
	allInRateHeaders = ["All-In", "All-In Rate", "Rate", "All In", "All In Rate", "All-in"]
	exportString = ""
	for i in range(numRepeats):
		#numVals = random.randint(1, 25)
		if(random.randint(0, 10)) != 0: exportString = allInRateHeaders[random.randint(0,len(allInRateHeaders) - 1)] + " "
		for j in range(2):
			if random.randint(0,10) == 0: exportString += "nan "
			if random.randint(0,1) == 0:
				exportString += str(float(random.randint(0,500)/10000)) + " "
			else:
				exportString += str(float(random.randint(0,500)/100)) + "%" + " "
		#print("All-In Rate " + exportString)
		df2 = pd.DataFrame({ 'label' : "All-In Rate", 'text' : exportString}, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index = True)
	return trainingData

def createLender(trainingData, numRepeats):
	lenderHeaders = ["Lender", "Mortgage Holder", "Mortgage Lender"]
	lenderValues = open('Training Data/lender.txt').readlines()
	exportString = ""
	for i in range(numRepeats):
		#numVals = random.randint(1, 25)
		if(random.randint(0, 10)) != 0: exportString = lenderHeaders[random.randint(0,len(lenderHeaders) - 1)] + " "
		for j in range(2):
			if random.randint(0,10) == 0: exportString += "nan "
			exportString += lenderValues[random.randint(0, len(lenderValues) - 1)] + " "
		#print("Lender " + exportString)
		df2 = pd.DataFrame({ 'label' : "Lender", 'text' : exportString}, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index = True)
	return trainingData

def createSpread(trainingData, numRepeats):
	spreadHeaders = ["Spread", "Credit Spread"]
	exportString = ""
	for i in range(numRepeats):
		#numVals = random.randint(1, 25)
		if(random.randint(0, 10)) != 0: exportString = spreadHeaders[random.randint(0,len(spreadHeaders) - 1)] + " "
		for j in range(2):
			if random.randint(0,10) == 0: exportString += "nan "
			exportString += str(random.randint(0, 25) * 10) + " BPs" + " "
		#print("Spread " + exportString)
		df2 = pd.DataFrame({ 'label' : "Spread", 'text' : exportString}, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index = True)
	return trainingData

def createIndex(trainingData, numRepeats):
	indexHeaders = ["Index", "Interest Rate Index", "Rate Index"]
	indexValues = ["Libor", "LIBOR", "Libor", "LIBOR", "Libor", "LIBOR", "ICE LIBOR", "BBA LIBOR", "Bond Buyers", "FNMA", "Call Money"]
	exportString = ""
	for i in range(numRepeats):
		#numVals = random.randint(1, 25)
		if(random.randint(0, 10)) != 0: exportString = indexHeaders[random.randint(0,len(indexHeaders) - 1)] + " "
		for j in range(2):
			if random.randint(0,10) == 0: exportString += "nan "
			exportString += indexValues[random.randint(0,len(indexValues) - 1)] + " "
		#print("Index " + exportString)
		df2 = pd.DataFrame({ 'label' : "Index", 'text' : exportString}, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index = True)
	return trainingData

#Creates randomized States column values numRepeats times and adds them to trainingData
def createStates(trainingData, numRepeats):
	states = ["AL", "AK", "AZ", "AR", "CA", "CZ", "CO", "CT", "DE", "DC", "FL", "GA", "GU", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VI", "WA", "WV", "WI", "WY", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Guam", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virgin Islands", "Virginia", "Washington", "Wisconsin", "Wyoming"];
	exportString = ""
	for i in range(numRepeats):
		#numVals = random.randint(1, 25)
		if(random.randint(0, 10)) != 0: exportString = "State "
		for j in range(2):
			if random.randint(0,10) == 0: exportString += "nan "
			exportString += states[random.randint(0,len(states) - 1)] + " "
		#print("State " + exportString)
		df2 = pd.DataFrame({ 'label' : "State", 'text' : exportString }, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index = True)
	return trainingData

#Creates randomized Units column values numRepeats times and adds them to trainingData
def createUnits(trainingData, numRepeats):
	unitsHeaders = ["Units", "#units", "# of Units", "Number of Units", "Unit Count"];
	for i in range(numRepeats):
		exportString = ""
		#numVals = random.randint(1, 25)
		if(random.randint(0, 10)) != 0: exportString = unitsHeaders[random.randint(0,len(unitsHeaders) - 1)] + " "
		for j in range(2):
			if random.randint(0,10) == 0: exportString += "nan "
			exportString += str(random.randint(1, 1000)) + " "
		#print("Units " + exportString)
		df2 = pd.DataFrame({ 'label' : "Units", 'text' : exportString }, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index = True)
	return trainingData

def createRateTypes(trainingData, numRepeats):
	rateTypeHeaders = ["Loan Type", "Type of Loan", "Fixed or Floating", "Type", "Rate Type", "Type of Rate", "Interest Rate Type", "Type of Interest Rate"]
	rateTypes = ["Fixed", "Floating", "Other", "Variable"]
	for i in range(numRepeats):
		exportString = ""
		#numVals = random.randint(1, 25)
		if(random.randint(0, 10)) != 0: exportString = rateTypeHeaders[random.randint(0,len(rateTypeHeaders) - 1)] + " "
		for j in range(2):
			if random.randint(0,10) == 0: exportString += "nan "
			exportString += rateTypes[random.randint(0, len(rateTypes) - 1)] + " "
		df2 = pd.DataFrame({ 'label' : "Rate Type", 'text' : exportString }, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index = True)
	return trainingData

def createAcquisitionDate(trainingData, numRepeats):
	ADHeaders = ["Acquisition Date", "Purchase Date", "Date of Acquisition", "Acquistion", "Acquired", "Year Acquired", "Date Acquired", "Origination Date", "Origination", "Year Originated", "Acquisition Date (yr)"];
	for i in range(numRepeats):
		exportString = ""
		#numVals = random.randint(1, 25)
		if(random.randint(0, 10)) != 0: exportString = ADHeaders[random.randint(0,4)] + " "
		yearOrDate = random.randint(0, 3)
		for j in range(2):
			if random.randint(0,10) == 0: exportString += "nan "
			if yearOrDate == 1: exportString += str(random.randint(1950, 2030)) + " "
			elif yearOrDate == 2: exportString += str(random.randint(1, 13)) + "/" + str(random.randint(1, 32)) + "/" + str(random.randint(1950, 2050)) + " "
			else: exportString += str(random.randint(1, 13)) + "-" + str(random.randint(1, 32)) + "-" + str(random.randint(1950, 2050)) + " 00:00:00 "
		df2 = pd.DataFrame({ 'label' : "Acquisition Date", 'text' : exportString }, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index = True)
	return trainingData

def createMaturityDate(trainingData, numRepeats):
	MDHeaders = ["Maturity Date", "Maturity", "Loan Matures", "Matures", "Date of Maturity", "Date Matures", "Maturation Date"]
	for i in range(numRepeats):
		exportString = ""
		#numVals = random.randint(1, 25)
		if random.randint(0, 10) != 0: exportString = MDHeaders[random.randint(0,4)] + " "
		for j in range(2):
			if random.randint(0, 10) == 0: exportString += "nan "
			if(random.randint(0,2) == 1): exportString += str(random.randint(1, 13)) + "/" + str(random.randint(1, 32)) + "/" + str(random.randint(1950, 2050)) + " "
			else: exportString += str(random.randint(1, 13)) + "-" + str(random.randint(1, 32)) + "-" + str(random.randint(1950, 2050)) + " 00:00:00 "
		df2 = pd.DataFrame({ 'label' : "Maturity Date", 'text' : exportString }, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index=True)
	return trainingData

def createPropertyName(trainingData, numRepeats):
	propertyNameHeaders = ["Property Name", "Name", "Property", "Property Number", "ID", "Property ID"]
	for i in range(numRepeats):
		exportString = ""
		if random.randint(0, 10) != 0: exportString = propertyNameHeaders[random.randint(0, len(propertyNameHeaders) - 1)] + " "
		for j in range(2):
			if random.randint(0, 10) == 0: exportString += "nan "
			else:
				if random.randint(0, 2) == 0: exportString += str(random.randint(1, 10000))
				elif random.randint(0, 2) == 0: exportString += streets[random.randint(0, len(streets) - 1)] + " at "
				exportString += streets[random.randint(0, len(streets) - 1)] + " "
		df2 = pd.DataFrame({ 'label' : "Property Name", 'text' : exportString }, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index=True)
	return trainingData

def createSqFootage(trainingData, numRepeats):
	sqFootageHeaders = ["Square Footage", "Square Feet", "Sq. Feet", "Sq. Ft.", "Feet", "Sq. Footage"]
	ends = ["", "ft", "ft.", "feet", " feet", " ft", " ft."]
	for i in range(numRepeats):
		exportString = ""
		if random.randint(0, 10) != 0: exportString = sqFootageHeaders[random.randint(0, len(sqFootageHeaders) - 1)] + " "
		for j in range(2):
			if(random.randint(0, 10) == 0): exportString += "nan "
			else: 
				exportString += str(random.randint(1, 100000)) + ends[random.randint(0, len(ends) - 1)] + " "
		df2 = pd.DataFrame({ 'label' : "Square Feet", 'text' : exportString }, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index=True)
	return trainingData

def createOccupancy(trainingData, numRepeats):
	occupancyHeaders = ["Occupancy", "Current Occupancy", "Occupancy Status", "Current Occupancy (%)", "% Occupied", "% Occupancy", "Occupancy %", "Occupancy at end of quarter"]
	for i in range(numRepeats):
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
		trainingData = pd.concat([trainingData, df2],ignore_index=True)
	return trainingData

def createLoanAmount(trainingData, numRepeats):
	loanAmountHeaders = ["Loan Amount", "Orig. Loan Amount", "Original Loan Amount", "OG Loan Amount"]
	for i in range(numRepeats):
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
		trainingData = pd.concat([trainingData, df2],ignore_index=True)
	return trainingData

def createDebtService(trainingData, numRepeats):
	debtServiceHeaders = ["Debt Service", "Debt Service Value", "Total Debt Service", "Annual Debt Service"]
	for i in range(numRepeats):
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
		trainingData = pd.concat([trainingData, df2],ignore_index=True)
	return trainingData

def createNOI(trainingData, numRepeats):
	NOIHeaders = ["NOI", "Net Operating Income", "Net Income", "Current NOI", "N.O.I.", "Current N.O.I.", "Current Net Operating Income"]
	for i in range(numRepeats):
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
		trainingData = pd.concat([trainingData, df2],ignore_index=True)
	return trainingData

def createDSCR(trainingData, numRepeats):
	DSCRHeaders = ["DSCR", "Debt Service Coverage", "Total DCR", "DCR", "Total DSCR", "Debt Coverage Ratio", "Debt Service Ratio", "Debt Coverage"]
	for i in range(numRepeats):
		exportString = ""
		if random.randint(0, 10) != 0: exportString += DSCRHeaders[random.randint(0,len(DSCRHeaders) - 1)] + " "
		for j in range(2):
			if random.randint(0, 10) == 0: exportString += "nan "
			else:
				exportString += str(random.randint(0,10)) + "." + str(random.randint(1,10000))
		df2 = pd.DataFrame({ 'label' : "DSCR", 'text' : exportString }, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index=True)
	return trainingData

def createMV(trainingData, numRepeats):
	MVHeaders = ["Market Value", "MV", "Value"]
	for i in range(numRepeats):
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
		trainingData = pd.concat([trainingData, df2],ignore_index=True)
	return trainingData

def createLTV(trainingData, numRepeats):
	LTVHeaders = ["LTV", "Loan-To-Value", "Loan To Value"]
	for i in range(numRepeats):
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
		trainingData = pd.concat([trainingData, df2], ignore_index=True)
	return trainingData

def createAmortStartDate(trainingData, numRepeats):
	ADHeaders = ["Amort Start Date", "Amortization Start Date", "Amort Date", "Amortization Date", "Amort Start", "Amortization Start"]
	for i in range(numRepeats):
		exportString = ""
		#numVals = random.randint(1, 25)
		if random.randint(0, 10) != 0: exportString = ADHeaders[random.randint(0,len(ADHeaders) - 1)] + " "
		for j in range(2):
			if random.randint(0, 10) == 0: exportString += "nan "
			else:
				if(random.randint(0,2) == 1): exportString += str(random.randint(1, 13)) + "/" + str(random.randint(1, 32)) + "/" + str(random.randint(1950, 2050)) + " "
				else: exportString += str(random.randint(1, 13)) + "-" + str(random.randint(1, 32)) + "-" + str(random.randint(1950, 2050)) + " 00:00:00 "
		df2 = pd.DataFrame({ 'label' : "Amort Start Date", 'text' : exportString }, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index=True)
	return trainingData

def createPropertyType(trainingData, numRepeats):
	propertyTypeHeaders = ["Property Type", "Type of Property", "Type", "Asset Type"]
	for i in range(numRepeats):
		exportString = ""
		if random.randint(0, 10) != 0: exportString = propertyTypeHeaders[random.randint(0,len(propertyTypeHeaders) - 1)] + " "
		for j in range(2):
			if random.randint(0, 10) == 0: exportString += "nan "
			else:
				exportString += propertyTypes[random.randint(0,len(propertyTypes) - 1)] + " "
		df2 = pd.DataFrame({ 'label' : "Property Type", 'text' : exportString }, index=[1])
		trainingData = pd.concat([trainingData, df2],ignore_index=True)
	return trainingData
			
def createCurrentBalance(trainingData, numRepeats):
	balanceHeaders = ["Loan Amount", "Outstanding Loan Amount", "Principal Balance", "OPB", "Outstanding Principal Balance", "Current Balance", "Balance", "Current Debt"]
	for i in range(numRepeats):
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
		trainingData = pd.concat([trainingData, df2],ignore_index=True)
	return trainingData
			


		#Creates randomized valid or invalid header rows and adds them to trainingData
def createHeaders(trainingData, numRepeats):
	headers = ["Property Location", "Location", "Address", "Street Location", "Street Address", "Property Address", "Street", "Full Property Address", "Property Street Address City State Zip", "Property Name", "Name", "Property", "Property Number", "City", "Town", "State", "Territory", "Providence", "Units", "#units", "# of Units", "Number of Units", "Built", "Constructed", "Year Constructed", "Year Built", "Date Built", "Date Constructed", "Built (yr)", "Constructed (yr)", "Occupancy", "Current Occupancy (%)", "Current Occupancy", "Occupancy at end of quarter", "Acquisition Date", "Purchase Date", "Date of Acquisition", "Acquisition", "Year Acquired", "Origination Date", "Maturity Date", "Maturity", "Loan Matures", "Matures", "Loan Amount", "Outstanding Loan Amount", "Principle Balance", "OPB", "Outstanding Principal Balance", "O.P.B.", "Orig. Loan Amount", "Original Loan Amount", "Original Amount", "DSCR", "Debt Service Coverage", "Debt Service", "Total DCR", "DCR", "D.S.C.R.", "D.C.R", "Total D.C.R", "Total DSCR", "Total D.S.C.R.", "NOI", "Net Operating Income", "Net Income", "Current NOI", "N.O.I.", "Current N.O.I.", "Asset Type", "Type", "Country", "Nation", "Status", "Loan Type", "Fixed or Floating", "Type", "All-In Rate", "All In Rate", "I/O or Amort", "Interest Only or Amortizing Debt Service", "Value", "Market Value", "Cap Rate", "Rate", "LTV", "Loan-To-Value", "L.T.V.", "EGI", "Effective Gross Income", "E.G.I", "Lender"];
	for i in range(numRepeats):
		if((numRepeats - (i + 1)) % (numRepeats / 50) == 0): print("X", end="")
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
