import os, sys
from parse_rest.connection import register, ParseBatcher
from parse_rest.datatypes import Object

from pprint import pprint

from urllib.request import urlopen
import ast
import requests
import pickle
import json

import numpy as np


application_id = "uxliXmbidhv6n7zhKAP2BG6mVJiFdpNkms4zaVMw"
rest_api_key = "SF5ZKAFt44znr3vPBqfYMcYLeioegKDsjStvHfFz"

register(application_id, rest_api_key)

first_object = Object()
class Customers(Object):
    pass

dictOfAllData = {}

allCustomers = []


apiKey = '?key=035b228cdff67a14e8f13f1864a8956b'

baseNessieURL = 'http://api.reimaginebanking.com/'
apiType = 'enterprise/'

numberOfCustomers = 0

listOfObjects = pickle.load( open( "allObjects.p", "rb" ) )

listOfCustomerIDs = []
for customer in listOfObjects:
	allCustomers.append(customer)
	customerID = customer['accountID']
	listOfCustomerIDs.append(customerID)
	dictOfFields = customer

	dictOfAllData[customerID] = dictOfFields

	# print(thisDict)
	numberOfCustomers += 1
	# print(numberOfCustomers)


allFields = list(dictOfFields.keys())
allFields.remove('updatedAt')

allFields.remove('objectId')

allFields.remove('createdAt')






apiKey = '?key=035b228cdff67a14e8f13f1864a8956b'

#'http://api.reimaginebanking.com/enterprise/customers?key=1ce2aee36e28857cc1e8c6f7a1992759'
baseNessieURL = 'http://api.reimaginebanking.com/'
apiType = 'enterprise/'
field = 'customers'

urlToQuery = baseNessieURL + apiType + field + apiKey

#print('curl -X GET --header "Accept: application/json"' + ' "' + urlToQuery + '"')

jsonObj = os.system('curl -X GET --header "Accept: application/json"' + ' "' + urlToQuery + '" > test.json')

jsonFile = open('test.json', 'r')



with open('test.json') as data_file:    
    listOfAllCustomerDicts = dict(json.load(data_file))['results']
#pickle.dump( listOfAllCustomerDicts, open( "listOfAllCustomerDicts.p", "wb" ) )

urlToQuery = baseNessieURL + apiType + 'bills' + apiKey
jsonObj = os.system('curl -X GET --header "Accept: application/json"' + ' "' + urlToQuery + '" > test.json')
jsonFile = open('test.json', 'r')



with open('test.json') as data_file:    
    listOfAllBills = dict(json.load(data_file))['results']


urlToQuery = baseNessieURL + apiType + 'accounts' + apiKey
jsonObj = os.system('curl -X GET --header "Accept: application/json"' + ' "' + urlToQuery + '" > test.json')
jsonFile = open('test.json', 'r')



with open('test.json') as data_file:    
    listOfAllAccounts = dict(json.load(data_file))['results']

#O(n^3) b/c it's a hackathon
numberOfCustomers = 0
numberThatDidntWork = 0
for customer in listOfAllCustomerDicts: #Get all customers
	numberOfCustomers += 1
	customerID = customer["_id"]
	if customerID not in listOfCustomerIDs:
		numberThatDidntWork += 1
		continue
	dictOfAllData[customerID].update(customer)
	dictOfAllData[customerID]['listOfAccounts'] = []


	for account in listOfAllAccounts:  #Map accounts to customers
		if account["customer_id"] == customerID:
			account['listOfBills'] = []
			for bill in listOfAllBills: #Map bills to accounts
				if bill["account_id"] == account["_id"]:
					account['listOfBills'].append(bill)


			dictOfAllData[customerID]['listOfAccounts'].append(account)




	# print(numberOfCustomers)

# pprint(dictOfAllData)
# print(numberThatDidntWork)
# pprint(allFields)



listOfAllCustomerIDs = list(dictOfAllData.keys())
listOfAllCustomerDicts = [dictOfAllData[customerID] for customerID in listOfAllCustomerIDs ]

matrixOfData = []
castTheseToInt = ['age', 'degree', 'gender', 'incomeClass', 'married', 'professional']
castTheseToFloat = ['averageTimeToPayBill']

matrixOfData = [[customer["accountID"], int(customer['age']), float(customer['averageTimeToPayBill']), int(customer['degree']), int(customer['gender']), int(customer['incomeClass']), int(customer['married']), int(customer['professional']), customer["card_type"] , customer["most_common_transaction_type"] , customer["has_a_house"], customer["credit_type"]] for customer in listOfAllCustomerDicts]
# pprint(matrixOfData)
numRows = len(matrixOfData)
numCols =  len(matrixOfData[0])

# print(matrixOfData[0])

# print(numRows)
# print(numCols)

dependentVariableDict = {}

for row in matrixOfData:

	dependentVariableDict[row[0]] = {
	"card_type": row[numCols - 4],
		"most_common_transaction_type": row[numCols - 3],
	"has_a_house": row[numCols - 2],
	"credit_type": row[numCols - 1]

	}
	
npMatrixOfData = np.matrix(matrixOfData)
print(npMatrixOfData)
	
listOfIVs = sys.argv[1:]
print(listOfIVs)



ivMatrix = npMatrixOfData[:, listOfIVs]
print(ivMatrix)

from sklearn.cluster import KMeans

n_clusters= 5

cluster = KMeans(n_clusters=n_clusters)

cluster.fit(ivMatrix)
cluster_labels = cluster.labels_
cluster_cluster_centers = cluster.cluster_centers_
clusters_labels_unique = np.unique(cluster_labels)


from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X = pca.fit_transform(ivMatrix)
print(X)

final = []

for rowNumber in range(len(X)):
	x = X[rowNumber][0]
	y = X[rowNumber][1]
	classification = cluster_labels[rowNumber]
	final.append({"x": str(x), 'y': str(y), 'category': str(classification )})


jsonObj = json.dumps(final)
print(jsonObj)



# print(npMatrixOfData)
# print(ivMatrix)


