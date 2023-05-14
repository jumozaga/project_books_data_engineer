from scraping_data import scraping

livros_data = scraping()

for data in livros_data:
    # Insere o livro no arquivo CSV
    with open("./livros.csv", "a", encoding="utf-8") as f:
        f.write(data+"\n")
    print("CSV criado")
