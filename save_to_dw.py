import csv
from conection_db import conect_postgres

conn = conect_postgres()

# Função para inserir os dados na tabela Dimensão Livro


def inserir_dados_dim_livro(cursor, livro):
    query = """
    INSERT INTO tb_dim_livro (
        titulo, estrelas, fk_dim_categoria, fk_dim_estoque, preco)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id_livro
    """
    cursor.execute(query, (livro['titulo'], livro['estrelas'],
                   livro['fk_dim_categoria'], livro['fk_dim_estoque'], livro['preco']))
    livro_id = cursor.fetchone()[0]
    return livro_id

# Função para inserir os dados na tabela Fato (Vendas)


def inserir_dados_fato(cursor, venda):
    query = """
    INSERT INTO tb_fat_vendas_troca (fk_dim_livro, fk_dim_tempo, quantidade_vendida, valor_total)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (venda['fk_dim_livro'], venda['fk_dim_tempo'],
                   venda['quantidade_vendida'], venda['valor_total']))


# Leitura do arquivo CSV
try:
    with open('./transformed_data/livros_t.csv', 'r', newline='') as arquivo_csv:
        
        leitor_csv = csv.DictReader(arquivo_csv)

        cursor = conn.cursor()

        for linha in leitor_csv:
            # Inserir dados na tabela Dimensão Categoria (se necessário)
            categoria = linha['categoria']
            cursor.execute(
                """INSERT INTO tb_dim_categoria (categoria) VALUES (%s) 
                ON CONFLICT (categoria) DO NOTHING""", (categoria,))
            conn.commit()

            # Obter o ID da Dimensão Categoria
            cursor.execute(
                """SELECT id_categoria FROM tb_dim_categoria 
                WHERE categoria = %s""", (categoria,))
            id_categoria = cursor.fetchone()[0]

            # Construir o objeto livro
            livro = {
                'titulo': linha['nome do livro'],
                'estrelas': int(linha['estrela']),
                'fk_dim_categoria': id_categoria,
                'fk_dim_estoque': int(linha['estoque']),
                'preco': float(linha['preco'])
            }

            # Inserir dados na tabela Dimensão Livro
            livro_id = inserir_dados_dim_livro(cursor, livro)

            # Construir o objeto venda
            venda = {
                'fk_dim_livro': livro_id,
                'fk_dim_tempo': 1,  # ID da Dimensão Tempo a ser definido conforme necessidade
                'quantidade_vendida': 0,  # Valor a ser definido conforme necessidade
                'valor_total': 0.0  # Valor a ser definido conforme necessidade
            }

            # Inserir dados na tabela Fato (Vendas)
            inserir_dados_fato(cursor, venda)

            # Confirmar a transação
            conn.commit()

    print("Dados inseridos com sucesso!")

except:
    print("Erro ao inserir os dados!")
