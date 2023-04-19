import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm
import time

# solicitação HTTP
base_url = "https://books.toscrape.com/"
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')
url_category = "https://books.toscrape.com/catalogue/category/books/"

# encontrar todas as categorias
categories = soup.find('ul', {'class': 'nav-list'}).find('ul').find_all(
    'a') if soup.find('ul', {'class': 'nav-list'}) else None

# criando um arquivo CSV para salvar os dados coletados
filename = "livros.csv"
with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['titulo', 'preco', 'estoque', 'rating', 'categoria'])

    # iterar sobre todas as categorias e encontrar os livros
    if categories:
        for category in categories:
            category_url = base_url + category['href']
            while True:
                # solicitação HTTP para cada página da categoria

                response = requests.get(category_url)
                soup = BeautifulSoup(response.content, 'html.parser')

                # encontrar todos os livros da página atual
                books = soup.find_all('article', {'class': 'product_pod'})
                total_books = len(books)

                for i, book in enumerate(tqdm(books, desc=category.text.strip(), total=total_books)):
                    title_tag = book.select_one("h3 a")
                    title = title_tag['title'] if 'title' in title_tag.attrs else title_tag.get_text(
                    )
                    price = book.select_one(".price_color").get_text()
                    stock = book.select_one(
                        ".instock.availability").get_text().strip()
                    rating = book.select_one("p.star-rating")["class"][-1]
                    category_name = category.text.strip()

                    # salvar os dados em um arquivo CSV
                    writer.writerow(
                        [title, price, stock, rating, category_name])
                    
                # encontrar o link para a próxima página, se houver
                next_button = soup.find('li', {'class': 'next'})
                if next_button is not None:
                    next_page_url = category_url.rsplit(
                        '/', 1)[0] + '/' + next_button.a['href']
                    category_url = next_page_url
                    
                    # esperar 1 segundo entre as requisições HTTP
                    time.sleep(1)
                else:
                    break