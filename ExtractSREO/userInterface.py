#from pickle import TRUE
#from re import A
from PyQt5 import QtCore, QtGui, QtWidgets
import fileExtraction as fileExtraction
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

BUTTON_STYLE_SHEET = "QPushButton { background-color:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(0, 103, 254, 255), stop:1 rgba(0, 125, 255, 255)); color:rgb(240, 240, 240); border-style: outset; border-width: 2px; border-radius: 16px; border-color: rgba(0,0,0,0); font: bold 22px; padding: 6px; } QPushButton::pressed { background-color:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(0, 113, 254, 255), stop:1 rgba(0, 135, 255, 255)); border-style: inset } QPushButton::disabled { background-color:rgb(185, 205, 255) }"
LINE_EDIT_STYLE_SHEET = "border-style: outset; border-width: 1px; border-radius: 8px; border-color: rgb(122,122,122)"

class chooseModelWindow(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		layout = QtWidgets.QVBoxLayout()
		self.buttonBox = QtWidgets.QHBoxLayout()

		self.newModelButton = QtWidgets.QPushButton("Create New Model")
		self.newModelButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.buttonBox.addWidget(self.newModelButton)
		self.newModelButton.clicked.connect(self.createNewModel)

		self.oldModelButton = QtWidgets.QPushButton("Use Existing Model")
		self.oldModelButton.clicked.connect(self.useOldModel)
		self.oldModelButton.setStyleSheet(BUTTON_STYLE_SHEET)
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
		self.topLabel = QtWidgets.QLabel("Generate model below a certain percentage of errors or generate model better than an existing model?")
		self.certainErrorsButton = QtWidgets.QPushButton("<= % Errors")
		self.certainErrorsButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.certainErrorsButton.clicked.connect(self.certainErrorsButtonPressed)

		self.betterThanCurrentButton = QtWidgets.QPushButton("Better Than Existing Model")
		self.betterThanCurrentButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.betterThanCurrentButton.clicked.connect(self.betterThanCurrentButtonPressed)

		self.trainAgainstSolvedCSVsButton = QtWidgets.QPushButton("Train with Solved CSVs")
		self.trainAgainstSolvedCSVsButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.trainAgainstSolvedCSVsButton.clicked.connect(self.trainAgainstSolvedCSVButtonPressed)
		self.trainCount = 0

		self.layout.addWidget(self.topLabel)
		self.buttonRow.addWidget(self.certainErrorsButton)
		self.buttonRow.addWidget(self.betterThanCurrentButton)
		self.buttonRow.addWidget(self.trainAgainstSolvedCSVsButton)
		self.layout.addLayout(self.buttonRow)
		
		self.setLayout(self.layout)

	def certainErrorsButtonPressed(self):
		newLayout = QtWidgets.QHBoxLayout()
		self.numberOfErrorsLabel = QtWidgets.QLabel("Number of errors to beat:")
		self.numberOfErrorsInput = QtWidgets.QLineEdit()
		self.numberOfErrorsInput.setStyleSheet(LINE_EDIT_STYLE_SHEET)
		self.generateButton = QtWidgets.QPushButton("Generate")
		self.generateButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.generateButton.clicked.connect(self.generateButtonPressed)
		newLayout.addWidget(self.numberOfErrorsLabel)
		newLayout.addWidget(self.numberOfErrorsInput)
		newLayout.addWidget(self.generateButton)

		self.layout.addLayout(newLayout)

	def generateButtonPressed(self):
		self.goal = int(self.numberOfErrorsInput.text())
		self.autoCreateModel()

	def betterThanCurrentButtonPressed(self):
		fileExtraction.setModelName(filedialog.askopenfilename().split(".")[0])
		self.goal = fileExtraction.testOnSolvedCSV() - 1
		self.autoCreateModel()

	def trainAgainstSolvedCSVButtonPressed(self):
		fakeframe = pd.read_csv("SREOs/CSVs/usethisone.csv")
		print(fakeframe.to_string())
		print(fakeframe)
		fileExtraction.trainAgainstSolvedCSV(True, "Model/trainingWithSolved")
		for i in range(100):
			fileExtraction.trainAgainstSolvedCSV(False, "Model/trainingWithSolved")

	def autoCreateModel(self):
		trainingData = pd.DataFrame(columns=['label','text'])
		count = 1
		errors = sys.maxsize
		while errors > self.goal:
			print("----------------------------------------------------------------------------------")
			trainingData = pd.DataFrame(columns=['label','text'])
			numReps = random.randint(35, 55) * 100
			LR = float(random.randint(35,50)) / 10.0
			print("Number of Repeats: " + str(numReps) + " Learning Rate: " + str(LR))
			modelName = "newTrial" + str(count) + "-" + str(numReps)
			fileExtraction.setModelName(modelName)
			trainingData = pd.concat([trainingData, generateData(numReps)],ignore_index=True)
			trainingData.to_csv("trainingData.csv",index=False)
			trainModel.trainModel(True,True,modelName,"trainingData.csv", LR)
			count += 1
			errors = fileExtraction.testOnSolvedCSV(self.goal)
			if errors > self.goal:
				os.remove(modelName + ".pt")
				os.remove(modelName + "Vocab.pt")
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
		self.input.setStyleSheet(LINE_EDIT_STYLE_SHEET)
		self.createButton = QtWidgets.QPushButton("Create")
		self.createButton.setStyleSheet(BUTTON_STYLE_SHEET)
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
		self.extractTab.maximize_window.connect(self.showMaximized)
		
		layout.addWidget(self.tabs)

class trainTabUI(QtWidgets.QWidget):
	switch_window = QtCore.pyqtSignal()

	def changeToGenerateDataWindow(self):
		self.switch_window.emit()

	def __init__(self):
		super().__init__()
		self.layout = QtWidgets.QVBoxLayout()
		self.trainText = QtWidgets.QLabel("Train Column Classification or Header Classification Model?")
		self.trainText.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
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
		self.newDatasetButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.oldDatasetButton = QtWidgets.QPushButton("Use Existing Dataset")
		self.buttonRow.addWidget(self.oldDatasetButton)
		self.oldDatasetButton.clicked.connect(self.oldDatasetButtonPressed)
		self.oldDatasetButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.createBetterModelButton = QtWidgets.QPushButton("Auto-Generate Model")
		self.createBetterModelButton.clicked.connect(self.createBetterModelButtonPressed)
		self.createBetterModelButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.buttonRow.addWidget(self.createBetterModelButton)

		self.trainModelButton = QtWidgets.QPushButton("Train Model")
		self.trainModelButton.setStyleSheet(BUTTON_STYLE_SHEET)

		self.layout.addWidget(self.trainText)
		self.layout.addLayout(self.checkRow)
		self.layout.addLayout(self.buttonRow)

		self.setLayout(self.layout)

	def createBetterModelButtonPressed(self):
		self.betterModelPopup = createBetterModelPopup()
		self.betterModelPopup.show()

	def oldDatasetButtonPressed(self):
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
	def __init__(self):
		super().__init__()
		self.models = None
		self.layout = QtWidgets.QVBoxLayout()
		self.chooseFilesRow = QtWidgets.QHBoxLayout()
		self.topRow = QtWidgets.QHBoxLayout()

		self.chooseModelButton = QtWidgets.QPushButton("Choose Model(s)")
		self.chooseModelButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.chooseModelButton.clicked.connect(self.chooseModelButtonPressed)
		self.topRow.addWidget(self.chooseModelButton)
		self.modelLabel = QtWidgets.QLabel("No Model Chosen")
		self.topRow.addWidget(self.modelLabel)

		self.invalidFileTypeLabel = QtWidgets.QLabel("Invalid File Type: ")
		self.invalidFileTypeLabel.hide()

		self.testSREOs = QtWidgets.QLabel("Test SREOs")

		self.singleFileButton = QtWidgets.QPushButton("Choose Individual File(s)")
		self.singleFileButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.singleFileButton.clicked.connect(self.useSelectedFiles)
		self.chooseFilesRow.addWidget(self.singleFileButton)
		self.singleFileButton.setDisabled(True)

		self.allFilesButton = QtWidgets.QPushButton("Test All Files")
		self.allFilesButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.chooseFilesRow.addWidget(self.allFilesButton)
		self.allFilesButton.setDisabled(True)
		self.allFilesButton.clicked.connect(self.useAllFiles)

		self.testOnSolvedCSVButton = QtWidgets.QPushButton("Test on Solved CSVs")
		self.testOnSolvedCSVButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.chooseFilesRow.addWidget(self.testOnSolvedCSVButton)
		self.testOnSolvedCSVButton.setDisabled(True)
		self.testOnSolvedCSVButton.clicked.connect(self.testOnSolvedCSV)

		self.layout.addLayout(self.topRow)
		self.layout.addWidget(self.testSREOs)
		self.layout.addLayout(self.chooseFilesRow)
		self.layout.addWidget(self.invalidFileTypeLabel)

		self.setLayout(self.layout)

	def chooseModelButtonPressed(self):
		fileName = filedialog.askopenfilenames()
		if(len(fileName) == 0):
			self.invalidFileTypeLabel.setText("Invalid File Type: " + fileName.split("/")[len(fileName.split("/")) - 1])
			self.invalidFileTypeLabel.show()
			return
		elif(len(fileName) == 1):
			fileName = fileName[0]
			if(fileName.split(".")[len(fileName.split(".")) - 1] != "pt"):
				self.invalidFileTypeLabel.setText("Invalid File Type: " + fileName.split("/")[len(fileName.split("/")) - 1])
				self.invalidFileTypeLabel.show()
				return
			else: 
				fileName = fileName.split(".")[0]
				modelName = fileName.split("/")[len(fileName.split("/")) - 1].split(".")[0]
				self.modelLabel.setText(modelName + " Selected")
		else:
			fileName = list(fileName)
			for i in range(len(fileName)):
				fileName[i] = fileName[i].split(".")[0]
			self.modelLabel.setText("Multiple Models Selected")
		self.invalidFileTypeLabel.hide()
		fileExtraction.setModelName(fileName)
		self.models = fileName
		self.singleFileButton.setDisabled(False)
		self.allFilesButton.setDisabled(False)
		self.testOnSolvedCSVButton.setDisabled(False)

	def useAllFiles(self):
		#showConsole()
		os.chdir(os.path.dirname(os.path.abspath(__file__)))
		for fileName in os.listdir("SREOs/CSVs/"):
			print(fileName)
			print('------------------------------------------------------------')
			data = fileExtraction.extractSREO("SREOs/CSVs/" + fileName)
			print(data.to_string())
			fileExtraction.testConfidence(True, data)
			print('------------------------------------------------------------')
	
	def useSelectedFiles(self):
		fileName = filedialog.askopenfilenames()
		if type(fileName) is tuple:
			for file in fileName:
				print(file)
				fileType = file.split(".")[len(file.split(".")) - 1]
				if(fileType == "csv" or fileType == "pdf" or fileType == "xlsx"):
					self.invalidFileTypeLabel.hide()
					data = fileExtraction.extractSREO(file)
					fileExtraction.testConfidence(True, data)
					print()
				else:
					self.invalidFileTypeLabel.setText("Invalid File Type: " + file)
					self.invalidFileTypeLabel.show()
		else:
			fileType = fileName.split(".")[len(fileName.split(".")) - 1]
			if(fileType == "csv" or fileType == "pdf" or fileType == "xlsx"):
				data = fileExtraction.extractSREO(fileName)
				print(data.columns)
				print()
				fileExtraction.testConfidence(True, data)
			else:
				self.invalidFileTypeLabel.setText("Invalid File Type: " + fileName.split("/")[len(fileName.split("/")) - 1])
				self.invalidFileTypeLabel.show()

	def testOnSolvedCSV(self):
		if type(self.models) is str:
			fileExtraction.testOnSolvedCSV()
		else:
			fileExtraction.testOnSolvedCSVMultiModel(len(self.models), self.models)

class extractTabUI(QtWidgets.QWidget):
	maximize_window = QtCore.pyqtSignal()

	def __init__(self):
		super().__init__()
		self.layout = QtWidgets.QVBoxLayout()
		self.mainColumns = QtWidgets.QHBoxLayout()
		self.leftColumn = QtWidgets.QVBoxLayout()
		self.rightColumn = QtWidgets.QVBoxLayout()
		self.backNextButtonsRow = QtWidgets.QHBoxLayout()

		self.invalidFileTypeLabel = QtWidgets.QLabel("Invalid File Type")
		self.invalidFileTypeLabel.hide()
		self.table = QtWidgets.QTableWidget()
		self.chooseModelButton = QtWidgets.QPushButton("Choose Model")
		self.chooseModelButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.chooseFileButton = QtWidgets.QPushButton("Choose File(s)")
		self.chooseFileButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.chooseFileButton.clicked.connect(self.validateFiles)

		self.layout.addWidget(self.invalidFileTypeLabel)
		self.layout.addLayout(self.mainColumns)
		self.mainColumns.addLayout(self.leftColumn)
		self.mainColumns.addLayout(self.rightColumn)
		self.rightColumn.addWidget(self.table)
		self.rightColumn.addLayout(self.backNextButtonsRow)
		self.leftColumn.addWidget(self.chooseFileButton)
		self.highlightRowsLabelVisible = False
		
		self.setLayout(self.layout)

	def validateFiles(self):
		self.files = filedialog.askopenfilenames()
		if len(self.files) == 0:
			return
		allValid = True
		for fileName in self.files:
			fileType = fileName.split(".")[len(fileName.split(".")) - 1]
			if(fileType == "csv" or fileType == "pdf" or fileType == "xlsx" or fileType == "xls"):
				self.invalidFileTypeLabel.hide()
				print()
			else:
				self.invalidFileTypeLabel.setText("Invalid File Type: " + fileName)
				self.invalidFileTypeLabel.show()
				allValid = False
		if allValid:
			self.fileIndex = 0
			self.extractFile()

	def extractFile(self):
		self.fileName = self.files[self.fileIndex]
		self.dataframe = fileExtraction.extractSREO(self.fileName)
		print(self.dataframe)
		self.table.setColumnCount(len(self.dataframe.columns))
		self.table.setRowCount(len(self.dataframe.index))
		
		for i, row in self.dataframe.iterrows():
			j = 0
			for columnName, cell in row.items():
				if str(cell) == "nan": cell = ""
				item = QtWidgets.QTableWidgetItem(str(cell))
				columnNameItem = QtWidgets.QTableWidgetItem(str(columnName))
				self.table.setItem(0,j,columnNameItem)
				self.table.setItem(i+1,j,item)
				j += 1
		if not self.highlightRowsLabelVisible:
			self.highlightRowsLabelVisible = True
			self.highlightRowsLabel = QtWidgets.QLabel("Highlight any rows which are not the first row of column titles or a property and click delete to remove")
			self.deleteButton = QtWidgets.QPushButton("Delete Row")
			self.deleteButton.setStyleSheet(BUTTON_STYLE_SHEET)
			self.deleteButton.clicked.connect(self.deleteRows)
			self.extractButton = QtWidgets.QPushButton("Extract")
			self.extractButton.setStyleSheet(BUTTON_STYLE_SHEET)
			self.extractButton.clicked.connect(self.extractRows)
			self.topRow = QtWidgets.QHBoxLayout()
			self.topRow.addWidget(self.highlightRowsLabel)
			self.topRow.addWidget(self.deleteButton)
			self.topRow.addWidget(self.extractButton)
			self.backButton = QtWidgets.QPushButton("Back")
			self.backButton.setStyleSheet(BUTTON_STYLE_SHEET)
			self.backButton.clicked.connect(self.backButtonPressed)
			self.backNextButtonsRow.addWidget(self.backButton)
			self.nextButton = QtWidgets.QPushButton("Next File")
			self.nextButton.setStyleSheet(BUTTON_STYLE_SHEET)
			self.nextButton.clicked.connect(self.nextButtonPressed)
			self.backNextButtonsRow.addWidget(self.nextButton)
			self.layout.insertLayout(0,self.topRow)
			self.maximize_window.emit()

	def nextButtonPressed(self):
		if self.fileIndex < len(self.files) - 1:
			self.fileIndex += 1
			self.extractFile()
	def backButtonPressed(self):
		if self.fileIndex > 0:
			self.fileIndex -= 1
			self.extractFile()
	def deleteRows(self):
		rowsRemoved = 0
		for selectedRows in self.table.selectedRanges():
			topRowIndex = selectedRows.topRow()
			numRows = selectedRows.rowCount()
			for row in range(numRows):
				self.table.removeRow(topRowIndex + row - rowsRemoved)
				rowsRemoved += 1

	def extractRows(self):
		numRows = self.table.rowCount()
		numColumns = self.table.columnCount()
		self.dataForExtraction = pd.DataFrame()
		for columnIndex in range(numColumns):
			for rowIndex in range(1,numRows):
				item = self.table.item(rowIndex, columnIndex).text()
				self.dataForExtraction.at[rowIndex - 1,self.table.item(0,columnIndex).text()] = item
		fileExtraction.setModelName("Model/currentBest")
		newFileName = self.fileName.split("/")[len(self.fileName.split("/")) - 1].split(".")[0]
		sreoTemplate = fileExtraction.fillTemplate(self.dataForExtraction)
		fileTypes = [("Excel File", "*.xlsx"), ("CSV File", "*.csv")]
		saveLocation = filedialog.asksaveasfile(initialfile = "Standardized-" + newFileName,filetypes = fileTypes, defaultextension = fileTypes)
		if saveLocation is None:
			return ""
		sreoTemplate.to_excel(saveLocation.name, index=False)
		if saveLocation.name != "":
			self.highlightRowsLabel.setText("Extracted data saved to " + saveLocation.name)
			
class generateDataWindow(QtWidgets.QWidget):
	switch_window = QtCore.pyqtSignal()
	def changeToTrainTestWindow(self):
		self.switch_window.emit()

	def __init__(self):
		super().__init__()

		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.verticalLayout.setContentsMargins(15, 15, 15, 15)
		self.topBar = QtWidgets.QHBoxLayout()

		self.textInputRow = QtWidgets.QHBoxLayout()
		self.buttonRow = QtWidgets.QHBoxLayout()

		self.bottomRows = QtWidgets.QVBoxLayout()

		#-------------------------------Labels---------------------------------------
		self.generateNewDataLabel = QtWidgets.QLabel("Generate New Data for Training")
		self.generateNewDataLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		self.topBar.addWidget(self.generateNewDataLabel)

		self.numberOfDataPointsLabel = QtWidgets.QLabel("Total # of data points created: ")
		self.textInputRow.addWidget(self.numberOfDataPointsLabel)

		#-------------------------------Buttons---------------------------------------
		self.generateDataButton = QtWidgets.QPushButton("Generate Data")
		self.generateDataButton.setStyleSheet(BUTTON_STYLE_SHEET)

		self.generateDataButton.clicked.connect(self.generateDataButtonPressed)
		self.generateDataButton.setDisabled(True)

		self.cancelButton = QtWidgets.QPushButton("Cancel")
		self.cancelButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.cancelButton.clicked.connect(self.changeToTrainTestWindow)

		self.doneButton = QtWidgets.QPushButton("Done")
		self.doneButton.setStyleSheet(BUTTON_STYLE_SHEET)
		self.doneButton.clicked.connect(self.train)
		#-------------------------------Misc---------------------------------------
		self.numRepeatsInput = QtWidgets.QLineEdit()
		self.numRepeatsInput.setStyleSheet(LINE_EDIT_STYLE_SHEET)
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
		self.bottomRows.addLayout(self.textInputRow)
		self.bottomRows.addWidget(self.progressBar)
		self.buttonRow.addWidget(self.cancelButton)
		self.buttonRow.addWidget(self.doneButton)
		self.bottomRows.addLayout(self.buttonRow)
		self.verticalLayout.addLayout(self.bottomRows)
		self.setLayout(self.verticalLayout)

	def train(self):
		self.chooseModelPopup = chooseModelWindow()
		self.chooseModelPopup.show()
		#self.chooseModelPopup.switchWindow.connect(lambda:self.switch_window.emit())

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
		if trainColumn:
			fileName = "trainingData.csv"
		else:
			fileName = "trainingHeaderData.csv"
		trainingData = pd.DataFrame(columns=['label','text'])
		total = 0
		for i in range(self.numRepeats):
			if trainColumn:
				trainingData = pd.concat([trainingData, generateData(1)],ignore_index=True)
			else:
				trainingData = pd.concat([trainingData, generateHeaderData(1)],ignore_index=True)
			total += 1
			if total % (self.numRepeats / 100) == 0:
				self.incrementProgressBar(1)
		trainingData.to_csv(fileName, index=False)
		self.doneButton.setDisabled(False)

class Controller:
	def __init__(self):
		self.trainTest = trainTestWindow()
		self.generateData = generateDataWindow()
		pass

	def showTrainTestWindow(self):
		self.trainTest.switch_window.connect(self.showGenerateDataWindow)
		self.generateData.close()
		self.trainTest.show()

	def showGenerateDataWindow(self):
		self.trainTest.close()
		self.generateData = generateDataWindow()
		self.generateData.show()
		self.generateData.switch_window.connect(self.showTrainTestWindow)

def showConsole():
	ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 4)

if __name__ == "__main__":
	import sys
	#fileExtraction.extractFromPDF("SREOs/James P. Knell - Certified RE Schedule 12.31.19.pdf")
	#ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
	app = QtWidgets.QApplication(sys.argv)
	controller = Controller()
	controller.showTrainTestWindow()
	sys.exit(app.exec_())
