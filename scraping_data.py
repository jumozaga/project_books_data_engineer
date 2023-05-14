from bs4 import BeautifulSoup
import requests

def scraping():
    # URL do site que será feito o web scraping
    url = "http://books.toscrape.com/"    
    # Realiza a requisição HTTP para a página
    response = requests.get(url)
    # Cria um objeto BeautifulSoup com o conteúdo HTML da página
    soup = BeautifulSoup(response.text, "html.parser")
    categorias = (
        soup.find("ul", {"class": "nav-list"}).find("ul").find_all("a")
        if soup.find("ul", {"class": "nav-list"})
        else None
    )

    livros_data = []

    for categoria in categorias:
        print(f"Processando categoria: {categoria.text.strip()}")

        # MONTA A URL COM A CATEGORIA
        url2 = url + categoria["href"]

        # USA NOVO ENDEREÇO COM A CATEGORIA
        response2 = requests.get(url2)
        html = response2.text
        soup2 = BeautifulSoup(html, "html.parser")

        # ENCONTRA A QUANTIDADE DE PAGINAS / SESSÃO
        current = soup2.find("li", class_="current")
        current = int(current.text.split("of")[1]) if current else 1

        # VARRE AS PAGINAS DENTRO DA URL CATEGORIA
        for n in range(1, current + 1):
            pages = url2.replace(
                "index.html", f"page-{n}.html") if current > 1 else url2
            response3 = requests.get(pages)
            html3 = response3.text
            soup3 = BeautifulSoup(html3, "html.parser")

            # PEGA OS LIVROS NA PAGINA DA CATEGORIA NA PAG X
            livros = soup3.find_all("article", class_="product_pod")

            for livro in livros:
                # titulo = livro.select_one("h3 a").text
                titulo = livro.h3.a["title"].replace(",", ".").strip()

                preco = livro.select_one(".price_color").text.strip()
                # preco = livro.select("p")[1].text.strip()

                estrelas = livro.select_one(
                    "p.star-rating")["class"][-1].strip()

                categoria_nome = categoria.text.strip()

                estoque = livro.select_one(
                    ".instock.availability").text.strip()

                molde = f"{titulo},{categoria_nome},{estrelas},\
                    {preco},{estoque}"

                livros_data.append(molde)
                
    return livros_data

