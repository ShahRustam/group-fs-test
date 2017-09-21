import time

print str(time.time())

import sqlparse
import re
import collections
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test_database

file = open('mrjoke.sql')
file = file.read()

parses = sqlparse.parse(file)

tableNamesCreateRE = "TABLE '(\w*)' (\(.*\))"
tableNamesInsertRE = "INTO '(\w*)' VALUES (\(.*\))"
fieldsNamesRE = "'(\w*)' ([\w\(\),]*)"

tableNames = []
data = {}

for script in parses:
    if script.get_type() == "CREATE":
        string = re.sub(' +', ' ', str(script).replace('`', "'").replace("\n", " "))
        firstRE = re.findall(tableNamesCreateRE, string)
        fields = []
        for fieldStr in firstRE[0][1].split(', '):
            if "PRIMARY KEY" not in fieldStr and "KEY" not in fieldStr:
                secondRE = re.findall(fieldsNamesRE, fieldStr)[0]
                fields.append({"name": secondRE[0], "type": secondRE[1]})
        tableNames.append({"tableName": firstRE[0][0], "fields": fields})
    elif script.get_type() == "INSERT":
        string = str(script).replace('`', "'")
        firstRE = re.findall(tableNamesInsertRE, string)
        if data.get(firstRE[0][0]) is None:
            data[firstRE[0][0]] = []
        data[firstRE[0][0]].append(eval(firstRE[0][1].replace("NULL", "''")))

for collection in tableNames:
    if collection.get("tableName") == "joke_ratings":
        dbCol = db[collection.get("tableName")]
        colData = data.get(collection.get("tableName"))
        fields = collection.get("fields")
        #print fields
        for row in colData:
            oneData = collections.OrderedDict()
            for field in fields:
                index = fields.index(field)
                val = row[index]
                oneData[str(index)+"-"+field.get("name")] = val
            dbCol.insert(oneData)
        print str(dbCol.find_one())

print str(time.time())
