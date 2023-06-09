# -*- coding: utf-8 -*-
"""clean.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CNrunmLYCUYSl69lcE4jlyvwu-EKK_bU
"""
import pandas as pd
import sweetviz as sv
import numpy as np
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt


ARQUIVO = """
https://raw.githubusercontent.com/jumozaga/webScraping/master/raw/livros.csv
"""

df = pd.read_csv(ARQUIVO, header=None)
df = df.rename(
    columns={
        0: "Titulo",
        1: "Categoria",
        2: "Classificacao",
        3: "Preco",
        4: "Em_estoque",
    }
)
df2 = df.copy(deep=True)

# Busca a cotação real para REAL - Libra Esterlina - Scrap para pegar cotação do dia
cotacao = requests.get(
    'https://www.remessaonline.com.br/cotacao/cotacao-libra-esterlina')
soup = BeautifulSoup(cotacao.text, 'html.parser')
cotacao = soup.find(
    "div", class_="style__Text-sc-1a6mtr6-2 ljisZu") if soup else 6.25

real_libra = float((cotacao.text[0:4]).replace(",", "."))
print("Cotação hoje: ", real_libra)

# MODIFICANDO DATAFRAME
# COLOCANDO O PREÇO EM REAIS
# df['Preco']= df['Preco'].str.replace('Â£','')
# df['Preco']= df['Preco'].astype(float) * real_libra
df2['Preco'] = df['Preco'].apply(lambda x: round(
    float(x.replace('Â£', '')) * real_libra, 2))

# REMOVE DF COLUNA
# df2 = df.drop('Real', axis=1)

# SUBSTITUINDO IN STOCK POR SIM OU NÃO
df2.loc[df.Em_estoque.str.strip() == 'In stock', 'Em_estoque'] = 'SIM'
df2.loc[df.Em_estoque.str.strip() != 'In stock', 'Em_estoque'] = 'NÃO'
# df2['Em_estoque'] = df2['Em_estoque'].apply(lambda x: True if x == 'In stock' else x)
# df2['Em_estoque'] = df2['Em_estoque'].str.strip().apply(lambda x: True if x == 'In stock' else False)

# COLOCANDO AS PALAVRAS EM PORTUGUÊS
df2['Classificacao'] = df2['Classificacao'].replace(
    {'One': 'Um', 'Two': 'Dois', 'Three': 'Três', 
     'Four': 'Quatro', 'Five': 'Cinco'})
df2['Categoria'] = df2['Categoria'].replace({'Travel': 'Viagem', 'Politics': 'Politica',
                                             'Mystery': 'Mistério', 'Historical Fiction': 'Historico Ficção',
                                             'Sequential Art': 'Arte', 'Fiction': 'Ficção',
                                             'Womens Fiction': 'Ficção Feminina', 'Fantasy': 'Fantasia',
                                             'New Adult': 'Novo Adulto', 'Young Adult': 'Jovem Adulto',
                                             'Science': 'Ciência', 'Poetry': 'Poesia', 'Psychology': 'Psicologia',
                                             'Art': 'Arte', 'Autobiography': 'Autobiografia', 'Parenting': 'Criação de filhos',
                                             'History': 'História', 'Food and Drink': 'Comida', 'Business': 'Negocios',
                                             'Philosophy': 'Filosofia', 'Nonfiction': 'Não Ficção',
                                             'Default': 'Padrão', 'Christian': 'Cristão', 'Health': 'Saúde',
                                             'Self Help': 'Auto-ajuda', 'Spirituality': 'Religioso',
                                             'Academic': 'Acadêmico', 'Contemporary': 'Conteporâneo',
                                             'Thriller': 'Ação', 'Christian Fiction': 'Ficção Cristã',
                                             'Add a comment': 'Sem Categoria', 'Adult Fiction': 'Ficção Adulta'})

# Encontrando o maior valor
maior = df2['Preco'].max()
# Encontrando menor valor
menor = df2.min()['Preco']

