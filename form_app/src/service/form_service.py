import re
import time

from repository import client

db = client['my_database']

forms_collection = db['forms_collection']


def get_forms_from_db() -> list[dict]:
    """Функция возвращает все шаблоны форм из базы"""
    db_forms = []
    for form in forms_collection.find():
        form.pop('_id')
        db_forms.append(form)
    return db_forms


CLIENT_DATE_PATTERNS = ('%d.%m.%Y', '%Y-%m-%d')


def validate_date(date: str) -> bool:
    """Функция валидирует дату, формат даты DD.MM.YYYY или YYYY-MM-DD"""
    pattern = r'(\d{2}.\d{2}.\d{4}\b)|(\d{4}-\d{2}-\d{2}\b)'
    match = re.match(pattern, date)
    if match:
        for k, match_obj in enumerate(match.groups()):
            if match_obj:
                client_date_pattern = CLIENT_DATE_PATTERNS[k]
                try:
                    time.strptime(date, client_date_pattern)
                    return True
                except ValueError:
                    return False
    return False


def validate_email(email: str) -> bool:
    """Функция валидирует email"""
    pattern = r'\w{4,20}@\w{3,20}\.((com)|(ru))\b'
    return True if re.match(pattern, email) else False


def validate_phone(phone: str) -> bool:
    """Функция валидирует номер телефона"""
    pattern = r'\+7\d{10}\b'
    return True if re.match(pattern, phone) else False


FIELDS_FOR_VALIDATE = {'date': validate_date,
                       'email': validate_email,
                       'phone': validate_phone,
                       }


def is_valid_field(db_form_field_value: str, form_field_value: str) -> bool:
    """Функция валидирует поле формы клиента"""
    return True if db_form_field_value == 'text' else FIELDS_FOR_VALIDATE[db_form_field_value](form_field_value)


def define_field_type(field: str) -> str:
    """Функция определяет тип поля формы клиента"""
    for field_type, validate_field_func in FIELDS_FOR_VALIDATE.items():
        if validate_field_func(field):
            return field_type
    return 'text'


def get_client_form(form: dict) -> dict:
    """Если шаблон формы в базе не найден, функция генерирует новый шаблон"""
    client_form = {}
    for form_field_key, form_key_value in form.items():
        client_form[form_field_key] = define_field_type(form_key_value)
    return client_form


def compare_forms(db_form: dict, form: dict) -> bool:
    """Функция сравнивает форму клиента с шаблоном формы из базы,
    возвращает True, если форма совпадает с шаблоном, False, если нет"""
    for db_form_field_key, db_form_field_type in db_form.items():
        if db_form_field_key in form:
            if is_valid_field(db_form_field_type, form[db_form_field_key]):
                continue
        return False
    return True


def find_form(form: dict) -> dict:
    """Функция перребирает все формы из базы данных,
       сравнивает с формой от клиента, возвращает первое совпадение,
       если совпадений нет, возвращает шаблон формы, которую прислал клиент"""
    db_forms = get_forms_from_db()
    for db_form in db_forms:
        if compare_forms(db_form['form'], form):
            return {'form_name': db_form['form_name']}
    return {'unknown_form': get_client_form(form)}
