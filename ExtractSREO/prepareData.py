from lib2to3.pytree import convert
from re import L
import os
import random
from numpy import dtype
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

CATEGORY, INFO = 0, 1
COLUMN_INFO = {  1: ("Loan Amount", ["Loan Amount", "Orig. Loan Amount", "Original Loan Amount", "OG Loan Amount", "Total Loan Amount", "Origional Balance", "Orig. Loan Amt."]), 
				 2: ("Debt Service", ["Debt Service", "Debt Service Value", "Total Debt Service", "Annual Debt Service", "Debt Service Total", "Debt Service Calculation", "2022 Total Debt Service (Projected)"]),
				 3: ("NOI", ["NOI", "Net Operating Income", "Net Income", "Current NOI", "N.O.I.", "Current N.O.I.", "Current Net Operating Income", "Net Rental Income", "NOI", "NOI (Period Ending YTD)", "NOI (12/31/2021)", "2022 Net Operating Income (Projected)", "12/31/2020 NOI"]),
				 4: ("Market Value", ["Market Value", "MV", "Value", "Internal Valuation", "PWC Value", "Market Total Value", "Borrower Started Value", "Full Market Value", "Value/Unit", "Valuation Dec-2020"]), 
				 5: ("Current Balance", ["Outstanding Loan Amount", "Principal Balance", "OPB", "Outstanding Principal Balance", "Current Balance", "Balance", "Current Debt", "Loan Balance", "Current Amount", "Outstanding", "Outstanding Loan(s)", "Outstanding Loans", "Outstanding Debt (YE)", "Outstanding Debt", "Balance of Mortgages", "Mortgage Outstanding", "Mortgage Liens as of ", "OPB (1/31/2022)", "Balance as of *"]),
				 6: ("Occupancy", ["Occupancy", "Current Occupancy", "Occupancy Status", "Current Occupancy (%)", "% Occupied", "% Occupancy", "Occupancy %", "Occupancy at end of quarter", "Occ. %", "Occupancy at end of quarter", "Physical Occupancy"]),
				 7: ("LTV", ["LTV", "LTV", "Loan-To-Value", "Loan To Value"]),
				 8: ("All-In Rate", ["All-In", "All-In Rate", "Rate", "All In", "All In Rate", "All-in", "Interest", "Interest Rate", "Current Rate", "Interest Rate (at 12/31/21)"]),
				 9: ("Acquisition Date", ["Acquisition Date", "Purchase Date", "Date of Acquisition", "Acquistion", "Acquired", "Year Acquired", "Date Acquired", "Origination Date", "Origination", "Year Originated", "Acquisition Date (yr)", "Year of Initial Ownership", "Owned Since", "Acq. Date Cost", "Acquisiton Year"]),
				 10: ("Maturity Date", ["Maturity Date", "Maturity", "Loan Matures", "Matures", "Date of Maturity", "Date Matures", "Maturation Date", "Loan Maturity Date", "Final Maturity", "Maturity Date(s)", "Due Date (year)", "Due Date"]),
				 11: ("Amort Start Date", ["Amort Start Date", "Amortization Start Date", "Amort Date", "Amortization Date", "Amort Start", "Amortization Start", "Commence Date"]),
				 12: ("DSCR", ["DSCR", "Debt Service Coverage", "Total DCR", "DCR", "Total DSCR", "Debt Coverage Ratio", "Debt Service Ratio", "Debt Coverage", "DSC"]),
				 13: ("Units", ["Units", "#units", "# of Units", "Number of Units", "Unit Count", "Multifamily Units (#)", "Multifamily Units", "Units / Sq. Ft.", "# Units / SF", "Units/ Sq. Ft."]),
				 14: ("Square Feet", ["Square Footage", "Square Feet", "Sq. Feet", "Sq. Ft.", "Feet", "Sq. Footage", "SF / # of Units", "SF/Units"]),
				 15: ("Spread", ["Spread", "Credit Spread"]),
				 16: ("Address", ["Property Location", "Location", "Address", "Street Location", "Street Address", "Property Address", "Street", "Full Property Address", "Property Street Address"]),
				 17: ("City", ["City", "Town", "Property City", "Location"]),
				 18: ("Property Type", ["Property Type", "Type of Property", "Type", "Asset Type", "Property Description", "Prop. Type", "Description", "Type of Community"]),
				 19: ("State", ["State", "Providence", "Territory", "Location", "Property State", "ST"]),
				 20: ("Index", ["Index", "Interest Rate Index", "Rate Index"]),
				 21: ("Lender", ["Lender", "Mortgage Holder", "Mortgage Lender", "Lender Name", "Lender Name                         (Confirm if Fannie or Freddie, where applicable)", "Lender (Servicer)"]),
				 22: ("Property Name", ["Property Name", "Name", "Property", "Property Number", "ID", "Property ID", "Building", "Building Number", "Building Name/Number", "Building Name", "Legal Name"]),
				 23: ("Rate Type", ["Loan Type", "Type of Loan", "Fixed or Floating", "Type", "Rate Type", "Type of Rate", "Interest Rate Type", "Type of Interest Rate", "Fixed / Variable", "Floating (Y/N)"])}
	
