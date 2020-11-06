import sys
import logging
import pymysql
from datetime import datetime
import uuid
#rds settings
rds_host  = 'covid-tracker-locations-db.c8wmeg2eqxqu.us-east-2.rds.amazonaws.com'
username = 'admin'
password = 'password'
db_name = 'covid_locations_db'

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
    addCase(str(event['address']))
    return "Added %d items from RDS MySQL table" %(item_count)


def addCase(addresses_visited):
    ### insert case into Cases table
    # generate UUID for case
    case_id = str(uuid.uuid1())
    
    # connects to database
    with conn.cursor() as cur:
        # inserts case into Cases
        cur.execute('INSERT into Cases (address_visited, case_id, timestamp) Values ("'+addresses_visited+'", "'+case_id+'", CURRENT_TIMESTAMP)')
        cur.execute("select * from Cases")
        conn.commit()
    
        # compute 'block_id'
        num_spaces = 0
        street_address = addresses_visited.split(',')[0].split(' ')
        block_id = str((int)street_address[0]/100) + ''.join(street_address[1:])
        
        cur.execute(' INSERT into Addresses(_address, block_id) Values("'+addresses_visited+'", "'+block_id+'" ')
        conn.commit()
    conn.commit()
    return
    
# parse data from website (addresses visited + businesses reported)
# call two functions: 1 for addresses, 1 for businesses (dummy)
# addresses function:
#   insert into Cases table (X)
#   check if address exists in Addresses table
#       if no: 
#           calculate block_id
#           create new row in Addresses table: cases == 1
#           update number of cases in block
#               
#       if yes:
#           find address in table
#           update num_cases
#           find block in table
#           update num cases_blk