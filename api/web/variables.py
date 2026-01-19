import os

def cargarvariables():
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_USER'] = 'root'
    os.environ['DB_PASS'] = 'password'
    os.environ['DB_NAME'] = 'gym_app'
