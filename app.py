from flask import Flask, g
from sqlmodel import SQLModel, Session
from settings import ALL_APPS, DATABASE
from models import *

app = Flask(__name__)

@app.route('/')
def root_url():
    return ('<h1>Добро пожаловать на главную страницу!</h1><br>'
            '<a href="/adverts">Список объявлений</a>')

@app.before_request
def create_session():
    g.session = Session(DATABASE)

@app.after_request
def close_session(response):
    g.session.close()
    return response

for view in ALL_APPS:
    app.add_url_rule(view.url_prefix,
                     view_func=view.GroupAPI.as_view(view.url_prefix, view))
    app.add_url_rule(f'{view.url_prefix}/<int:pk>',
                     view_func=view.ItemAPI.as_view(f'{view.url_prefix}_item', view))

if __name__ == "app":
    SQLModel.metadata.create_all(DATABASE)