from pickle import TRUE
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

	def useOldModel(self):
		global modelName
		fileName = filedialog.askopenfilename()
		modelName = fileName.split(".")[0]
		#showConsole()
		if trainColumn: trainingData = "trainingData.csv"
		else: trainingData = "trainingHeaderData.csv"
		trainModel.trainModel(trainColumn, False, modelName, trainingData)
		controller.showTrainTestWindow()
		self.close()

class createBetterModelPopup(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QtWidgets.QVBoxLayout()
		self.buttonRow = QtWidgets.QHBoxLayout()
		self.topLabel = QtWidgets.QLabel("Make model with certain errors or make model better than current?")
		self.certainErrorsButton = QtWidgets.QPushButton("Certain Errors")
		self.certainErrorsButton.clicked.connect(self.certainErrorsButtonPressed)
		self.betterThanCurrentButton = QtWidgets.QPushButton("Better Than Current")
		self.betterThanCurrentButton.clicked.connect(self.betterThanCurrentButtonPressed)

		self.layout.addWidget(self.topLabel)
		self.buttonRow.addWidget(self.certainErrorsButton)
		self.buttonRow.addWidget(self.betterThanCurrentButton)
		self.layout.addLayout(self.buttonRow)
		
		self.setLayout(self.layout)

	def certainErrorsButtonPressed(self):
		newLayout = QtWidgets.QHBoxLayout()
		self.numberOfErrorsLabel = QtWidgets.QLabel("Number of errors to beat:")
		self.numberOfErrorsInput = QtWidgets.QLineEdit()
		self.generateButton = QtWidgets.QPushButton("Generate")
		self.generateButton.clicked.connect(self.generateButtonPressed)
		newLayout.addWidget(self.numberOfErrorsLabel)
		newLayout.addWidget(self.numberOfErrorsInput)
		newLayout.addWidget(self.generateButton)

		self.layout.addLayout(newLayout)

	def generateButtonPressed(self):
		self.goal = int(self.numberOfErrorsInput.text())
		self.createModel()

	def betterThanCurrentButtonPressed(self):
		ExtractSREO.setModelName(filedialog.askopenfilename().split(".")[0])
		self.goal = ExtractSREO.testOnSolvedCSV()
		self.createModel

	def createModel(self):
		trainingData = pd.DataFrame(columns=['label','text'])
		count = 1
		numReps = random.randint(1, 100) * 100
		modelName = "newTrial1-" + str(numReps)
		ExtractSREO.setModelName(modelName)
		for i in range(numReps):
			randVal = random.randint(0,23)
			trainingData = pd.concat([trainingData, generateData(randVal)],ignore_index=True)
		trainModel.trainModel(True, True, modelName,"trainingData.csv")
		while ExtractSREO.testOnSolvedCSV() >= self.goal:
			print("----------------------------------------------------------------------------------")
			numReps = random.randint(10, 100) * 100
			modelName = "newTrial" + str(count) + "-" + str(numReps)
			ExtractSREO.setModelName(modelName)
			for i in range(numReps):
				randVal = random.randint(0,23)
				trainingData = pd.concat([trainingData, generateData(randVal)],ignore_index=True)
			trainModel.trainModel(True,True,modelName,"trainingData.csv")
			count += 1
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print("New Best Model = " + modelName)

class newModelPopup(QtWidgets.QWidget):
	#closeWindows = QtCore.pyqtSignal()
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
		#showConsole()
		if trainColumn: trainingData = "trainingData.csv"
		else: trainingData = "trainingHeaderData.csv"
		trainModel.trainModel(trainColumn,True,modelName,trainingData)
		controller.showTrainTestWindow()
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
		self.trainTab = trainTabUI()
		self.trainTab.switch_window.connect(self.changeToGenerateDataWindow)
		self.tabs.addTab(self.trainTab,"Train")
		self.testTab = testTabUI()
		self.tabs.addTab(self.testTab,"Test")
		self.extractTab = extractTabUI()
		self.tabs.addTab(self.extractTab,"Extract")
		layout.addWidget(self.tabs)

class trainTabUI(QtWidgets.QWidget):
	switch_window = QtCore.pyqtSignal()

	def changeToGenerateDataWindow(self):
		self.switch_window.emit()

	def __init__(self):
		super().__init__()
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
		self.createBetterModelButton = QtWidgets.QPushButton("Experimental Data Eval")
		self.createBetterModelButton.clicked.connect(self.createBetterModelButtonPressed)
		self.buttonRow.addWidget(self.createBetterModelButton)

		self.trainModelButton = QtWidgets.QPushButton("Train Model")

		self.layout.addWidget(self.trainText)
		self.layout.addLayout(self.checkRow)
		self.layout.addLayout(self.buttonRow)

		self.setLayout(self.layout)

	def createBetterModelButtonPressed(self):
		self.betterModelPopup = createBetterModelPopup()
		self.betterModelPopup.show()

	def chooseTrainModel(self):
		self.chooseModelPopup = chooseModelWindow()
		self.chooseModelPopup.show()

	def columnOrHeaderCheck(self):
		global trainColumn
		if(trainColumn):
			trainColumn = False
		else:
			trainColumn = True
		self.columnCheck.setChecked(trainColumn)
		self.headerCheck.setChecked(not trainColumn)

class testTabUI(QtWidgets.QWidget):
	switch_window = QtCore.pyqtSignal()

	def changeToGenerateDataWindow(self):
		self.switch_window.emit()

	def __init__(self):
		super().__init__()
		self.layout = QtWidgets.QVBoxLayout()
		self.textInputRow = QtWidgets.QHBoxLayout()
		self.chooseFilesRow = QtWidgets.QHBoxLayout()
		self.topRow = QtWidgets.QHBoxLayout()

		self.chooseModelButton = QtWidgets.QPushButton("Choose Model")
		self.chooseModelButton.clicked.connect(self.chooseTestModel)
		self.topRow.addWidget(self.chooseModelButton)
		self.modelLabel = QtWidgets.QLabel("No Model Chosen")
		self.topRow.addWidget(self.modelLabel)

		self.invalidFileTypeLabel = QtWidgets.QLabel("Invalid File Type: ")
		self.invalidFileTypeLabel.hide()

		self.testText = QtWidgets.QLabel("Test Inputted Text")
		self.testSREOs = QtWidgets.QLabel("Test SREOs")

		self.textInput = QtWidgets.QLineEdit()
		self.textInputRow.addWidget(self.textInput)

		self.testInputButton = QtWidgets.QPushButton("Test Input")
		self.textInputRow.addWidget(self.testInputButton)
		self.testInputButton.setDisabled(True)

		self.singleFileButton = QtWidgets.QPushButton("Choose Individual File(s)")
		self.singleFileButton.clicked.connect(self.useExistingFile)
		self.chooseFilesRow.addWidget(self.singleFileButton)
		self.singleFileButton.setDisabled(True)

		self.allFilesButton = QtWidgets.QPushButton("Test All Files")
		self.chooseFilesRow.addWidget(self.allFilesButton)
		self.allFilesButton.setDisabled(True)
		self.allFilesButton.clicked.connect(self.useAllFiles)

		self.testOnSolvedCSVButton = QtWidgets.QPushButton("Test on Solved CSV")
		self.chooseFilesRow.addWidget(self.testOnSolvedCSVButton)
		self.testOnSolvedCSVButton.setDisabled(True)
		self.testOnSolvedCSVButton.clicked.connect(ExtractSREO.testOnSolvedCSV)

		self.layout.addLayout(self.topRow)
		self.layout.addWidget(self.testText)
		self.layout.addLayout(self.textInputRow)
		self.layout.addWidget(self.testSREOs)
		self.layout.addLayout(self.chooseFilesRow)
		self.layout.addWidget(self.invalidFileTypeLabel)

		self.setLayout(self.layout)

	def columnOrHeaderCheck(self):
		global trainColumn
		if(trainColumn):
			trainColumn = False
		else:
			trainColumn = True
		self.columnCheck.setChecked(trainColumn)
		self.headerCheck.setChecked(not trainColumn)

	def chooseTestModel(self):
		fileName = filedialog.askopenfilename()
		if(fileName == ""):
			self.invalidFileTypeLabel.setText("Invalid File Type: " + fileName.split("/")[len(fileName.split("/")) - 1])
			self.invalidFileTypeLabel.show()
		elif(fileName.split(".")[len(fileName.split(".")) - 1] != "pt"):
			self.invalidFileTypeLabel.setText("Invalid File Type: " + fileName.split("/")[len(fileName.split("/")) - 1])
			self.invalidFileTypeLabel.show()
		else:
			self.invalidFileTypeLabel.hide()
			modelName = fileName.split("/")[len(fileName.split("/")) - 1]
			ExtractSREO.setModelName(fileName.split(".")[0])
			self.modelLabel.setText(modelName.split(".")[0] + " Selected")
			self.testInputButton.setDisabled(False)
			self.singleFileButton.setDisabled(False)
			self.allFilesButton.setDisabled(False)
			self.testOnSolvedCSVButton.setDisabled(False)

	def useAllFiles(self):
		#showConsole()
		os.chdir(os.path.dirname(os.path.abspath(__file__)))
		for fileName in os.listdir("SREOs/CSVs/"):
			print(fileName)
			print('------------------------------------------------------------')
			data = ExtractSREO.extractSREO("SREOs/CSVs/" + fileName)
			print(data.to_string())
			ExtractSREO.testConfidence(True, data)
			print('------------------------------------------------------------')
	
	def useExistingFile(self):
		fileName = filedialog.askopenfilenames()
		if type(fileName) is tuple:
			for file in fileName:
				print(file)
				fileType = file.split(".")[len(file.split(".")) - 1]
				if(fileType == "csv" or fileType == "pdf" or fileType == "xlsx"):
					self.invalidFileTypeLabel.hide()
					data = ExtractSREO.extractSREO(file)
					ExtractSREO.testConfidence(True, data)
					print()
				else:
					self.invalidFileTypeLabel.setText("Invalid File Type: " + file)
					self.invalidFileTypeLabel.show()
		else:
			fileType = fileName.split(".")[len(fileName.split(".")) - 1]
			if(fileType == "csv" or fileType == "pdf" or fileType == "xlsx"):
				data = ExtractSREO.extractSREO(fileName)
				ExtractSREO.testConfidence(True, data)
			else:
				self.invalidFileTypeLabel.setText("Invalid File Type: " + fileName.split("/")[len(fileName.split("/")) - 1])
				self.invalidFileTypeLabel.show()

class extractTabUI(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QtWidgets.QHBoxLayout()
		self.leftColumn = QtWidgets.QVBoxLayout()
		self.rightColumn = QtWidgets.QVBoxLayout()
		self.backNextButtonsRow = QtWidgets.QHBoxLayout()

		self.table = QtWidgets.QTableWidget()
		self.chooseModelButton = QtWidgets.QPushButton("Choose Model")
		self.chooseFileButton = QtWidgets.QPushButton("Choose File(s)")
		self.chooseFileButton.clicked.connect(self.extractFile)
		self.backButton = QtWidgets.QPushButton("Back")
		self.backNextButtonsRow.addWidget(self.backButton)
		self.nextButton = QtWidgets.QPushButton("Next")
		self.backNextButtonsRow.addWidget(self.nextButton)

		self.layout.addLayout(self.leftColumn)
		self.layout.addLayout(self.rightColumn)
		self.rightColumn.addWidget(self.table)
		self.rightColumn.addLayout(self.backNextButtonsRow)
		self.leftColumn.addWidget(self.chooseFileButton)
		
		self.setLayout(self.layout)

	def extractFile(self):
		fileName = filedialog.askopenfilename()
		df = ExtractSREO.extractSREO(fileName)
		print(df)
		self.table.setColumnCount(len(df.columns))
		self.table.setRowCount(len(df.columns[1]))
		print(str(len(df.columns)) + " " + str(len(df.columns[1])))
		for i in range(len(df.columns)):
			cellIndex = 0
			for column in df.columns:
				item = QtWidgets.QTableWidgetItem(str(column[cellIndex]))
				self.table.setItem(i,cellIndex,item)
				cellIndex += 1
			

class generateColumnDataWindow(QtWidgets.QWidget):
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
		self.buttonRow = QtWidgets.QHBoxLayout()

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

		self.numberOfDataPointsLabel = QtWidgets.QLabel("Total # of data points created: ")
		self.textInputRow.addWidget(self.numberOfDataPointsLabel)

		self.createNewModelWarningText = QtWidgets.QLabel("Note: In order to create a new model all data types must be selected")
		#-------------------------------Buttons---------------------------------------
		self.toggleAllButton = QtWidgets.QPushButton("Toggle All")
		self.topBar.addWidget(self.toggleAllButton)
		self.toggleAllButton.clicked.connect(self.toggleAll)

		self.generateDataButton = QtWidgets.QPushButton("Generate Data")

		self.generateDataButton.clicked.connect(self.generateDataButtonPressed)
		self.generateDataButton.setDisabled(True)

		self.cancelButton = QtWidgets.QPushButton("Cancel")
		self.cancelButton.clicked.connect(self.changeToTrainTestWindow)

		self.doneButton = QtWidgets.QPushButton("Done")
		self.doneButton.clicked.connect(self.train)
		#-------------------------------Misc---------------------------------------
		self.numRepeatsInput = QtWidgets.QLineEdit()
		self.numRepeatsInput.setMaxLength(7)
		self.numRepeatsInput.textEdited.connect(self.textInputted)
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
		self.buttonRow.addWidget(self.cancelButton)
		self.buttonRow.addWidget(self.doneButton)
		self.bottomRows.addLayout(self.buttonRow)
		self.bottomRows.addWidget(self.createNewModelWarningText,stretch=0)
		self.verticalLayout.addLayout(self.bottomRows)

		self.resize(1280,640)
		self.setLayout(self.verticalLayout)

	def train(self):
		self.chooseModelPopup = chooseModelWindow()
		self.chooseModelPopup.show()
		#self.chooseModelPopup.switchWindow.connect(lambda:self.switch_window.emit())

	def boxChecked(self):
		for i in range(len(self.checkVars)):
			for j in range(len(self.checkVars[i])):
				self.checkValues[i][j] = self.checkVars[i][j].isChecked()
		containsTrue = False
		for row in self.checkValues:
			if(True in row):
				containsTrue = True
				continue
		self.generateDataButton.setDisabled(not containsTrue)

	def toggleAll(self):
		containsFalse = False
		for row in self.checkValues:
			if False in row: containsFalse = True
		for i in range(len(self.checkVars)):
			for j in range(len(self.checkVars[i])):
				self.checkVars[i][j].setChecked(containsFalse)
				self.checkValues[i][j] = containsFalse
				self.generateDataButton.setDisabled(not containsFalse)

	def incrementProgressBar(self, val):
		self.progressBar.setValue(self.progressBar.value() + val)

	def textInputted(self):
		if self.numRepeatsInput.text().isnumeric():
			self.numRepeats = int(self.numRepeatsInput.text())
			self.numberOfDataPointsLabel.setText("Total # of data points created: ")
			self.generateDataButton.setDisabled(False)
		else:
			self.generateDataButton.setDisabled(True)
			self.numberOfDataPointsLabel.setText("Please enter a number           ")

	def generateDataButtonPressed(self):
		self.progressBar.setValue(0)
		self.doneButton.setDisabled(True)
		fileName = "trainingData.csv"
		trainingData = pd.DataFrame(columns=['label','text'])
		trueValues = []
		for i in range(len(self.checkValues)):
			for j in range(len(self.checkValues[i])):
				if(self.checkValues[i][j]):
					trueValues.append((4 * i) + j)
		if(trainColumn):
			total = 0
			for i in range(int(self.numRepeats / 1000)):
				for j in range(1000):
					randVal = random.randint(0,len(trueValues) - 1)
					trainingData = pd.concat([trainingData, generateData(trueValues[randVal])],ignore_index=True)
					total += 1
					if(total % (self.numRepeats / 100) == 0):
						self.incrementProgressBar(1)
			for i in range(self.numRepeats % 1000):
				randVal = random.randint(0,len(trueValues) - 1)
				trainingData = pd.concat([trainingData, generateData(trueValues[randVal])],ignore_index=True)
				total += 1
				if(total % (self.numRepeats / 100) == 0):
					self.incrementProgressBar(1)
		trainingData.to_csv(fileName, index=False)
		self.doneButton.setDisabled(False)

class generateHeaderDataWindow(QtWidgets.QWidget):
	switch_window = QtCore.pyqtSignal()

	def changeToTrainTestWindow(self):
		self.switch_window.emit()

	def __init__(self):
		super().__init__()

		self.generateValid = True
		self.generateInvalid = True

		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.verticalLayout.setContentsMargins(15, 15, 15, 15)
		self.checksRow = QtWidgets.QHBoxLayout()
		self.textInputRow = QtWidgets.QHBoxLayout()
		self.buttonRow = QtWidgets.QHBoxLayout()
		self.bottomRows = QtWidgets.QVBoxLayout()

		self.topLabel = QtWidgets.QLabel("Generate Header Data")
		self.validCheck = QtWidgets.QCheckBox("Valid")
		self.validCheck.setChecked(self.generateValid)
		self.validCheck.clicked.connect(self.validChecked)
		self.checksRow.addWidget(self.validCheck)
		self.invalidCheck = QtWidgets.QCheckBox("Invalid")
		self.invalidCheck.setChecked(self.generateInvalid)
		self.invalidCheck.clicked.connect(self.invalidChecked)
		self.checksRow.addWidget(self.invalidCheck)

		self.inputLabel = QtWidgets.QLabel("Total # of data points created: ")
		self.textInputRow.addWidget(self.inputLabel)
		self.numRepeatsInput = QtWidgets.QLineEdit()
		self.numRepeatsInput.textEdited.connect(self.textInputted)
		self.textInputRow.addWidget(self.numRepeatsInput)
		self.generateDataButton = QtWidgets.QPushButton("Generate Data")
		self.generateDataButton.clicked.connect(self.generateData)
		self.textInputRow.addWidget(self.generateDataButton)

		self.progressBar = QtWidgets.QProgressBar()
		palette = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
		self.progressBar.setPalette(palette)
		self.progressBar.setStyleSheet("QProgressBar { border: 2px solid grey; border-radius: 0px; text-align: center; } QProgressBar::chunk {background-color: #16aff0; width: 1px;}")
		self.progressBar.setProperty("value", 0)

		self.cancelButton = QtWidgets.QPushButton("Cancel")
		self.cancelButton.clicked.connect(self.changeToTrainTestWindow)

		self.doneButton = QtWidgets.QPushButton("Done")
		self.doneButton.clicked.connect(self.train)

		self.verticalLayout.addWidget(self.topLabel)
		self.verticalLayout.addLayout(self.checksRow)
		self.verticalLayout.addLayout(self.textInputRow)
		self.verticalLayout.addWidget(self.progressBar)
		self.buttonRow.addWidget(self.cancelButton)
		self.buttonRow.addWidget(self.doneButton)
		self.verticalLayout.addLayout(self.buttonRow)

		self.setLayout(self.verticalLayout)

	def incrementProgressBar(self, val):
		self.progressBar.setValue(self.progressBar.value() + val)

	def validChecked(self):
		self.generateValid = not self.generateValid
		self.validCheck.setChecked(self.generateValid)

	def invalidChecked(self):
		self.generateInvalid = not self.generateInvalid
		self.invalidCheck.setChecked(self.generateInvalid)

	def textInputted(self):
		if self.numRepeatsInput.text().isnumeric():
			self.numRepeats = int(self.numRepeatsInput.text())
			self.inputLabel.setText("Total # of data points created: ")
			self.generateDataButton.setDisabled(False)
		else:
			self.generateDataButton.setDisabled(True)
			self.inputLabel.setText("Please enter a number           ")
		
	def generateData(self):
		self.doneButton.setDisabled(True)
		fileName = "trainingHeaderData.csv"
		trainingData = pd.DataFrame(columns=['label','text'])
		numRepeats = int(self.numRepeatsInput.text())
		for i in range(numRepeats):
			if self.generateValid and self.generateInvalid:
				rand = random.randint(0,1)
				if rand == 0:
					trainingData = pd.concat([trainingData, createValidHeader()], ignore_index = True)
				else:
					trainingData = pd.concat([trainingData, createInvalidHeader()], ignore_index = True)
			elif self.generateValid:
				trainingData = pd.concat([trainingData, createValidHeader()], ignore_index = True)
			elif self.generateInvalid:
				trainingData = pd.concat([trainingData, createValidHeader()], ignore_index = True)
			if(i % (numRepeats / 100) == 0):
					self.incrementProgressBar(1)
		trainingData.to_csv(fileName,index=False)
		self.doneButton.setDisabled(False)

	def train(self):
		self.chooseModelPopup = chooseModelWindow()
		self.chooseModelPopup.show()
		#self.chooseModelPopup.switchWindow.connect(lambda:self.switch_window.emit())

class Controller:
	
	def __init__(self):
		self.trainTest = trainTestWindow()
		self.generateData = generateColumnDataWindow()
		pass

	def showTrainTestWindow(self):
		self.trainTest.switch_window.connect(self.showgenerateColumnDataWindow)
		self.generateData.close()
		self.trainTest.show()

	def showgenerateColumnDataWindow(self):
		self.trainTest.close()
		if trainColumn:
			self.generateData = generateColumnDataWindow()
		else:
			self.generateData = generateHeaderDataWindow()
		self.generateData.show()
		self.generateData.switch_window.connect(self.showTrainTestWindow)

def showConsole():
	ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 4)

if __name__ == "__main__":
	import sys
	#ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
	app = QtWidgets.QApplication(sys.argv)
	controller = Controller()
	controller.showTrainTestWindow()
	sys.exit(app.exec_())
