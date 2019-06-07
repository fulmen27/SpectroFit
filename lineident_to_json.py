import os
import json
import csv

lineident = {"filename": "lineident.csv", "1st_col": [], "2nd_col": [], "3rd_col": [], "lambda": [], "element_name": [], }
if os.path.exists('lineident.csv'):
    with open(lineident["filename"], 'r') as f:
        lineident["lineident_file"] = csv.reader(f, delimiter=";")
        for row in lineident["lineident_file"]:
            lineident["1st_col"].append(float(row[0]))
            lineident["2nd_col"].append(float(row[1]))
            lineident["3rd_col"].append(float(row[2]))
            lineident["lambda"].append(float(row[3]) / 10)
            lineident["element_name"].append(row[4])

passed = []
to_write = dict()
for i in range(len(lineident["element_name"])):
    tmp = lineident["element_name"][i][0:2].replace(" ", "")
    if tmp in passed:
        to_write[tmp]['number'] += 1
        to_write[tmp][lineident["element_name"][i]+str(to_write[tmp]['number'])] = {}
        to_write[tmp][lineident["element_name"][i]+str(to_write[tmp]['number'])]["lambda"] = lineident["lambda"][i]
        to_write[tmp][lineident["element_name"][i]+str(to_write[tmp]['number'])]["1st_col"] = lineident["1st_col"][i]
        to_write[tmp][lineident["element_name"][i]+str(to_write[tmp]['number'])]["2nd_col"] = lineident["2nd_col"][i]
        to_write[tmp][lineident["element_name"][i]+str(to_write[tmp]['number'])]["3rd_col"] = lineident["3rd_col"][i]
    else:
        passed.append(tmp)
        to_write[tmp] = {'number': 1}
        to_write[tmp][lineident["element_name"][i]+str(to_write[tmp]['number'])] = {}
        to_write[tmp][lineident["element_name"][i]+str(to_write[tmp]['number'])]["lambda"] = lineident["lambda"][i]
        to_write[tmp][lineident["element_name"][i]+str(to_write[tmp]['number'])]["1st_col"] = lineident["1st_col"][i]
        to_write[tmp][lineident["element_name"][i]+str(to_write[tmp]['number'])]["2nd_col"] = lineident["2nd_col"][i]
        to_write[tmp][lineident["element_name"][i]+str(to_write[tmp]['number'])]["3rd_col"] = lineident["3rd_col"][i]

with open('lineident.json', 'w') as f:
    json.dump(to_write, f)
