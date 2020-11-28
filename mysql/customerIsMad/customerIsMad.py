import sys
import logging
import pymysql
import json
import pymongo


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
    cur = conn.cursor()
    # get number of cases, block id, and address visited for each address
    result_row = cur.execute("SELECT COUNT(*) AS numCasesPerAddr, block_id, address_visited FROM Cases GROUP BY address_visited")
    query_result = cur.fetchall()
    conn.commit()
    # for each address in the result
    for row in query_result:
        numCases = row[0]
        blockId = row[1]
        addrVisited = row[2]
        # add num cases and address to dictionary entry for the block
        if blockId not in dict:
            dict[blockId] = [(numCases,addrVisited)]
        else:
            dict[blockId].append((numCases,addrVisited))

    
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
    
    # loop through all keys (blocks)
    for key in dict:
        parent = {}
        sumChid = 0
        children = []
        # loop through all values in a key (# cases by  address)
        for child in dict[key]:
            numViol = 0
            print(child[1])
            print(col1.find({'Address': child[1]}).count())
            # find address in MongoDB
            curViol = col1.find({'Address': child[1]})
            if(curViol.count() > 0):
                # for each tuple in the current violation
                for x in curViol:
                    # sum the number of violations by number of mask, SD, sick, and dirty reports
                    numViol += x["mask"]
                    numViol += x["socialDistancing"]
                    numViol += x["sick"]
                    numViol += x["dirty"]
            childy = {}
            childy['text'] = str(child[0]) + " Cases at " + child[1].split(',')[0] + ", " + str(numViol) + " violations" 
            childy['value'] = child[0]
            children.append(childy)
            sumChid += child[0]
        parent['children'] = children
        parent['text'] = key + ' - ' + str(sumChid)
        series.append(parent)
        print("OUT1")
    
    finalJson['series'] = series
    print("OUT2")
    r = finalJson
    r = json.dumps(r)
    loaded_r = json.loads(r)
    client1.close()
    return loaded_r
