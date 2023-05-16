from pymongo import MongoClient
import psycopg
# con="mongodb"
# host="0.0.0.0"
# port="27017"
# db_name="livros3"


def conect_mongodb(con, host, port, db_name):
    client = MongoClient(f"{con}://{host}:{port}")
    print(client)
    db = client[f"{db_name}"]
    return db
# conect_db(con, host, port, db_name)


def conect_postgres(db, user, password):

    conn = psycopg.connect(
        f"dbname={db} user={user} password={password}"
    )

    return conn
