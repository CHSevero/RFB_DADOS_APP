import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import streamlit as st


st.cache_resource
def get_connection():
    print('get_connection')
    load_dotenv()
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
    )


def get_engine():
    print('get_engine')
    return create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")