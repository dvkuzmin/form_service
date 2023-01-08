import random
import json

import requests


FIRST_FORM = {'user_name': 'vasya',
              'user_email': 'vasya@gmail.com',
              'user_phone': '+79101234560',
              'user_extra_field': '+79154321293'}


SECOND_FORM = {'client_name': 'petya',
               'client_birthday': '2000-07-15',
               'client_phone': '+79101234560'}


THIRD_FORM = {'customer_name': 'vanya',
              'order_date': '2000-07-15',
              'customer_email': 'vanya@mail.ru'}


INVALID_FORM_1 = {'name': 'vanya',
                  'order_date': '2000-07-15',
                  'user_email': 'vanya@mail.ru111'}


INVALID_FORM_2 = {'client_name': 'vanya',
                  'client_birthday': '2000-07-151',
                  'user_email': 'vanya@mail.ru'}


INVALID_FORM_3 = {'user_name': 'vanya',
                  'order_date': '2000-07-151',
                  'customer_email': 'vanya@mail.ru'}

FORMS = (FIRST_FORM,
         SECOND_FORM,
         THIRD_FORM,
         INVALID_FORM_1,
         INVALID_FORM_2,
         INVALID_FORM_3)


def make_request():
    form = random.choice(FORMS)
    print(form)
    res = requests.post('http://127.0.0.1:5000/get_form', data=json.dumps(form))
    print(res.text)


if __name__ == '__main__':
    make_request()
