from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

# Conecta com o banco de dados MongoDB
client = MongoClient('mongodb://172.17.0.5:27017/')
db = client['livros2']

# URL do site que será feito o web scraping
# url = 'http://books.toscrape.com/index.html'
for n in range(1,51):
      url = f'https://books.toscrape.com/catalogue/page-{n}.html'

      # Realiza a requisição HTTP para a página
      response = requests.get(url)

      # Cria um objeto BeautifulSoup com o conteúdo HTML da página
      soup = BeautifulSoup(response.text, 'html.parser')
      # nexts = soup.find('li', class_='next')
      current = soup.find('li', class_='current')

      # for n in range (int(current.text.split('of')[1])):
      #  Encontra todos os elementos de livro da página
      print("Olhando os elementos da pagina")
      livros = soup.find_all('article', class_='product_pod')
      # livros = soup.select('[class=\"col-xs-6 col-sm-4 col-md-3 col-lg-3\"]')
      # print(livros)

      
            # Itera sobre cada livro encontrado
      for livro in livros:
            # Encontra o título do livro
            print("Procurando o título")
            titulo = livro.h3.a['title']

            # Encontra a categoria do livro
            print("Procurando categoria")           
            # categoria = livro.select('a')[0]['href'].split('/')[1]
            categoria =livro.h3.a['href'].split('/')[-2]


            # Encontra a avaliação do livro em estrelas
            print("Procurando as estrelas")
            estrelas = livro.select('p')[0]['class'][1]
            # estrelas = livro.selectFisrt("p:contains(star-rating)")
            
            print("Procurando o preço")
            preco = livro.select('p')[1].text
            
            print("Procurando a disponibilidade")
            estoque = livro.select('p')[2].text

            # Cria um dicionário com os dados do livro
            print("Criando Dicionario")
            livro_data = {
                  'titulo': titulo,
                  'categoria': categoria,
                  'estrelas': estrelas,
                  'preco': preco,
                  'estoque': estoque,
            }
            print("Dicionario criado")
            
            print("Criando CSV em UTF-8")
            with open('livros.csv', 'a', encoding='utf-8') as f:
                  f.write(f'{titulo},{categoria},{estrelas},{preco},{estoque} \n')
            print("CSV criado")     
            

            # Insere o livro no banco de dados MongoDB
            # print("Indo lá no BD, me deseja boa sorte hehe")
            # db.livros.insert_one(livro_data)
            # print("Inserido no BD")
