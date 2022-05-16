import os
import pymysql
import boto3
import logging
import traceback


def get_db_pwd_parameter(parameter_name):
    print('extract access...')
    try:
        ssm_client = boto3.client('ssm')
        result = ssm_client.get_parameter(
            Name=parameter_name,
            WithDecryption=True
        )['Parameter']['Value']
        return result
    except Exception:
        logging.error(traceback.format_exc())
        return None


def get_db_connection(auto_commit=True):
    print('Connecting to db ...')
    db_rds_host = 'viviendadb1.cwfju1wpxqlz.us-east-1.rds.amazonaws.com'
    db_user = 'admin'
    db_name = 'viviendadb1'
    env_var_pwd = os.getenv('dbpwd')
    if not env_var_pwd:
        logging.error('unable to retrieve db password key')
        return None
    db_password = get_db_pwd_parameter(env_var_pwd)

    if not db_password or len(db_password) < 3:
        logging.error("unable to retrieve db password: [" + str(db_password) + "]")
        return None

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
