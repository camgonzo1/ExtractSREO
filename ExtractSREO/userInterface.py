from PyQt5 import QtCore, QtGui, QtWidgets
import ExtractSREO as ExtractSREO
from prepareData import *
import trainModel as trainModel
import ctypes
import tkinter as tk
from tkinter import filedialog
import random
import os

root = tk.Tk()
root.withdraw()
trainColumn = True
modelName = ""
controller = None


class chooseModelWindow(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		layout = QtWidgets.QVBoxLayout()
		self.buttonBox = QtWidgets.QHBoxLayout()

		self.newModelButton = QtWidgets.QPushButton("Create New Model")
		self.buttonBox.addWidget(self.newModelButton)
		self.newModelButton.clicked.connect(self.createNewModel)

		self.oldModelButton = QtWidgets.QPushButton("Use Existing Model")
		self.oldModelButton.clicked.connect(self.useOldModel)
		self.buttonBox.addWidget(self.oldModelButton)
		layout.addLayout(self.buttonBox)
		self.setLayout(layout)

	def createNewModel(self):
		self.popup = newModelPopup()
		self.popup.show()
		self.popup.closeWindows.connect(lambda:self.close())

	def useOldModel(self):
		global modelName
		fileName = filedialog.askopenfilename()
		modelName = fileName.split(".")[0]
		ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 4)
		trainModel.trainModel(True, False, modelName, "trainingData.csv")
		self.close()
		

class newModelPopup(QtWidgets.QWidget):
	closeWindows = QtCore.pyqtSignal()
	def __init__(self):
		super().__init__()
		layout = QtWidgets.QVBoxLayout()
		self.textLabel = QtWidgets.QLabel("Enter Model Name:")
		self.hbox = QtWidgets.QHBoxLayout()
		self.input = QtWidgets.QLineEdit()
		self.createButton = QtWidgets.QPushButton("Create")
		self.createButton.clicked.connect(self.createModel)
		layout.addWidget(self.textLabel)
		layout.addLayout(self.hbox)
		self.hbox.addWidget(self.input)
		self.hbox.addWidget(self.createButton)

		self.setLayout(layout)

	def createModel(self):
		global modelName, controller
		modelName = "Model/" + self.input.text()
		ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 4)
		trainModel.trainModel(True,True,modelName,"trainingData.csv")
		controller.showTrainTestWindow()
		self.closeWindows.emit()
		self.close()