# verificando se o DataFrame não está vazio
if not df.empty:
    livro_max_preco = df2[df2['Preco'] == maior][[
        'Titulo', 'Classificacao', 'Preco']].iloc[0]
    livro_min_preco = df2[df2['Preco'] == menor][[
        'Titulo', 'Classificacao', 'Preco']].iloc[0]

df3 = pd.DataFrame([livro_max_preco, livro_min_preco])

# Ordenados pelo preço
ordenada_preco = df2.sort_values('Preco', ascending=False)

# Ordenados pela Classificacao/Avaliação
ordenada_classificacao = df2.sort_values('Classificacao', ascending=True)

# Os 5 mais bem classificados
classificacao_geral = ordenada_classificacao.head(
    196)[['Titulo', 'Categoria', 'Classificacao']]

# Os 5 mais bem classificados por categoria
top_5 = ordenada_classificacao.groupby('Categoria').apply(lambda x: x.head(5))

# Os 5 mais baratos por categoria
top5_p = ordenada_preco.groupby('Categoria').apply(lambda x: x.tail(5))

# Gráfico de barras mostrando a quantidade de livros em cada categoria
# Criar um dicionário contendo a contagem de livros em cada categoria
count_by_category = df2.groupby('Categoria')['Titulo'].count().to_dict()

# Criar o gráfico de barras
plt.bar(range(len(count_by_category)), count_by_category.values())

# Definir as etiquetas dos eixos
plt.xticks(range(len(count_by_category)),
           count_by_category.keys(), rotation=90)
plt.xlabel('Categoria')
plt.ylabel('Quantidade de Livros')
plt.show()

# Quantidade de Títulos por Categoria e Classificação
# criar tabela pivot
pivot_df = df2.pivot_table(
    index='Categoria', columns='Classificacao', values='Titulo', aggfunc='count')
# criar gráfico de barras
pivot_df.plot(kind='bar', stacked=True)
plt.xlabel('Categoria')
plt.ylabel('Quantidade de Títulos')
plt.title('Quantidade de Títulos por Categoria e Classificação')
plt.show()

# criando uma tabela pivot para encontrar o título mais barato e mais caro de cada categoria
pivot_df = df2.pivot_table(index='Categoria', values=['Preco', 'Titulo'], aggfunc={
                           'Preco': [min, max], 'Titulo': 'count'})
# renomeando as colunas
pivot_df.columns = ['Titulo mais barato',
                    'Titulo mais caro', 'Quantidade de títulos']
# criando o gráfico
fig, ax = plt.subplots(figsize=(50, 20))
ax.bar(pivot_df.index, pivot_df['Titulo mais caro'],
       color='red', label='Título mais caro')
ax.bar(pivot_df.index, pivot_df['Titulo mais barato'],
       color='blue', label='Título mais barato')
ax.set_ylabel('Preço')
ax.set_title('Título mais barato e mais caro de cada categoria')
ax.legend()
plt.show()


# sv.analyze(df2).show_html('base.html')
# sv.analyze(df3).show_html('df3.html')
# sv.analyze(ordenada_preco).show_html('ordenada_preco.html')
# sv.analyze(ordenada_classificacao).show_html('ordenada_classificacao .html')
# sv.analyze(classificacao_geral).show_html('classificacao_geral.html')
# sv.analyze(top_5).show_html('top_5.html')
# sv.analyze(top5_p).show_html('top5_p.html')


# filtros = {'5 Melhores Avaliados Por categoria': top_5, 'Top 5 por Preço mais baratos':top5_p, "Mais barato":livro_min_preco, "Mais caro":livro_max_preco,
#         }
# df4= pd.DataFrame.from_dict(filtros,orient="columns")

print(livro_max_preco)
print(livro_min_preco)
print(ordenada_preco)
print(ordenada_classificacao)
print(classificacao_geral)
print(top_5)
print(top5_p)
print(df3)
print(df2)
print(df)
