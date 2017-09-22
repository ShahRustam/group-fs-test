import time

print str(time.time())

import sqlparse
import re
import collections
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test_database

#file = open('groupfs_new_20170922.sql')
file = open('mrjoke.sql')
file = file.read()

parses = sqlparse.parse(file)

tableNamesCreateRE = "TABLE '(\w*)' (\(.*\))"
tableNamesInsertRE = "INTO '(\w*)' VALUES (\(.*\))"
fieldsNamesRE = "'(\w*)' ([\w\(\),]*)"

fieldInFieldsRe = "\((.*)\)"

tableNames = []
data = {}


def replaceType(x):
    x = re.sub("['],[']", '""","""', x)
    x = re.sub("([^'\s]),[']", r'\1,"""', x)
    x = re.sub("['],([^'\s])", r'""",\1', x)
    x = re.sub("[\(](['])", '("""', x)
    x = re.sub("(['])[\)]", '""")', x)
    if x[-2:]=="))":
        x = x[:-1]
    return x


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
        if firstRE[0][1].count("(") > 1:
            array = firstRE[0][1].split("),(")
            for index, row in enumerate(array):
                if index == 0:
                    data[firstRE[0][0]].append(eval(
                        replaceType(row + ")").replace("NULL", '""" """').strip()
                    ))
                elif index == (len(array) - 1):
                    data[firstRE[0][0]].append(eval(
                        replaceType("(" + row).replace("NULL", '""" """').strip()
                    ))
                else:
                    # print "START:" + "(" + row + ")" + ":STOP"
                    data[firstRE[0][0]].append(
                        eval(
                            replaceType("(" + row + ")").replace("NULL", '""" """').strip()
                        ))
        else:
            data[firstRE[0][0]].append(eval(replaceType(firstRE[0][1]).replace("NULL", '""" """').strip()))

# print data.get("wp_posts")[:5]
print "______________________"

for collection in tableNames:
    dbCol = db[collection.get("tableName")]
    colData = data.get(collection.get("tableName"))
    fields = collection.get("fields")
    if colData:
        for row in colData:
            oneData = collections.OrderedDict()
            for field in fields:
                index = fields.index(field)
                val = row[index]
                try:
                    oneData[str(index) + "-" + field.get("name")] = int(val)
                except:
                    try:
                        oneData[str(index) + "-" + field.get("name")] = float(val)
                    except:
                        oneData[str(index) + "-" + field.get("name")] = val
            dbCol.insert(oneData)
#
print str(time.time())
