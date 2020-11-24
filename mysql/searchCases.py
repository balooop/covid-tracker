import pymysql

#rds settings
# CHANGE RDS_HOST AND DB_NAME
rds_host  = 'covid-tracker.c7ic0rieoltc.us-east-1.rds.amazonaws.com'
username = 'admin'
password = 'Cov1dgrap3'
db_name = 'covid-tracker'  

conn = pymysql.connect(rds_host, user=username, passwd=password, db=db_name, connect_timeout=5)
    
def handler(event, context):
    ### find all cases matching the given address from the cases table

    # connects to database
    with conn.cursor() as cur:
        # finds count of all cases
        cur.execute('SELECT num_cases FROM Addresses WHERE _address = "' + str(event['address']) + '"')
        result=cur.fetchone()
        conn.commit()
    conn.commit()
    if result is None:
        return 0
    return result[0]
    