headers = ["Property Location", "Location", "Address", "Street Location", "Street Address", "Property Address", "Street", "Full Property Address", "Property Street Address City State Zip", "Property Name", "Name", "Property", "Property Number", "City", "Town", "State", "Territory", "Providence", "Units", "#units", "# of Units", "Number of Units", "Built", "Constructed", "Year Constructed", "Year Built", "Date Built", "Date Constructed", "Built (yr)", "Constructed (yr)", "Occupancy", "Current Occupancy (%)", "Current Occupancy", "Occupancy at end of quarter", "Acquisition Date", "Purchase Date", "Date of Acquisition", "Acquisition", "Year Acquired", "Origination Date", "Maturity Date", "Maturity", "Loan Matures", "Matures", "Loan Amount", "Outstanding Loan Amount", "Principle Balance", "OPB", "Outstanding Principal Balance", "O.P.B.", "Orig. Loan Amount", "Original Loan Amount", "Original Amount", "DSCR", "Debt Service Coverage", "Debt Service", "Total DCR", "DCR", "D.S.C.R.", "D.C.R", "Total D.C.R", "Total DSCR", "Total D.S.C.R.", "NOI", "Net Operating Income", "Net Income", "Current NOI", "N.O.I.", "Current N.O.I.", "Asset Type", "Type", "Country", "Nation", "Status", "Loan Type", "Fixed or Floating", "Type", "All-In Rate", "All In Rate", "I/O or Amort", "Interest Only or Amortizing Debt Service", "Value", "Market Value", "Cap Rate", "Rate", "LTV", "Loan-To-Value", "L.T.V.", "EGI", "Effective Gross Income", "E.G.I", "Lender"];



def generateData(generateIndex):
	randVal = random.randint(0,len(COLUMN_INFO[generateIndex][INFO]) - 1)
	df = pd.DataFrame({ 'label' : COLUMN_INFO[generateIndex][CATEGORY], 'text' : COLUMN_INFO[generateIndex][INFO][randVal]}, index=[1])
	return df

def createValidHeader():
	numVals = random.randint(15, 25)
	exportString = ""
	for j in range(numVals):
		rand = random.randint(0,5)
		if(rand == 0):
			exportString += "nan "
		else:
			exportString += headers[random.randint(0, 91)] + " "
	df = pd.DataFrame({ 'label' : "Valid", 'text' : exportString }, index = [1])
	return df


def createInvalidHeader():
	rand = random.randint(0,1)
	numVals = random.randint(15, 25)
	exportString = ""
	for j in range(0,numVals):
			rand = random.randint(0,10)
			if(rand == 0): exportString += str(random.randint(1,12)) + "/" + str(random.randint(1,31)) + "/" + str(random.randint(2000,2022)) + " "
			elif(rand == 1): exportString += headers[random.randint(0,91)] + " "
			else: exportString += "nan "
	df = pd.DataFrame({'label' : "Invalid", 'text' : exportString }, index = [1])
	return df