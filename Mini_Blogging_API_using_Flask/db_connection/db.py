import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_DATABASE_HOST = os.getenv('MYSQL_DATABASE_HOST')
MYSQL_DATABASE_USER = os.getenv('MYSQL_DATABASE_USER')
MYSQL_DATABASE_PASSWORD = os.getenv('MYSQL_DATABASE_PASSWORD')
MYSQL_DATABASE_DB = os.getenv('MYSQL_DATABASE_DB')

# Database connection function
def connect_mysql():
    return pymysql.connect(
        host=MYSQL_DATABASE_HOST, 
        user = MYSQL_DATABASE_USER, 
        passwd = MYSQL_DATABASE_PASSWORD, 
        database = MYSQL_DATABASE_DB,
        autocommit = True, 
        charset = 'utf8mb4', 
        port= 3306,
        cursorclass = pymysql.cursors.DictCursor
        )
