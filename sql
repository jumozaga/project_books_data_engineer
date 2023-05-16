BEGIN;

CREATE TABLE IF NOT EXISTS public.tb_dim_categoria
(
    id_categoria SERIAL PRIMARY KEY,
    categoria VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS public.tb_dim_estoque
(
    id_estoque SERIAL PRIMARY KEY,
    estoque INT
);

CREATE TABLE IF NOT EXISTS public.tb_dim_tempo
(
    id_tempo SERIAL PRIMARY KEY,
    data DATE,
    hora TIME
);

CREATE TABLE IF NOT EXISTS public.tb_dim_livro
(
    id_livro SERIAL PRIMARY KEY,
    titulo VARCHAR(100),
    preco NUMERIC(10, 2),
    estrelas INT,
    fk_dim_categoria INT REFERENCES tb_dim_categoria(id_categoria),
    fk_dim_estoque INT REFERENCES tb_dim_estoque(id_estoque)
);

CREATE TABLE IF NOT EXISTS public.tb_fat_vendas_troca
(
    id_fat_venda SERIAL PRIMARY KEY,
    fk_dim_livro INT REFERENCES tb_dim_livro(id_livro),
    fk_dim_tempo INT REFERENCES tb_dim_tempo(id_tempo),
    quantidade_vendida INT,
    valor_total NUMERIC(10, 2)
);

END;
