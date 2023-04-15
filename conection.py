from pymongo import MongoClient

# con="mongodb"
# host="0.0.0.0"
# port="27017"
# db_name="livros3"

def conect_db(con, host, port, db_name):
    """_Resumo da função_

    Arguments:
        host -- _IP host, não usar 'localhost' use:0.0.0.0_
        port -- _Porta do Banco_
        db_name -- _Nome do Banco de dados_

    Keyword Arguments:
        type -- _postgresql ou mongodb)

    Returns:
        _db=client[db_name]_
    """
    
    client = MongoClient(f"{con}://{host}:{port}")
    print(client)
    db = client[f"{db_name}"]
    return db


# conect_db(con, host, port, db_name)
