import csv
from conection_db import conect_postgres

conn = conect_postgres()


with open('./transformed_data/livros_t.csv', 'r', newline='') as arquivo_csv:
    for data in arquivo_csv:
        # Pega o livro no arquivo CSV
        data = data.split(',')
        # molde = f"{titulo},{categoria_nome},{estrelas},\
        #             {preco},{estoque}"
        titulo = data[0]
        categoria = data[1]
        estrelas = data[2]
        preco = data[3]
        estoque = data[4]

        cur = conn.cursor()

        cur.execute(
            """INSERT INTO tb_dim_categoria (categoria) VALUES (%s) 
                ON CONFLICT (categoria) DO NOTHING""", (categoria,))
        conn.commit()

        cur.execute(
            """INSERT INTO tb_dim_estoque (estoque) VALUES (%s) 
                ON CONFLICT (estoque) DO NOTHING""", (estoque,))
        conn.commit()

        cur.execute(
            """INSERT INTO tb_dim_livro(titulo) VALUES (%s) 
                ON CONFLICT (titulo) DO NOTHING""", (titulo,))
        conn.commit()

        cur.execute(
            """INSERT INTO tb_dim_livro(preco) VALUES (%d) 
                ON CONFLICT (preco) DO NOTHING""", (preco,))
        conn.commit()

        cur.execute(
            """INSERT INTO tb_dim_livro(estrelas) VALUES (%s) 
                ON CONFLICT (estrelas) DO NOTHING""", (estrelas,))
        conn.commit()
conn.close()
arquivo_csv.close()
