# -*- coding: utf-8 -*-

from app.config import *
from app.utils.error import *
from app.utils.utils import *
from app.controller.login import loginRequired


class UploadSQL(MethodView):
    @loginRequired
    def post(self):
        if 'file' not in request.files:
            return sendError(ErrorResponse.makeCustomError("not_found_file_filed", "Please, add file field"))
        file = request.files['file']
        user = currentUser()
        parses = sqlparse.parse(file.read())
        tableNamesCreateRE = "TABLE '(\w*)' (\(.*\))"
        tableNamesInsertRE = "INTO '(\w*)' VALUES (\(.*\))"
        fieldsNamesRE = "'(\w*)' ([\w\(\),]*)"
        tableNames = []
        data = {}
        client.drop_database(str(user.get("_id")))
        # for name in client[].collection_names(include_system_collections=False):
        #     client[str(user.get("_id"))][name].delete_many({})
        db = client[str(user.get("_id"))]
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
                                self.replaceType(row + ")").replace("NULL", '""" """').strip()
                            ))
                        elif index == (len(array) - 1):
                            data[firstRE[0][0]].append(eval(
                                self.replaceType("(" + row).replace("NULL", '""" """').strip()
                            ))
                        else:
                            # print "START:" + "(" + row + ")" + ":STOP"
                            data[firstRE[0][0]].append(
                                eval(
                                    self.replaceType("(" + row + ")").replace("NULL", '""" """').strip()
                                ))
                else:
                    data[firstRE[0][0]].append(eval(self.replaceType(firstRE[0][1]).replace("NULL", '""" """').strip()))
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
        return jsonify({"status": 1, "data": []})

    def replaceType(self,x):
        x = re.sub("['],[']", '""","""', x)
        x = re.sub("([^'\s]),[']", r'\1,"""', x)
        x = re.sub("['],([^'\s])", r'""",\1', x)
        x = re.sub("[\(](['])", '("""', x)
        x = re.sub("(['])[\)]", '""")', x)
        if x[-2:] == "))":
            x = x[:-1]
        return x
