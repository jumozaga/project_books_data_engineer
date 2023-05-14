from scraping_data import scraping


def save_csv():
    livros_data = scraping()

    for data in livros_data:
        # Insere o livro no arquivo CSV
        with open("./livros.csv", "a", encoding="utf-8") as f:
            f.write(data+"\n")

    return "CSV criado"


save_csv()
