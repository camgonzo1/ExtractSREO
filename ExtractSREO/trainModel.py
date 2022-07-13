from collections import Counter
from tkinter.tix import COLUMN
import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import DataLoader
from torch import nn
import torch.nn.functional as F
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") #Defines whether the user is using CPU or GPU processing
tokenizer = get_tokenizer('basic_english') #Defines a inital tokenizer
emsize = 512
EPOCHS = 5
LR = 1 #The learning rate of the model
BATCH_SIZE = 32 #Number of data points in each batch
vocab = None
text_pipeline = None
label_pipeline = None
model = None
COLUMN_LABELS = {0: "N/A", 1: "Units", 2: "City", 3: "State", 4: "Address", 5: "Rate Type", 6: "Acquisition Date", 
				 7: "Maturity Date", 8: "Property Name", 9: "Square Feet", 10: "Occupancy", 11: "Loan Amount", 
				 12: "Debt Service", 13: "NOI", 14: "DSCR", 15: "Market Value", 16: "LTV", 17: "Amort Start Date", 
				 18: "Property Type", 19: "Current Balance", 20: "All-In Rate", 21: "Lender", 22: "Spread", 23: "Index"}
HEADER_LABELS = {0: "N/A", 1: "Invalid", 2: "Valid"}

# Gets Number of Labels
def getNumLabels():
	 return len(COLUMN_LABELS) - 1


# Converts labels to numeric values able to be processed by the model
def get_column_label(label):
	return list(COLUMN_LABELS.values()).index(label)

def get_header_label(label):
	if label == "Valid": return 2
	elif label == "Invalid": return 1
	else: return 0

# Receives an inputted batch and collates to label, text, and offsets tensors to be imported into a DataLoader object
def collate_batch(batch):
	label_list, text_list, offsets = [], [], [0]
	for(label, text) in batch:
		label_list.append(label_pipeline(label))
		processed_text = torch.tensor(text_pipeline(text), dtype=torch.int64)
		text_list.append(processed_text)
		offsets.append(processed_text.size(0))
	label_list = torch.tensor(label_list, dtype=torch.int64)
	offsets = torch.tensor(offsets[:-1]).cumsum(dim=0)
	text_list = torch.cat(text_list)
	return label_list.to(device), text_list.to(device), offsets.to(device)

# Tokenizes all of the text values in a dataset
def yield_tokens(data_iter):
	for _, text in data_iter:
		yield tokenizer(text)

#A Neural Network model with 5 linear layers
class TextClassificationModel(nn.Module):
	#Initializes the model
	def __init__(self, vocab_size, embed_dim, num_class):
		super().__init__()
		self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=True) #The model's embedding bag
		self.fc1 = nn.Linear(512, 256)
		self.fc2 = nn.Linear(256, 128)
		self.fc3 = nn.Linear(128, 64)
		self.fc4 = nn.Linear(64, 16)
		self.fc5 = nn.Linear(16, num_class)
		self.init_weights()

	#Assigns inital weights for the layers and embedding bag
	def init_weights(self):
		initrange = 0.5
		self.embedding.weight.data.uniform_(-initrange,initrange)
		self.fc1.weight.data.uniform_(-initrange,initrange)
		self.fc1.bias.data.zero_()
		self.fc2.weight.data.uniform_(-initrange,initrange)
		self.fc2.bias.data.zero_()
		self.fc3.weight.data.uniform_(-initrange,initrange)
		self.fc3.bias.data.zero_()
		self.fc4.weight.data.uniform_(-initrange,initrange)
		self.fc4.bias.data.zero_()
		self.fc5.weight.data.uniform_(-initrange,initrange)
		self.fc5.bias.data.zero_()

	#Applies the model to inputted text to achieve a result
	def forward(self, text, offsets):
		embedded = self.embedding(text, offsets)
		x = F.relu(self.fc1(embedded))
		x = F.relu(self.fc2(x))
		x = F.relu(self.fc3(x))
		x = F.relu(self.fc4(x))
		x = self.fc5(x)
		return x

#Trains the model given a dataloader, optimizer, and criterion
def train(dataloader, model, optimizer, criterion, epoch):
	model.train()
	total_acc, total_count = 0,0
	log_interval = 500
	start_time = time.time()
	for idx, (label, text, offsets) in enumerate(dataloader):
		optimizer.zero_grad()
		predicted_label = model(text, offsets)
		loss = criterion(predicted_label, label)
		loss.backward()
		torch.nn.utils.clip_grad_norm_(model.parameters(), 0.1)
		optimizer.step()
		total_acc += (predicted_label.argmax(1) == label).sum().item()
		total_count += label.size(0)
		if idx % log_interval == 0 and idx > 0:
			elapsed = time.time() - start_time
			print('| epoch {:3d} | {:5d}/{:5d} batches'
				'| accuracy {:8.3f}'.format(epoch, idx, len(dataloader),total_acc/total_count))
			total_acc, total_count = 0,0
			start_time = time.time()

#Evaluates the performance of the model against a given dataloader, optimizer, and criterion
def evaluate(dataloader, model, optimizer, criterion):
	model.eval()
	total_acc, total_count = 0,0
	with torch.no_grad():
		for idx, (label, text, offsets) in enumerate(dataloader):
			predicted_label = model(text, offsets)
			loss = criterion(predicted_label, label)
			total_acc += (predicted_label.argmax(1) == label).sum().item()
			total_count += label.size(0)
	return total_acc/total_count

