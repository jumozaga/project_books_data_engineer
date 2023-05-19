import pandas as pd
from bs4 import BeautifulSoup
import requests

def transform_data():
    
    try:
        ARQUIVO = """
    https://raw.githubusercontent.com/jumozaga/webScraping/master/raw/livros.csv
    """
    except:
        
        print("Arquivo não encontrado")
        
    finally:
        ARQUIVO = """./raw/livros.csv"""

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

    # Busca a cotação real para REAL - Libra Esterlina - Scrap para pegar cotação do dia
    cotacao = requests.get(
        'https://www.remessaonline.com.br/cotacao/cotacao-libra-esterlina')
    soup = BeautifulSoup(cotacao.text, 'html.parser')
    cotacao = soup.find(
        "div", class_="style__Text-sc-1a6mtr6-2 ljisZu") if soup else 6.25
    real_libra = float((cotacao.text[0:4]).replace(",", "."))
    print("Cotação hoje: ", real_libra)


    # COLOCANDO O PREÇO EM REAIS
    df['Preco'] = df['Preco'].apply(lambda x: round(
        float(x.replace('Â£', '')) * real_libra, 2))

    # REMOVE DF COLUNA
    # df2 = df.drop('Real', axis=1)

    # SUBSTITUINDO IN STOCK POR SIM OU NÃO
    df.loc[df.Em_estoque.str.strip() == 'In stock', 'Em_estoque'] = 'SIM'
    df.loc[df.Em_estoque.str.strip() != 'In stock', 'Em_estoque'] = 'NÃO'

    # COLOCANDO AS PALAVRAS EM PORTUGUÊS
    df['Classificacao'] = df['Classificacao'].replace(
        {'One': 'Um', 'Two': 'Dois', 'Three': 'Três',
        'Four': 'Quatro', 'Five': 'Cinco'})
    df['Categoria'] = df['Categoria'].replace({'Travel': 'Viagem', 'Politics': 'Politica',
                                            'Mystery': 'Mistério', 'Historical Fiction': 'Historico Ficção',
                                            'Sequential Art': 'Arte', 'Fiction': 'Ficção', 'Classics': 'Classicos',
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


    return df.to_csv('./transformed_data/livros_t.csv', index=False)
