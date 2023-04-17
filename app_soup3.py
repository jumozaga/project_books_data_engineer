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

db = conect_db(con, host, port, db_name)

# URL do site que será feito o web scraping
url = "http://books.toscrape.com/"

# Realiza a requisição HTTP para a página
response = requests.get(url)

# Cria um objeto BeautifulSoup com o conteúdo HTML da página
soup = BeautifulSoup(response.text, "html.parser")

categorias = soup.find('ul', {'class': 'nav-list'}).find('ul').find_all(
    'a') if soup.find('ul', {'class': 'nav-list'}) else None

for categoria in categorias:
    
    print(f"Processando categoria: {categoria.text.strip()}")

    # MONTA A URL COM A CATEGORIA 
    url2 = url + categoria['href']

    # USA NOVO ENDEREÇO COM A CATEGORIA  
    response2 = requests.get(url2)
    html = response2.text
    soup2 = BeautifulSoup(html, "html.parser")

    # ENCONTRA A QUANTIDADE DE PAGINAS / SESSÃO
    current = soup2.find("li", class_="current")
    current = int(current.text.split("of")[1]) if current else 1

    # VARRE AS PAGINAS DENTRO DA URL CATEGORIA
    for n in range(1, current+1):
        pages = url2.replace("index.html", f"page-{n}.html") if current > 1 else url2
        response3 = requests.get(pages)
        html3 = response3.text
        soup3 = BeautifulSoup(html3, "html.parser")

        # PEGA OS LIVROS NA PAGINA DA CATEGORIA NA PAG X
        livros = soup3.find_all('article', class_='product_pod')

        for livro in livros:

            # titulo = livro.select_one("h3 a").text
            titulo = livro.h3.a['title']

            preco = livro.select_one(".price_color").text

            estrelas = livro.select_one("p.star-rating")["class"][-1]

            categoria_nome = categoria.text.strip()

            estoque = livro.select_one(".instock.availability").text.strip()

            # Cria um dicionário com os dados do livro
            livro_data = {
                "titulo": titulo,
                "categoria": categoria_nome,
                "estrelas": estrelas,
                "preco": preco,
                "estoque": estoque,
            }

            # Insere o livro no arquivo CSV
            with open("livros3.csv", "a", encoding="utf-8") as f:
                f.write(f"{titulo},{categoria_nome},{estrelas},{preco},{estoque} \n")
            print("CSV criado")

            # Insere o livro no banco de dados MongoDB
            print("SALVANDO OS DADOS NO BANCO DE DADOS")
            db.livros.insert_one(livro_data)

print("DADOS SALVOS COM SUCESSO")



       # nav = soup.select_one(".nav-list")
        # categorias = [a.text.strip() for a in nav.select("a")]

    # url2 = f"""https://books.toscrape.com/catalogue/category/books/{
    #     categoria.lower()+ "_"}/index.html
    # """
    

        # Processar a página e extrair a categoria de cada livro
        # livros = soup3.select('[class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]')
