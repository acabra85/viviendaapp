import os
from botocore.exceptions import ClientError
import pymysql
import boto3
import logging


def get_db_pwd_parameter(parameter_name):
    print('extract access...')
    ssm_client = boto3.client('ssm')
    try:
        result = ssm_client.get_parameter(
            Name=parameter_name,
            WithDecryption=True
        )['Parameter']['Value']
        return result
    except ClientError as e:
        logging.error(e)
        return None


def get_db_connection(auto_commit=True):
    print('Connecting to db ...')
    db_rds_host = 'viviendadb1.cwfju1wpxqlz.us-east-1.rds.amazonaws.com'
    db_user = 'admin'
    db_name = 'viviendadb1'
    db_password = get_db_pwd_parameter(os.getenv('dbpwd'))

    if not db_password or len(db_password) < 3:
        raise Exception("unable to retrieve db password: [" + db_password + "]")

    try:
        conn = pymysql.connect(host=db_rds_host,
                               user=db_user,
                               port=3306,
                               passwd=db_password,
                               db=db_name,
                               charset='utf8',
                               autocommit=auto_commit,
                               connect_timeout=5)
        print(' ... connected ? [' + str(conn.open))
        return conn
    except Exception as e:
        print("ERROR: Unexpected error: Could not connect to MySql instance.:" + str(e))
        return None
