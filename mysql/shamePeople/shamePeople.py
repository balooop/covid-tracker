import sys
import logging
import pymysql
import json
import re

#rds settings
rds_host  = 'covid-tracker.c7ic0rieoltc.us-east-1.rds.amazonaws.com'
username = 'admin'
password = 'Cov1dgrap3'
db_name = 'covid-locations-tracker'
conn = pymysql.connect(rds_host, user=username, passwd=password, db=db_name, connect_timeout=5)

# logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def handler(event, context):
    businessDict = []
    peopleDict = []
    returnDict = {}
    visited = []
    cur = conn.cursor()
    # get number of cases, block id, and address visited for each address
    result_row = cur.execute("SELECT _address, num_cases, num_cases_blk FROM Cases NATURAL JOIN Addresses NATURAL JOIN Blocks GROUP BY netid HAVING num_cases = num_cases_blk;")
    query_result = cur.fetchall()
    conn.commit()
    for row in query_result:
        address = row[0]
        numCases = row[1]
        businessDict.append((address, numCases))
    result_row = cur.execute("SELECT netid, COUNT(_address) as num_caused FROM Cases JOIN Addresses on Cases.address_visited = Addresses._address GROUP by netid ORDER BY num_caused DESC;")
    query_result = cur.fetchall()
    conn.commit()
    for row in query_result:
        netID = row[0]
        num_caused = row[1]
        peopleDict.append((netID, num_caused))
            
    
    returnDict['people'] = peopleDict
    returnDict['business'] = businessDict
    
    r = returnDict
    r = json.dumps(r)
    loaded_r = json.loads(r)
    return loaded_r
