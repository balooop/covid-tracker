import sys
import logging
import pymysql
import json
import pymongo
import re

#rds settings
rds_host  = 'covid-tracker.c7ic0rieoltc.us-east-1.rds.amazonaws.com'
username = 'admin'
password = 'Cov1dgrap3'
db_name = 'covid-locations-tracker'
conn = pymysql.connect(rds_host, user=username, passwd=password, db=db_name, connect_timeout=5)

client1 = pymongo.MongoClient("mongodb+srv://user:cs411project@cluster0.2xbcj.mongodb.net/?retryWrites=true&w=majority")
db1 = client1[ "Complaints" ]
col1 = db1[ "Complaints" ] 

# logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def handler(event, context):
    dict = {}
    visited = []
    cur = conn.cursor()
    # get number of cases, block id, and address visited for each address
    result_row = cur.execute("SELECT COUNT(*) AS numCasesPerAddr, block_id, address_visited FROM Cases GROUP BY address_visited")
    query_result = cur.fetchall()
    conn.commit()
    for row in query_result:
        numCases = row[0]
        blockId = row[1]
        addrVisited = row[2]
        visited.append(addrVisited)
        if blockId not in dict:
            dict[blockId] = [(numCases,addrVisited)]
        else:
            dict[blockId].append((numCases,addrVisited))
            
    print("NAV")
    violations = col1.find()
    print("GAY")
    for document in violations:
        print(document["Address"])
        if document["Address"] not in visited:
            # compute 'block_id'
            firstHalf = document["Address"].split(' ')[0]
            firstHalf = re.sub("[^0-9]", "", firstHalf)
            street_address = document["Address"].split(',')[0].split(' ')
            block_id = str((int(firstHalf)//100)*100) + ''.join(street_address[1:])
            if block_id not in dict:
                dict[block_id] = [(0, document["Address"])]
            else:
                dict[block_id].append((0, document["Address"]))
            
    
    type = {}
    options = {}
    plotarea = {}
    series = []
    finalJson = {}
    
    type['type'] = 'treemap'
    options['split-type'] = 'balanced'
    options['color-type'] = 'palette'
    options['palette'] = ["#1ab7ea", "#ff5700", "#cd201f", "#25D366", "#3aaf85", "#f1c40f", "#17968e", "#f7b362", "#F58F84", "#5B3256", "#317589", "#6B9362"]

    plotarea['margin'] = "0 0 35 0"
    
    
    finalJson.update(type)
    finalJson['options'] = options
    finalJson['plotarea'] = plotarea
    
    
    for key in dict:
        parent = {}
        sumChid = 0
        sumChildViol = 0
        children = []
        # loop through all values in a key (# cases by  address)
        for child in dict[key]:
            numViol = 0
            # find address in MongoDB
            curViol = col1.find({'Address': child[1]})
            if(curViol.count() > 0):
                for x in curViol:
                    numViol += x["mask"]
                    numViol += x["socialDistancing"]
                    numViol += x["sick"]
                    numViol += x["dirty"]
            childy = {}
            childy['text'] = str(child[0]) + " Cases at " + child[1].split(',')[0] + ", " + str(numViol) + " violations" 
            childy['value'] = child[0] + numViol
            children.append(childy)
            sumChid += child[0]
            sumChildViol += numViol
        parent['children'] = children
        parent['text'] = key + ' - ' + str(sumChid) + " Cases, " + str(sumChildViol) + " Violations"
        series.append(parent)

    finalJson['series'] = series
    r = finalJson
    r = json.dumps(r)
    loaded_r = json.loads(r)
    client1.close()
    return loaded_r
