import csv
from conection_db import conect_postgres

conn = conect_postgres()

try:
    with open('./transformed_data/livros_t.csv', 'r', newline='') as arquivo:
        leia = csv.reader(arquivo)
        next(leia)                
        for data in leia:  # Usar leia em vez de arquivo para iterar pelas linhas do CSV
            # Pega os dados do livro no arquivo CSV
            titulo = data[0]
            categoria = data[1]
            estrelas = data[2]
            preco = data[3]
            estoque = data[4]

            cur = conn.cursor()

            cur.execute(
                """INSERT INTO tb_dim_categoria (categoria) VALUES (%s)
                ON CONFLICT (categoria) DO NOTHING""", (categoria,))
            
            cur.execute(
                """INSERT INTO tb_dim_estoque (estoque) VALUES (%s)
                ON CONFLICT (estoque) DO NOTHING""", (estoque,))
            
            cur.execute(
                """INSERT INTO tb_dim_livro(titulo, preco, estrelas, fk_dim_categoria, fk_dim_estoque)
                VALUES (%s, %s, %s, (SELECT id_categoria FROM tb_dim_categoria WHERE categoria = %s),
                (SELECT id_estoque FROM tb_dim_estoque WHERE estoque = %s))
                """,(titulo, preco, estrelas, categoria, estoque))
            
            conn.commit()

except Exception as e:
    print(f"Ah, não !Um erro ocorreu: {e}")

finally:
    conn.close()
    arquivo.close()
