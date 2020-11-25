import sys
import logging
import pymysql
from datetime import datetime
import uuid
import re
#rds settings
# CHANGE RDS_HOST AND DB_NAME
rds_host  = 'covid-tracker.c7ic0rieoltc.us-east-1.rds.amazonaws.com'
username = 'admin'
password = 'Cov1dgrap3'
db_name = 'covid-tracker'

logger = logging.getLogger()
logger.setLevel(logging.INFO)
try:
    conn = pymysql.connect(rds_host, user=username, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()
    
# logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def handler(event, context):
    maskFlag = 0
    socialDistancingFlag = 0
    sickFlag = 0
    dirtyFlag = 0
    
    maskWords = ['no mask', 'lost mask', 'on chin', 'nose', '', 'covering', 'not wearing', "weren't wearing", "wasn't wearing", "isn't wearing", ""]
    socialDistancing = ['too many people', 'no social distancing', 'crowded']
    sick = ['cough', 'coughing', 'sick', 'ill', 'sneeze', 'covid', ]
    dirty = ['dirty', 'nasty', 'gross', 'not clean', 'rancid', 'unsanitary', 'unhygenic', 'health concerns', 'smells bad', 'not hygenic', 'bad hygenie', 'concern for health']
    
    words = event['Complaints'].lower()
    for word in maskWords:
        if word in words:
            maskFlag = 1
            break
    for word in socialDistancing:
        if word in words:
            socialDistancingFlag = 1
            break
    for word in sick:
        if word in words:
            sickFlag = 1
            break
    for word in dirty:
        if word in words:
            dirtyFlag = 1
            break
            

