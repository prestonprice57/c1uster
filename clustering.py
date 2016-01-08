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

from geopy.geocoders import Nominatim

print("Python running")
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

pickle.dump( dictOfAllData, open( "dictFile.p", "wb" ) )

listOfAllCustomerIDs = list(dictOfAllData.keys())
listOfAllCustomerDicts = [dictOfAllData[customerID] for customerID in listOfAllCustomerIDs ]

matrixOfData = []
castTheseToInt = ['age', 'degree', 'gender', 'incomeClass', 'married', 'professional']
castTheseToFloat = ['averageTimeToPayBill']

matrixOfData = [[customer["accountID"], int(customer['age']), float(customer['averageTimeToPayBill']), int(customer['degree']), int(customer['gender']), int(customer['incomeClass']), int(customer['married']), int(customer['professional']), customer["card_type"] , customer["most_common_transaction_type"] , customer["has_a_house"], customer["credit_type"]] for customer in listOfAllCustomerDicts]
# pprint(matrixOfData)
numRows = len(matrixOfData)
numCols =  len(matrixOfData[0])

listOfPossibleIVs = ['accountID', 'age', 'averageTimeToPayBill', 'degree', 'gender', 'incomeClass', 'married', 'professional']

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
# print(npMatrixOfData)
	
listOfIVs = sys.argv[3:]
# print(listOfIVs)

dvTypeNumber = sys.argv[2]

classifyOnly = sys.argv[1]


ivMatrix = npMatrixOfData[:, listOfIVs]
# print(ivMatrix)

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
# print(X)

final = []

geolocator = Nominatim()



for rowNumber in range(len(X)):
	x = round(X[rowNumber][0], 2)
	y = round(X[rowNumber][1], 2)
	classification = cluster_labels[rowNumber]
	customerID = matrixOfData[rowNumber][0]
	print(dictOfAllData[customerID]['address'])
	try:
		zipCode = dictOfAllData[customerID]['address']['zip']
	except:
		continue
	#print( zipCode)
	# location = geolocator.geocode(zipCode)

	final.append({"x": str(x), 'y': str(y), 'category': str(classification ), 'zip': zipCode})


coordinatesJSON = json.dumps(final)
with open("coordinates.json", 'w') as outfile:
    json.dump(final, outfile)
# json.dump(final, "coordinates.json")
print(coordinatesJSON)

dvOptions = []


if int(dvTypeNumber) == 3:
	dvOptions = ["Venture", "QuickSilver", "Journey", "Spark", "Platinum"]

elif int(dvTypeNumber) == 2:
	dvOptions = ["Food", "Entertainment", "Utilities", "Housing", "Education"]

elif int(dvTypeNumber) == 1:
	dvOptions = ["Has a House", "Does not have a House"]

else:
	dvOptions = ['1','2','3','4','5'] #higher = better



realDVDict = {'0': {},
			'1': {},
			'2': {},
			'3': {},
			'4': {}}

for classNumber in range(5):
	for dyType in dvOptions:
		realDVDict[str(classNumber)][dyType] = 0

for rowNumber in range(len(matrixOfData)):
	classification = cluster_labels[rowNumber]

	dvClass = matrixOfData[rowNumber][numCols - int(dvTypeNumber) - 1]
	realDVDict[str(classification)][dvClass] += 1



classTotals = []
for classNumber in range(5):
	totalNumberForThisClass = 0
	for dyType in dvOptions:
		totalNumberForThisClass += realDVDict[str(classNumber)][dyType]

	classTotals.append(totalNumberForThisClass)

	for dyType in dvOptions:
		realDVDict[str(classNumber)][dyType] = str(round(realDVDict[str(classNumber)][dyType] / totalNumberForThisClass * 100, 2))

dvJSON = json.dumps(realDVDict)
with open("dv.json", 'w') as outfile:
    json.dump(realDVDict, outfile)
# json.dump(realDVDict, "dv.json")
print(dvJSON)



avgValuesForEachFeatureInEachCluster = {'0': {},
			'1': {},
			'2': {},
			'3': {},
			'4': {}}


ivsUsed = []


for iv in listOfIVs:
	ivsUsed.append(listOfPossibleIVs[int(iv)])

for classNumber in range(5):
	for ivString in ivsUsed:
		avgValuesForEachFeatureInEachCluster[str(classNumber)][ivString] = 0



for rowNumber in range(len(matrixOfData)):
	classification = cluster_labels[rowNumber]


	for ivIndex in range(len(listOfIVs)):
		ivNumber = int(listOfIVs[ivIndex])
		ivString = ivsUsed[ivIndex]
		avgValuesForEachFeatureInEachCluster[str(classification)][ivString] += matrixOfData[rowNumber][ivNumber]


for classNumber in range(5):
	totalNumberForThisClass = 0

	for ivString in ivsUsed:
		avgValuesForEachFeatureInEachCluster[str(classNumber)][ivString] = str(round(avgValuesForEachFeatureInEachCluster[str(classNumber)][ivString] / classTotals[classNumber],2 ))

avgValueJSON = json.dumps(avgValuesForEachFeatureInEachCluster)
with open("avgValue.json", 'w') as outfile:
    json.dump(avgValuesForEachFeatureInEachCluster, outfile)
# json.dump(avgValuesForEachFeatureInEachCluster, "avgValue.json")

#print(avgValueJSON)
# pprint(avgValuesForEachFeatureInEachCluster)


# print(npMatrixOfData)
# print(ivMatrix)


