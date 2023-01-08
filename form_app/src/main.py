from app import app
from repository import insert_documents, forms, client

db = client['my_database']

forms_collection = db['forms_collection']


def main():
    """Функция проверяет наличие записей в БД, если база пустая, то заполняется фикстурами. Возвращает WSGI приложение"""
    db_form = forms_collection.find_one()
    if not db_form:
        insert_documents(forms, forms_collection)
    return app


form_app = main()
