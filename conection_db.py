import os
from pymongo import MongoClient
import psycopg
from dotenv import load_dotenv

load_dotenv()

# con="mongodb"
# host="0.0.0.0"
# port="27017"
# db_name="livros3"

con = os.getenv("CONEXAO")
host = os.getenv("HOST")
port = os.getenv("PORT")
db_name = os.getenv("DATABASE")


def conect_mongodb(con=con, host=host, port=port, db_name=db_name):
    client = MongoClient(f"{con}://{host}:{port}")
    print(client)
    db = client[f"{db_name}"]
    return db
# conect_db(con, host, port, db_name)


host2 = os.environ.get("host")
db = os.environ.get("db")
user = os.environ.get("user")
password = os.environ.get("password")


def conect_postgres(db=db, user=user, password=password):

    conn = psycopg.connect(
        f"dbname={db} user={user} password={password}"
    )
    
    return conn


