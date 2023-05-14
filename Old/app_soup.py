from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

# Conecta com o banco de dados MongoDB
client = MongoClient('mongodb://172.17.0.2:27017/')
db = client['livros']

# URL do site que será feito o web scraping
url = 'http://books.toscrape.com/index.html'

# Realiza a requisição HTTP para a página
response = requests.get(url)

# Cria um objeto BeautifulSoup com o conteúdo HTML da página
soup = BeautifulSoup(response.text, 'html.parser')

# Encontra todos os elementos de livro da página
print("Olhando os elementos da pagina")
livros = soup.find_all('article', class_='product_pod')

# Itera sobre cada livro encontrado
for livro in livros:
    # Encontra o título do livro
    print("Procurando o título")
    titulo = livro.h3.a['title']

    # Encontra a categoria do livro
    print("Procurando categoria")
    categoria = livro.select('a')[1]['href'].split('/')[2]

    # Encontra a avaliação do livro em estrelas
    print("Procurando as estrelas")
    estrelas = livro.select('p')[0]['class'][1]

    # Cria um dicionário com os dados do livro
    print("Criando Dicionario")
    livro_data = {
        'titulo': titulo,
        'categoria': categoria,
        'estrelas': estrelas
    }
    print("Dicionario criado")

    # Insere o livro no banco de dados MongoDB
    print("Indo lá no BD, me deseja boa sorte hehe")
    db.livros.insert_one(livro_data)