class trainTestWindow(QtWidgets.QWidget):
	switch_window = QtCore.pyqtSignal()

	def changeToGenerateDataWindow(self):
		self.switch_window.emit()

	def __init__(self):
		super().__init__()
		
		layout = QtWidgets.QVBoxLayout()
		self.setLayout(layout)

		self.tabs = QtWidgets.QTabWidget()
		self.tabs.addTab(self.trainTabUI(),"Train")
		self.tabs.addTab(self.testTabUI(),"Test")
		layout.addWidget(self.tabs)

	def trainTabUI(self):
		self.trainTab = QtWidgets.QWidget()
		self.layout = QtWidgets.QVBoxLayout()
		self.trainText = QtWidgets.QLabel("Train Column Classification or Header Classification Model?")
		self.checkRow = QtWidgets.QHBoxLayout()
		self.buttonRow = QtWidgets.QHBoxLayout()

		self.columnCheck = QtWidgets.QCheckBox("Column Model")
		self.columnCheck.setChecked(trainColumn)
		self.columnCheck.clicked.connect(self.columnOrHeaderCheck)
		self.checkRow.addWidget(self.columnCheck)
		self.headerCheck = QtWidgets.QCheckBox("Header Model")
		self.headerCheck.setChecked(not trainColumn)
		self.headerCheck.clicked.connect(self.columnOrHeaderCheck)
		self.checkRow.addWidget(self.headerCheck)

		self.newDatasetButton = QtWidgets.QPushButton("Generate New Dataset")
		self.buttonRow.addWidget(self.newDatasetButton)
		self.newDatasetButton.clicked.connect(self.changeToGenerateDataWindow)
		self.oldDatasetButton = QtWidgets.QPushButton("Use Existing Dataset")
		self.buttonRow.addWidget(self.oldDatasetButton)
		self.oldDatasetButton.clicked.connect(self.chooseTrainModel)

		self.trainModelButton = QtWidgets.QPushButton("Train Model")

		self.layout.addWidget(self.trainText)
		self.layout.addLayout(self.checkRow)
		self.layout.addLayout(self.buttonRow)

		self.trainTab.setLayout(self.layout)
		return self.trainTab

	def testTabUI(self):
		self.testTab = QtWidgets.QWidget()
		self.layout = QtWidgets.QVBoxLayout()
		self.textInputRow = QtWidgets.QHBoxLayout()
		self.chooseFilesRow = QtWidgets.QHBoxLayout()
		self.topRow = QtWidgets.QHBoxLayout()

		self.chooseModelButton = QtWidgets.QPushButton("Choose Model")
		self.chooseModelButton.clicked.connect(self.chooseTestModel)
		self.topRow.addWidget(self.chooseModelButton)
		self.modelLabel = QtWidgets.QLabel("No Model Chosen")
		self.topRow.addWidget(self.modelLabel)

		self.testText = QtWidgets.QLabel("Test Inputted Text")
		self.testSREOs = QtWidgets.QLabel("Test SREOs")

		self.textInput = QtWidgets.QLineEdit()
		self.textInputRow.addWidget(self.textInput)

		self.testInputButton = QtWidgets.QPushButton("Test Input")
		self.textInputRow.addWidget(self.testInputButton)
		self.testInputButton.setDisabled(True)

		self.singleFileButton = QtWidgets.QPushButton("Choose Individual File")
		self.singleFileButton.clicked.connect(self.useExistingFile)
		self.chooseFilesRow.addWidget(self.singleFileButton)
		self.singleFileButton.setDisabled(True)

		self.allFilesButton = QtWidgets.QPushButton("Test All Files")
		self.chooseFilesRow.addWidget(self.allFilesButton)
		self.allFilesButton.setDisabled(True)
		self.allFilesButton.clicked.connect(self.useAllFiles)

		self.layout.addLayout(self.topRow)
		self.layout.addWidget(self.testText)
		self.layout.addLayout(self.textInputRow)
		self.layout.addWidget(self.testSREOs)
		self.layout.addLayout(self.chooseFilesRow)

		self.testTab.setLayout(self.layout)
		return self.testTab

	def chooseTrainModel(self):
		self.chooseModelPopup = chooseModelWindow()
		self.chooseModelPopup.show()

	def columnOrHeaderCheck(self):
		global trainColumn
		if(trainColumn):
			trainColumn = False
			self.columnCheck.setChecked(False)
			self.headerCheck.setChecked(True)
		else:
			trainColumn = True
			self.columnCheck.setChecked(True)
			self.headerCheck.setChecked(False)

	def chooseTestModel(self):
		fileName = filedialog.askopenfilename()
		modelName = fileName.split("/")[len(fileName.split("/")) - 1]
		if(fileName.split(".")[1] != "pt"):
			self.modelLabel.setText("Invalid Model File!")
		else:
			ExtractSREO.setModelName(fileName.split(".")[0])
			self.modelLabel.setText(modelName.split(".")[0] + " Selected")
			self.testInputButton.setDisabled(False)
			self.singleFileButton.setDisabled(False)
			self.allFilesButton.setDisabled(False)

	def useExistingFile(self):
		fileName = filedialog.askopenfilename()
		fileType = fileName.split(".")[1]
		if(fileType == ".csv" or fileType == ".pdf" or fileType == ".xlsx"):
			data = ExtractSREO.extractSREO(trainColumn, fileName)
			ExtractSREO.testConfidence(True, data)
		else:
			self.testSREOs.setText("Invalid file type")

	def useAllFiles(self):
		os.chdir(os.path.dirname(os.path.abspath(__file__)))
		for fileName in os.listdir("SREOs/CSVs/"):
			print(fileName)
			print('------------------------------------------------------------')
			data = ExtractSREO.extractSREO(True, "SREOs/CSVs/" + fileName)
			print(data.to_string())
			ExtractSREO.testConfidence(True, data)
			print('------------------------------------------------------------')


