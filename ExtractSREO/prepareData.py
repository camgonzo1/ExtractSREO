#from lib2to3.pytree import convert
#from re import L
import os
import random
#from numpy import dtype
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

LABEL, TEXT = 0, 1
COLUMN_INFO = {  0: ("Loan Amount", ["Loan Amount", "Orig. Loan Amount", "Original Loan Amount", "OG Loan Amount", "Total Loan Amount", "Origional Balance", "Orig. Loan Amt.", "Total Loan", "Total Loan(s)", "Total Commitment"]), 
				 1: ("Debt Service", ["Debt Service", "Debt Service Value", "Total Debt Service", "Annual Debt Service", "Debt Service Total", "Debt Service Calculation", "2022 Total Debt Service (Projected)", "Combined Annual Debt Service"]),
				 2: ("NOI", ["NOI", "Net Operating Income", "Net Income", "Current NOI", "N.O.I.", "Current N.O.I.", "Current Net Operating Income", "Net Rental Income", "NOI", "NOI  (Period Ending YTD)", "NOI (12/31/2021)", "2022 Net Operating Income (Projected)", "12/31/2020 NOI", "12/31/2020 NOI (Per Collier's Valuation), NOI  (Period Ending YTD 2022)"]),
				 3: ("Market Value", ["Market Value", "MV", "Value", "Internal Valuation", "PWC Value", "Market Total Value", "Borrower Started Value", "Full Market Value", "Value/Unit", "Valuation Dec-2020"]), 
				 4: ("Current Balance", ["Current Loan Balance","Current Debt", "Outstanding Loan Amount", "Principal Balance", "OPB", "Outstanding Principal Balance", "Current Balance", "Balance", "Current Debt", "Loan Balance", "Current Amount", "Outstanding", "Outstanding Loan(s)", "Outstanding Loans", "Outstanding Debt (YE)", "Outstanding Debt", "Balance of Mortgages", "Mortgage Outstanding", "Mortgage Liens as of ", "OPB (1/31/2022)", "Balance as of *", "Principal Balance as of 12/31/21", "Outstanding Principal"]),
				 5: ("Occupancy", ["Occupancy", "Current Occupancy", "Occupancy Status", "Current Occupancy (%)", "% Occupied", "% Occupancy", "Occupancy %", "Occupancy at end of quarter", "Occ. %", "Occupancy at end of quarter", "Physical Occupancy"]),
				 6: ("LTV", ["LTV", "LTV", "Loan-To-Value", "Loan To Value"]),
				 7: ("All-In Rate", ["All-In", "All-In Rate", "Rate", "All In", "All In Rate", "All-in", "Interest", "Interest Rate", "Current Rate", "Interest Rate (at 12/31/21)"]),
				 8: ("Acquisition Date", ["Acquisition Date", "Acquisition Date", "Purchase Date", "Date of Acquisition", "Acquistion", "Acquired", "Year Acquired", "Date Acquired", "Origination Date", "Origination", "Year Originated", "Acquisition Date (yr)", "Year of Initial Ownership", "Owned Since", "Acq. Date Cost", "Acquisiton Year"]),
				 9: ("Maturity Date", ["Maturity Date", "Maturity", "Loan Matures", "Matures", "Date of Maturity", "Date Matures", "Maturation Date", "Loan Maturity Date", "Final Maturity", "Maturity Date(s)", "Due Date (year)", "Due Date"]),
				 10: ("Amort Start Date", ["Amort Start Date", "Amortization Start Date", "Amort Date", "Amortization Date", "Amort Start", "Amortization Start", "Commence Date", "Amort."]),
				 11: ("DSCR", ["DSCR", "Debt Service Coverage", "Total DCR", "DCR", "Total DSCR", "Debt Coverage Ratio", "Debt Service Ratio", "Debt Coverage", "DSC"]),
				 12: ("Units", ["Units", "#units", "# of Units", "Number of Units", "Unit Count", "Multifamily Units (#)", "Multifamily Units", "Units / Sq. Ft.", "# Units / SF", "Units/ Sq. Ft."]),
				 13: ("Square Feet", ["Square Footage", "Square Feet", "Sq. Feet", "Sq. Ft.", "Feet", "Sq. Footage", "SF / # of Units", "SF/Units"]),
				 14: ("Spread", ["Spread", "Credit Spread"]),
				 15: ("Address", ["Property Location", "Location", "Address", "Street Location", "Street Address", "Property Address", "Street", "Full Property Address", "Property Street Address"]),
				 16: ("City", ["City", "Town", "Property City", "Location"]),
				 17: ("Property Type", ["Property Type", "Type of Property", "Type", "Asset Type", "Property Description", "Prop. Type", "Description", "Type of Community"]),
				 18: ("State", ["State", "Providence", "Territory", "Location", "Property State", "ST"]),
				 19: ("Index", ["Index", "Interest Rate Index", "Rate Index"]),
				 20: ("Lender", ["Lender", "Mortgage Holder", "Mortgage Lender", "Lender Name", "Lender Name (Confirm if Fannie or Freddie, where applicable)", "Lender (Servicer)", "Lender(s)"]),
				 21: ("Property Name", ["Property Name","Property Name", "Name", "Property", "Property Number", "Debt ID", "Property ID", "Building", "Building Number", "Building Name/Number", "Building Name", "Legal Name"]),
				 22: ("Rate Type", ["Type", "Loan Type", "Type of Loan", "Fixed or Floating", "Type", "Rate Type", "Type of Rate", "Interest Rate Type", "Type of Interest Rate", "Fixed / Variable", "Fixed/Variable", "Floating (Y/N)", "Structure"])}

