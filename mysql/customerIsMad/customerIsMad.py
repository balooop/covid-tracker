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
        street_address = addrVisited.split(',')[0].split(' ')
        processed_address = [street_address[0] + ' ' + ' '.join(filter(lambda x: ('#' not in x and 'suite' not in x.lower() and 'ste' not in x.lower()), street_address[1:]))] + addrVisited.split(',')[1:]
        processed_address = ','.join(processed_address)
        visited.append(processed_address)
        if blockId not in dict:
            dict[blockId] = [(numCases,processed_address)]
        else:
            dict[blockId].append((numCases,processed_address))
            
    violations = col1.find()
    for document in violations:
        firstHalf = document["Address"].split(' ')[0]
        firstHalf = re.sub("[^0-9]", "", firstHalf)
        street_address = document["Address"].split(',')[0].split(' ')
        block_id = str((int(firstHalf)//100)*100) + ''.join(filter(lambda x: ('#' not in x and 'suite' not in x.lower() and 'ste' not in x.lower()), street_address[1:]))
        processed_address = [street_address[0] + ' ' + ' '.join(filter(lambda x: ('#' not in x and 'suite' not in x.lower() and 'ste' not in x.lower()), street_address[1:]))] + document["Address"].split(',')[1:]
        processed_address = ','.join(processed_address)
        if processed_address not in visited:
            if block_id not in dict:
                dict[block_id] = [(0, processed_address)]
            else:
                dict[block_id].append((0, processed_address))
            
    
    type = {}
    options = {}
    plotarea = {}
    series = []
    finalJson = {}
    
    type['type'] = 'treemap'
    options['split-type'] = 'balanced'
    options['color-type'] = 'palette'
    options['palette'] = ["#EF767A", "#7C99B4", "#8EB8E5", "#49DCB1", "#49DCB1", "#C2BBF0", "#3590F3", "#034732", "#F58F84", "#5B3256", "#317589", "#6B9362", "#8D6B94", "#565676", "#C38D94", "#565676"]

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
            childy['text'] = child[1].split(',')[0] + " - " + str(child[0]) + " Case(s), " + str(numViol) + " Violation(s)" 
            childy['value'] = child[0] + numViol
            children.append(childy)
            sumChid += child[0]
            sumChildViol += numViol
        parent['children'] = children
        parent['text'] = key + ' - ' + str(sumChid) + " Case(s), " + str(sumChildViol) + " Violation(s)"
        series.append(parent)

    finalJson['series'] = series
    r = finalJson
    r = json.dumps(r)
    loaded_r = json.loads(r)
    client1.close()
    return loaded_r
