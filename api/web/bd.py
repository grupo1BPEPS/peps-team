<<<<<<< HEAD
# bd.py
import os
import pymysql
##from dotenv import load_dotenv

##load_dotenv()

def obtener_conexion():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )
=======
import os
import pymysql

def obtener_conexion():
    return pymysql.connect(host=os.environ.get('DB_HOST'),
                                user=os.environ.get('DB_USERNAME'),
                                password=os.environ.get('DB_PASSWORD'),
                                port=int(os.environ.get('DB_PORT', 3306)),
                                db=os.environ.get('DB_DATABASE'))
>>>>>>> d011334 (Test)
