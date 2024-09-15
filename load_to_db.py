import json
from sqlalchemy.orm import sessionmaker
from models import Author, Quote  # Ваші моделі для цитат та авторів
from base import engine

Session = sessionmaker(bind=engine)
session = Session()

# Завантаження авторів
with open('authors.json', 'r') as f:
    authors = json.load(f)
    for author in authors:
        new_author = Author(
            name=author['author'],
            birth_date=author['birth_date'],
            birth_place=author['birth_place'],
            description=author['description']
        )
        session.add(new_author)

# Завантаження цитат
with open('quotes.json', 'r') as f:
    quotes = json.load(f)
    for quote in quotes:
        new_quote = Quote(
            text=quote['quote'],
            author_name=quote['author'],  # Використовуємо ім'я автора для зовнішнього ключа
            tags=",".join(quote['tags'])  # Зберігаємо теги через кому
        )
        session.add(new_quote)

session.commit()