class generateDataWindow(QtWidgets.QWidget):
	
	switch_window = QtCore.pyqtSignal()
	def changeToTrainTestWindow(self):
		self.switch_window.emit()

	def __init__(self):
		super().__init__()
		self.checkValues = [[True,True,True,True],
							[True,True,True,True],
							[True,True,True,True],
							[True,True,True,True],
							[True,True,True,True],
							[True,True,True]]

		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.verticalLayout.setContentsMargins(15, 15, 15, 15)
		self.topBar = QtWidgets.QHBoxLayout()

		self.checksGrid = QtWidgets.QGridLayout()
		self.checksGrid.setHorizontalSpacing(15)
		self.checksGrid.setVerticalSpacing(30)

		self.textInputRow = QtWidgets.QHBoxLayout()

		self.bottomRows = QtWidgets.QVBoxLayout()

		#-------------------------------Check Boxes---------------------------------------
		self.addressCheck = QtWidgets.QCheckBox("Property Address")
		self.addressCheck.setChecked(self.checkValues[0][0])
		self.checksGrid.addWidget(self.addressCheck,0,0)
		self.addressCheck.clicked.connect(self.boxChecked)

		self.nameCheck = QtWidgets.QCheckBox("Property Name")
		self.nameCheck.setChecked(self.checkValues[1][0])
		self.checksGrid.addWidget(self.nameCheck,1,0)
		self.nameCheck.clicked.connect(self.boxChecked)


		self.cityCheck = QtWidgets.QCheckBox("City")
		self.cityCheck.setChecked(self.checkValues[2][0])
		self.checksGrid.addWidget(self.cityCheck,2,0)
		self.cityCheck.clicked.connect(self.boxChecked)

		self.stateCheck = QtWidgets.QCheckBox("State")
		self.stateCheck.setChecked(self.checkValues[3][0])
		self.checksGrid.addWidget(self.stateCheck,3,0)

		self.propertyTypeCheck = QtWidgets.QCheckBox("Property Type")
		self.propertyTypeCheck.setChecked(self.checkValues[4][0])
		self.checksGrid.addWidget(self.propertyTypeCheck,4,0)
		self.propertyTypeCheck.clicked.connect(self.boxChecked)

		self.unitsCheck = QtWidgets.QCheckBox("Units")
		self.unitsCheck.setChecked(self.checkValues[5][0])
		self.checksGrid.addWidget(self.unitsCheck,5,0)

		self.sqFtCheck = QtWidgets.QCheckBox("Square Feet")
		self.sqFtCheck.setChecked(self.checkValues[0][1])
		self.checksGrid.addWidget(self.sqFtCheck,0,1)
		self.sqFtCheck.clicked.connect(self.boxChecked)

		self.occupancyCheck = QtWidgets.QCheckBox("Occupancy")
		self.occupancyCheck.setChecked(self.checkValues[1][1])
		self.checksGrid.addWidget(self.occupancyCheck,1,1)
		self.occupancyCheck.clicked.connect(self.boxChecked)

		self.indexCheck = QtWidgets.QCheckBox("Index")
		self.indexCheck.setChecked(self.checkValues[2][1])
		self.checksGrid.addWidget(self.indexCheck,2,1)
		self.indexCheck.clicked.connect(self.boxChecked)

		self.lenderCheck = QtWidgets.QCheckBox("Lender")
		self.lenderCheck.setChecked(self.checkValues[3][1])
		self.checksGrid.addWidget(self.lenderCheck,3,1)
		self.lenderCheck.clicked.connect(self.boxChecked)

		self.loanAmountCheck = QtWidgets.QCheckBox("Loan Amount")
		self.loanAmountCheck.setChecked(self.checkValues[4][1])
		self.checksGrid.addWidget(self.loanAmountCheck,4,1)
		self.loanAmountCheck.clicked.connect(self.boxChecked)

		self.marketValueCheck = QtWidgets.QCheckBox("Market Value")
		self.marketValueCheck.setChecked(self.checkValues[5][1])
		self.checksGrid.addWidget(self.marketValueCheck,5,1)
		self.marketValueCheck.clicked.connect(self.boxChecked)

		self.spreadCheck = QtWidgets.QCheckBox("Spread")
		self.spreadCheck.setChecked(self.checkValues[0][2])
		self.checksGrid.addWidget(self.spreadCheck,0,2)
		self.spreadCheck.clicked.connect(self.boxChecked)

		self.debtServiceCheck = QtWidgets.QCheckBox("Debt Service")
		self.debtServiceCheck.setChecked(self.checkValues[1][2])
		self.checksGrid.addWidget(self.debtServiceCheck,1,2)
		self.debtServiceCheck.clicked.connect(self.boxChecked)

		self.NOICheck = QtWidgets.QCheckBox("NOI")
		self.NOICheck.setChecked(self.checkValues[2][2])
		self.checksGrid.addWidget(self.NOICheck,2,2)
		self.NOICheck.clicked.connect(self.boxChecked)

		self.DSCRCheck = QtWidgets.QCheckBox("DSCR")
		self.DSCRCheck.setChecked(self.checkValues[3][2])
		self.checksGrid.addWidget(self.DSCRCheck,3,2)
		self.DSCRCheck.clicked.connect(self.boxChecked)

		self.LTVCheck = QtWidgets.QCheckBox("LTV")
		self.LTVCheck.setChecked(self.checkValues[4][2])
		self.checksGrid.addWidget(self.LTVCheck,4,2)
		self.LTVCheck.clicked.connect(self.boxChecked)

		self.rateTypeCheck = QtWidgets.QCheckBox("Rate Type")
		self.rateTypeCheck.setChecked(self.checkValues[5][2])
		self.checksGrid.addWidget(self.rateTypeCheck,5,2)
		self.rateTypeCheck.clicked.connect(self.boxChecked)

		self.amortDateCheck = QtWidgets.QCheckBox("Amort Start Date")
		self.amortDateCheck.setChecked(self.checkValues[0][3])
		self.checksGrid.addWidget(self.amortDateCheck,0,3)
		self.amortDateCheck.clicked.connect(self.boxChecked)

		self.maturityDateCheck = QtWidgets.QCheckBox("Maturity Date")
		self.maturityDateCheck.setChecked(self.checkValues[1][3])
		self.checksGrid.addWidget(self.maturityDateCheck,1,3)
		self.maturityDateCheck.clicked.connect(self.boxChecked)

		self.acquisitionDateCheck = QtWidgets.QCheckBox("Acquisition Date")
		self.acquisitionDateCheck.setChecked(self.checkValues[2][3])
		self.checksGrid.addWidget(self.acquisitionDateCheck,2,3)
		self.acquisitionDateCheck.clicked.connect(self.boxChecked)

		self.allInRateCheck = QtWidgets.QCheckBox("All-In Rate")
		self.allInRateCheck.setChecked(self.checkValues[3][3])
		self.checksGrid.addWidget(self.allInRateCheck,3,3)
		self.allInRateCheck.clicked.connect(self.boxChecked)

		self.currentBalanceCheck = QtWidgets.QCheckBox("Current Balance")
		self.currentBalanceCheck.setChecked(self.checkValues[4][3])
		self.checksGrid.addWidget(self.currentBalanceCheck,4,3)
		self.currentBalanceCheck.clicked.connect(self.boxChecked)

		self.checkVars = [[self.addressCheck,self.sqFtCheck,self.spreadCheck,self.amortDateCheck],
						  [self.nameCheck,self.occupancyCheck,self.debtServiceCheck,self.maturityDateCheck],
						  [self.cityCheck,self.indexCheck,self.NOICheck,self.acquisitionDateCheck],
						  [self.stateCheck,self.lenderCheck,self.DSCRCheck,self.allInRateCheck],
						  [self.propertyTypeCheck,self.loanAmountCheck,self.LTVCheck,self.currentBalanceCheck],
						  [self.unitsCheck,self.marketValueCheck,self.rateTypeCheck]]

		#-------------------------------Labels---------------------------------------
		self.generateNewDataLabel = QtWidgets.QLabel("Generate New Data for Training")
		self.topBar.addWidget(self.generateNewDataLabel)

		self.numberOfDataPointsLabel = QtWidgets.QLabel("# of each data point generated:")
		self.textInputRow.addWidget(self.numberOfDataPointsLabel)
		#-------------------------------Buttons---------------------------------------
		self.toggleAllButton = QtWidgets.QPushButton("Toggle All")
		self.topBar.addWidget(self.toggleAllButton)
		self.toggleAllButton.clicked.connect(self.toggleAll)

		self.generateDataButton = QtWidgets.QPushButton("Generate Data")
		self.generateDataButton.clicked.connect(self.generateColumnData)

		self.doneButton = QtWidgets.QPushButton("Done")
		self.doneButton.clicked.connect(self.train)
		#-------------------------------Misc---------------------------------------
		self.numRepeatsInput = QtWidgets.QLineEdit()
		self.numRepeatsInput.setMaxLength(7)
		self.textInputRow.addWidget(self.numRepeatsInput)
		self.textInputRow.addWidget(self.generateDataButton)

		self.progressBar = QtWidgets.QProgressBar()
		palette = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
		self.progressBar.setPalette(palette)
		self.progressBar.setStyleSheet("QProgressBar { border: 2px solid grey; border-radius: 0px; text-align: center; } QProgressBar::chunk {background-color: #16aff0; width: 1px;}")
		self.progressBar.setProperty("value", 0)

		self.verticalLayout.addLayout(self.topBar)
		self.verticalLayout.addLayout(self.checksGrid)
		self.bottomRows.addLayout(self.textInputRow)
		self.bottomRows.addWidget(self.progressBar)
		self.bottomRows.addWidget(self.doneButton)
		self.verticalLayout.addLayout(self.bottomRows)

		self.resize(1280,720)
		self.setLayout(self.verticalLayout)

	def train(self):
		self.chooseModelPopup = chooseModelWindow()
		self.chooseModelPopup.show()

	def boxChecked(self):
		for i in range(len(self.checkVars)):
			for j in range(len(self.checkVars[i])):
				self.checkValues[i][j] = self.checkVars[i][j].isChecked()

	def toggleAll(self):
		containsFalse = False
		for row in self.checkValues:
			if False in row: containsFalse = True
		for i in range(len(self.checkVars)):
			for j in range(len(self.checkVars[i])):
				self.checkVars[i][j].setChecked(containsFalse)
				self.checkValues[i][j] = containsFalse

	def generateColumnData(self):
		self.numRepeats = self.numRepeatsInput.text()
		if(self.numRepeats.isnumeric()):
			self.numRepeats = int(self.numRepeats)
			self.generateData()
		else:
			self.generateNewDataLabel.setText("Please enter a number")

	def incrementProgressBar(self, val):
		self.progressBar.setValue(self.progressBar.value() + val)

	def generateData(self):
		fileName = "trainingData.csv"
		trainingData = pd.DataFrame(columns=['label','text'])
		columnFunctions = [[createAddresses, createSqFootage, createSpread, createAmortStartDate],
						   [createPropertyName, createOccupancy, createDebtService, createMaturityDate],
						   [createCity, createIndex, createNOI, createAcquisitionDate],
						   [createState, createLender, createDSCR, createAllInRate],
						   [createPropertyType, createLoanAmount, createLTV, createCurrentBalance],
						   [createUnits, createMV, createRateTypes]]
		trueValues = []
		for i in range(len(self.checkValues)):
			for j in range(len(self.checkValues[i])):
				if(self.checkValues[i][j]):
					trueValues.append([i,j])
		if(trainColumn):
			i = 0
			while i < self.numRepeats:
				randVal = random.randint(0,len(trueValues) - 1)
				row = trueValues[randVal][0]
				col = trueValues[randVal][1]
				if(self.checkValues[row][col]):
					trainingData = pd.concat([trainingData, columnFunctions[row][col]()],ignore_index=True)
					i += 1
				if(i % (self.numRepeats / 50) == 0):
					self.incrementProgressBar(2)
		print("Done")
		trainingData.to_csv(fileName, index=False)
		

class Controller:
	def __init__(self):
		pass

	def showTrainTestWindow(self):
		self.trainTest = trainTestWindow()
		self.generateData = generateDataWindow()
		self.trainTest.switch_window.connect(self.showGenerateDataWindow)
		self.generateData.close()
		self.trainTest.show()

	def showGenerateDataWindow(self):
		self.generateData.switch_window.connect(self.showTrainTestWindow)
		self.trainTest.close()
		self.generateData.show()

def showConsole():
	ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 4)

if __name__ == "__main__":
	import sys
	ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
	#if(input("1 for UI 2 for command prompt ") == "2"):
		#ExtractSREO.runTests(trainColumn)
	app = QtWidgets.QApplication(sys.argv)
	controller = Controller()
	controller.showTrainTestWindow()
	sys.exit(app.exec_())