HEADERS = ["Property Location", "Location", "Address", "Street Location", "Street Address", "Property Address", "Street", "Full Property Address", "Property Street Address City State Zip", "Property Name", "Name", "Property", "Property Number", "City", "Town", "State", "Territory", "Providence", "Units", "#units", "# of Units", "Number of Units", "Built", "Constructed", "Year Constructed", "Year Built", "Date Built", "Date Constructed", "Built (yr)", "Constructed (yr)", "Occupancy", "Current Occupancy (%)", "Current Occupancy", "Occupancy at end of quarter", "Acquisition Date", "Purchase Date", "Date of Acquisition", "Acquisition", "Year Acquired", "Origination Date", "Maturity Date", "Maturity", "Loan Matures", "Matures", "Loan Amount", "Outstanding Loan Amount", "Principle Balance", "OPB", "Outstanding Principal Balance", "O.P.B.", "Orig. Loan Amount", "Original Loan Amount", "Original Amount", "DSCR", "Debt Service Coverage", "Debt Service", "Total DCR", "DCR", "D.S.C.R.", "D.C.R", "Total D.C.R", "Total DSCR", "Total D.S.C.R.", "NOI", "Net Operating Income", "Net Income", "Current NOI", "N.O.I.", "Current N.O.I.", "Asset Type", "Type", "Country", "Nation", "Status", "Loan Type", "Fixed or Floating", "Type", "All-In Rate", "All In Rate", "I/O or Amort", "Interest Only or Amortizing Debt Service", "Value", "Market Value", "Cap Rate", "Rate", "LTV", "Loan-To-Value", "L.T.V.", "EGI", "Effective Gross Income", "E.G.I", "Lender"];

def validColumnHeader(data):
	for i in range(len(COLUMN_INFO)):
		for header in COLUMN_INFO[i][TEXT]:
			if data == header:
				return True
	return False

def generateData(numRepeats):
	df = pd.DataFrame(columns=['label','text'])
	for i in range(numRepeats):
		generateIndex = random.randint(0,len(COLUMN_INFO) - 1)
		randVal = random.randint(0,len(COLUMN_INFO[generateIndex][TEXT]) - 1)
		df.loc[i, 'label'] = COLUMN_INFO[generateIndex][LABEL]
		df.loc[i, 'text'] = COLUMN_INFO[generateIndex][TEXT][randVal]
	return df

def generateHeaderData(numRepeats):
	df = pd.DataFrame(columns=['label','text'])
	for i in range(numRepeats):
		headerType = random.randint(0,1)
		if headerType == 1:
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
			exportString += HEADERS[random.randint(0, 91)] + " "
	df = pd.DataFrame({ 'label' : "Valid", 'text' : exportString }, index = [1])
	return df


def generateInvalidHeader():
	rand = random.randint(0,1)
	numVals = random.randint(15, 25)
	exportString = ""
	for j in range(0,numVals):
			rand = random.randint(0,10)
			if(rand == 0): exportString += str(random.randint(1,12)) + "/" + str(random.randint(1,31)) + "/" + str(random.randint(2000,2022)) + " "
			elif(rand == 1): exportString += HEADERS[random.randint(0,91)] + " "
			else: exportString += "nan "
	df = pd.DataFrame({'label' : "Invalid", 'text' : exportString }, index = [1])
	return df