#Function to quickly predict an inputted string of text
def predict(text, text_pipeline):
	with torch.no_grad():
		text = torch.tensor(text_pipeline(text))
		output = model(text, torch.tensor([0]))
		return output
	
def trainModel(trainColumn, createNewModel, modelName, trainingFilePath):
	if not createNewModel:
		loadModel(modelName)

	#Imports the .csv files used for training and testing
	trainingFile = pd.read_csv(trainingFilePath)
	trainingFile.dropna(axis = 0, how = 'any', inplace = True)
	if trainColumn:
		trainingFile['labelNum'] = trainingFile['label'].apply(get_column_label)
		
	else:
		trainingFile['labelNum'] = trainingFile['label'].apply(get_header_label)
	
	# For testing
	print('--------Training Data---------')
	print(trainingFile['label'].value_counts())
	#Splits the training dataset into training and validation sets
	train_text, valid_text, train_label, valid_label = train_test_split(trainingFile['text'].to_list(), trainingFile['labelNum'].to_list(), test_size = 0.2, stratify = trainingFile['labelNum'].to_list(), random_state=0)
	#Converts the data into a zipped list able to be read by the model
	train_data = list(zip(train_label, train_text))
	valid_data = list(zip(valid_label, valid_text))

	# For Testing
	print('Train data len: ' + str(len(train_text)))
	print('Class distribution ' + str(Counter(train_label)))
	print('Valid data len: ' + str(len(valid_text)))
	print('Class distribution ' + str(Counter(valid_label)))

	#Pipelines are lists of tokenized verions of either text or labels which get read by the model
	if createNewModel:
		global vocab
		global text_pipeline
		global label_pipeline
		global model
		vocab = build_vocab_from_iterator(yield_tokens(train_data), specials = ["<unk>"]) #Builds a vocab set from training data
		vocab.set_default_index(vocab["<unk>"])
		text_pipeline = lambda x: vocab(tokenizer(x))
		label_pipeline = lambda x: int(x)
		num_class = len(set([label for (label, text) in train_data])) + 1
		model = TextClassificationModel(len(vocab), emsize, num_class).to(device)

	
	#Creates model and defines criterion, optimizer, and scheduler parameters
	criterion = torch.nn.CrossEntropyLoss()
	optimizer = torch.optim.SGD(model.parameters(), lr = LR)
	scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 1.0, gamma=0.1)
	total_accu = None

	#Converts training, testing, and validation datasets to dataloaders
	train_iter = train_data
	valid_iter = valid_data
	train_dataloader = DataLoader(train_iter, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_batch)
	valid_dataloader = DataLoader(valid_iter, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_batch)

	#Trains the model EPOCHS number of times with given training set
	for epoch in range(1, EPOCHS + 1):
		epoch_start_time = time.time()
		train(train_dataloader, model, optimizer, criterion, epoch)
		accu_val = evaluate(valid_dataloader, model, optimizer, criterion)
		if total_accu is not None and total_accu > accu_val:
			scheduler.step()
		else:
			total_accu = accu_val
		# For Testing
		print('-' * 59)
		print('| end of epoch {:3d} | time: {:5.2f}s | ' 'valid accuracy {:8.3f} '.format(epoch, time.time() - epoch_start_time, accu_val))
		print('-' * 59)

	torch.save(model, modelName + ".pt")
	torch.save(vocab, modelName + "Vocab.pt")
	print("Saved to path: " + modelName + ".pt")

def loadModel(modelName):
	global model
	global vocab
	global text_pipeline
	global label_pipeline
	vocab = torch.load(modelName + "Vocab.pt")
	model = torch.load(modelName + ".pt")
	model.eval()
	text_pipeline = lambda x: vocab(tokenizer(x))
	label_pipeline = lambda x: int(x)

def outputConfidence(modelName, columnOrHeader, textInput, print):
	loadModel(modelName)
	#Set of numerical labels and their text values
	if columnOrHeader == 1:
		labels = COLUMN_LABELS
	else:
		labels = HEADER_LABELS
	output = predict(textInput, text_pipeline)
	probs = torch.nn.functional.softmax(output, dim=1).tolist()
	maxVal = 0
	maxIndex = -1
	for i in range(len(probs[0])):
		if maxVal < probs[0][i]:
			maxVal = probs[0][i]
			maxIndex = i
	if maxVal > .95:
		return labels[maxIndex], maxVal
	else: return "N/A", maxVal

	######################################################### Testing Below #########################################################
def testInput(modelName, columnOrHeader, testString, print):
	loadModel(modelName)
	#Set of numerical labels and their text values
	if columnOrHeader == 1:
		labels = COLUMN_LABELS
	else:
		labels = HEADER_LABELS
	output = predict(testString, text_pipeline)
	probs = torch.nn.functional.softmax(output, dim=1).tolist()
	#Some test text to see how well the model performs
	if(print == 1): 
		print("[N/A, Units, City, State, Address, Rate Type, Acquisition Date, Maturity Date, Property Name]")
		probsString = ""
		for i in range(len(probs[0])):
			probsString += labels[i] + " " + str(float(probs[0][i])) + " | "  
		print(probsString)
		print(testString + " is a %s" %labels[predict(testString, text_pipeline).argmax(1).item()])
	return labels[output.argmax(1).item()]