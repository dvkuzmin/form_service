import os
import json

from flask import Flask, request

from repository import client
from service import find_form

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

app = Flask(__name__, root_path=BASE_DIR)

db = client['my_database']

forms_collection = db['forms_collection']


@app.route('/get_form', methods=['POST'])
def get_form():
    form = json.loads(request.data.decode())
    db_form = find_form(form)

    return db_form
