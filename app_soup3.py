
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from conection import conect_db

load_dotenv()

con = os.getenv("CONEXAO")
host = os.getenv("HOST")
port = os.getenv("PORT")
db_name = os.getenv("DATABASE")

db = conect_db(con,host, port, db_name)
    


# URL do site que será feito o web scraping
url = "http://books.toscrape.com/index.html"

# Realiza a requisição HTTP para a página
response = requests.get(url)

# Cria um objeto BeautifulSoup com o conteúdo HTML da página
soup = BeautifulSoup(response.text, "html.parser")
nav = soup.select_one(".nav-list")
categorias = [a.text.strip() for a in nav.select("a")]
# livros = soup.select(".product_pod")
for categoria in categorias:
    print(f"Processando categoria: {categoria}")
    url2 = f"https://books.toscrape.com/catalogue/category/books/{categoria.lower().replace(' ', '-')}/index.html"
    print(url2)
    response2 = requests.get(url2)
    html = response2.text
    soup2 = BeautifulSoup(html, "html.parser")
    print(soup2)
    # Processar a página e extrair a categoria de cada livro    
    livros = soup.select('[class=\"col-xs-6 col-sm-4 col-md-3 col-lg-3\"]')
    print(livros)
    
    print("Fim da Categoria:'{}'".format(categoria))
    for livro in livros:
            titulo = livro.select_one("h3 a").text
            preco = livro.select_one(".price_color").text
            estrelas = livro.select_one("p.star-rating")["class"][-1]
            categoria = categoria
            # categoria = soup2.select_one(".breadcrumb li:nth-of-type(3) a")
            estoque = livro.select_one(".instock.availability").text.strip()


            # Cria um dicionário com os dados do livro
            print("Criando Dicionario")

            livro_data = {
                "titulo": titulo,
                "categoria": categoria,
                "estrelas": estrelas,
                "preco": preco,
                "estoque": estoque,
            }
            print("Dicionario criado")

            print("Criando CSV em UTF-8")
            with open("livros3.csv", "a", encoding="utf-8") as f:
                f.write(f"{titulo},{categoria},{estrelas},{preco},{estoque} \n")
            print("CSV criado")
            
            # Insere o livro no banco de dados MongoDB
            print("Indo lá no BD, me deseja boa sorte hehe")
            db.livros.insert_one(livro_data)
            print("Inserido no BD")
