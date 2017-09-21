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
        for name in client[str(user.get("_id"))].collection_names(include_system_collections=False):
            client[str(user.get("_id"))][name].delete_many({})
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
                data[firstRE[0][0]].append(eval(firstRE[0][1].replace("NULL", "' '")))
        for collection in tableNames:
            dbCol = db[collection.get("tableName")]
            colData = data.get(collection.get("tableName"))
            fields = collection.get("fields")
            for row in colData:
                oneData = collections.OrderedDict()
                for field in fields:
                    index = fields.index(field)
                    val = row[index]
                    oneData[str(index) + "-" + field.get("name")] = val
                dbCol.insert(oneData)
        return jsonify({"status": 1, "data": []})
