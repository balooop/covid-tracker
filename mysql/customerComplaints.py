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
    
    maskWords = ['not wearing', 'covering', 'wearing', 'not wearing']
    socialDistancing = ['too many people', 'no social distancing']
    sick = ['cough', 'coughing', 'sick', 'ill']
    dirty = ['dirty', 'nasty', 'gross', 'not clean', '']
    
    words = event['Complaints']
    for word in maskWords:
        if word in words:
            maskFlag = 1
            break
    for word in socialDistancing:
        if word in words:
            socialDistancingFlag = 1
            break
    for word in sickFlag:
        if word in words:
            sickFlag = 1
            break
    for word in dirtyFlag:
        if word in words:
            dirtyFlag = 1
            break
            

