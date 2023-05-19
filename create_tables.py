import psycopg
from conection_db import conect_postgres

conn = conect_postgres()


def create_tables():
    """
    Cria as tabelas no banco de dados
    :return: None
    """
    with conn.cursor() as cur:
        # Criação das tabelas
        try:
            # Tabela Dimensão Categoria
            cur.execute('''
                CREATE TABLE IF NOT EXISTS tb_dim_categoria(
                    id_categoria SERIAL PRIMARY KEY,
                    categoria VARCHAR(50) 
                )
            ''')
            # Adicionar restrição de unicidade para a coluna categoria
            cur.execute('''
                ALTER TABLE tb_dim_categoria ADD CONSTRAINT unique_categoria UNIQUE (categoria)
            ''')

            # Tabela Dimensão Estoque
            cur.execute('''
                CREATE TABLE IF NOT EXISTS tb_dim_estoque(
                    id_estoque SERIAL PRIMARY KEY,
                    estoque VarChar(50) 
                )
            ''')
            cur.execute('''
                ALTER TABLE tb_dim_estoque ADD CONSTRAINT unique_estoque UNIQUE (estoque)
            ''')

            # Tabela Dimensão Tempo
            cur.execute('''
                CREATE TABLE IF NOT EXISTS tb_dim_tempo(
                    id_tempo SERIAL PRIMARY KEY,
                    data DATE,
                    hora TIME
                )
            ''')
            # Tabela Dimensão Livro
            cur.execute('''
                CREATE TABLE IF NOT EXISTS tb_dim_livro(
                    id_livro SERIAL PRIMARY KEY,
                    titulo VARCHAR(250),
                    preco NUMERIC(10, 3),
                    estrelas varchar(20),
                    fk_dim_categoria INT REFERENCES tb_dim_categoria(id_categoria),
                    fk_dim_estoque INT REFERENCES tb_dim_estoque(id_estoque)
                )

            ''')

            # Tabela Fato (Vendas)
            cur.execute('''
                CREATE TABLE IF NOT EXISTS tb_fat_vendas_troca (
                    id_fat_venda SERIAL PRIMARY KEY,
                    fk_dim_livro INT REFERENCES tb_dim_livro(id_livro),
                    fk_dim_tempo INT REFERENCES tb_dim_tempo(id_tempo),
                    quantidade_vendida INT,
                    valor_total NUMERIC(10, 2)
                )

            ''')

            # Confirma as alterações no banco de dados
            conn.commit()

            print("Tabelas criadas com sucesso!")

        except BaseException as e:
            print(f"Erro ao criar as tabelas{e}")
            conn.rollback()

    return conn


create_tables()
