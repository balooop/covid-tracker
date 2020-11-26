import sys
import logging
import pymysql
import json
#rds settings
rds_host  = 'covid-tracker.c7ic0rieoltc.us-east-1.rds.amazonaws.com'
username = 'admin'
password = 'Cov1dgrap3'
db_name = 'covid-locations-tracker'

logger = logging.getLogger()
logger.setLevel(logging.INFO)
try:
    conn = pymysql.connect(rds_host, user=username, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()
    
logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def handler(event, context):
    print("hi")
    dict = {}
    sql = "SELECT COUNT(*) AS numCasesPerAddr, block_id, address_visited FROM Cases GROUP BY address_visited"
    cursor = conn.cursor()
    result_row = cursor.execute(sql)
    query_result = cursor.fetchall()
    for row in query_result:
        numCases = row[0]
        blockId = row[1]
        addrVisited = row[2]
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
    options['palette'] = ["#1ab7ea", "#ff5700", "#cd201f", "#25D366", "#FFFC00", "#3aaf85", "#f1c40f", "#17968e", "#f7b362", "#F58F84", "#5B3256", "#317589", "#6B9362"]
    
    plotarea['margin'] = "0 0 35 0"
    
    
    finalJson.update(type)
    finalJson['options'] = options
    finalJson['plotarea'] = plotarea
    
    
    
    for key in dict:
        parent = {}
        parent['text'] = key
        children = []
        for child in dict[key]:
            childy = {}
            childy['text'] = child[1]
            childy['value'] = child[0]
            children.append(childy)
        parent['children'] = children
        series.append(parent)
    
    finalJson['series'] = series
    r = finalJson
    r = json.dumps(r)
    loaded_r = json.loads(r)
    return loaded_r
