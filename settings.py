from dotenv import find_dotenv, load_dotenv
import os
from sqlalchemy import create_engine
from viewsets import ViewSet
from advertisement.views import *
from user.views import *


env_file = find_dotenv(".env")
if env_file != '':
    load_dotenv(env_file)
 
DATABASE = create_engine(f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:'
        f'{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:'
        f'{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}') 

ALL_APPS = [
    ViewSet('/adverts', list_func = adverts_list, post_func = adverts_post,
            retrieve_func = adverts_retrieve, patch_func = adverts_patch,
            delete_func = adverts_delete),
        
    ViewSet('/users', list_func = user_list, post_func = user_post,
            retrieve_func = user_retrieve, delete_func = user_delete),
]