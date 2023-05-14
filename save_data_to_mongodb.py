import os
from dotenv import load_dotenv
from conection_db import conect_db
from scraping_data import scraping


def save_mongo():

    load_dotenv()

    con = os.getenv("CONEXAO")
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    db_name = os.getenv("DATABASE")
    db = conect_db(con, host, port, db_name)

    livros_data = scraping()

    for data in livros_data:
        data = data.split(',')
        # Cria um dicionário com os dados do livro
        livro_data = {
            "titulo": data[0],
            "categoria": data[1],
            "estrelas": data[2],
            "preco": data[3],
            "estoque": data[4],
        }

        # Insere o livro no banco de dados MongoDB
        print("SALVANDO OS DADOS NO BANCO DE DADOS")
        db.livros.insert_one(livro_data)
    return "Dados salvos com sucesso no banco de dados MongoDB"


save_mongo()
