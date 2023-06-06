"""
MIT License

Copyright (c) 2021 Aphonso Henrique

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import wget
import zipfile
import os
from helpers import get_connection, get_engine
import pandas as pd
import sys
import gc


base_url = 'https://dadosabertos.rfb.gov.br/CNPJ/'
base_path = '/tmp/'
files = [
    'Cnaes', 
    'Empresas0', 'Empresas1','Empresas2','Empresas3', 'Empresas4', 
    'Empresas5', 'Empresas6','Empresas7', 'Empresas8','Empresas9', 
    'Estabelecimentos0', 'Estabelecimentos1', 'Estabelecimentos2', 
    'Estabelecimentos3', 'Estabelecimentos4', 'Estabelecimentos5', 
    'Estabelecimentos6', 'Estabelecimentos7', 'Estabelecimentos8', 
    'Estabelecimentos9', 
    'Motivos',
    'Municipios','Naturezas', 'Paises', 'Qualificacoes',
    'Simples', 
    'Socios0', 'Socios1', 'Socios2', 'Socios3',
    'Socios4', 'Socios5', 'Socios6', 'Socios7', 'Socios8',
    'Socios9'
]


def download(url, path):
    print('download')
    wget.download(url, path)
    print()


def dowload_files():
    print('dowload_files')
    for file in files:
        download(base_url + file + '.zip', base_path + file)
    

def extract_files():
    print('extract_files')
    for file in files:
        with zipfile.ZipFile(base_path + file, 'r') as zip_ref:
            zip_ref.extractall(base_path)


def to_sql(dataframe, **kwargs):
    print('to_sql')
    size = 4096
    total = len(dataframe)
    name = kwargs.get('name')

    def chunker(df):
        return (df[i:i + size] for i in range(0, len(df), size))

    for i, df in enumerate(chunker(dataframe)):
        df.to_sql(**kwargs)
        index = i * size
        percent = (index * 100) / total
        progress = f'{name} {percent:.2f}% {index:0{len(str(total))}}/{total}'
        sys.stdout.write(f'\r{progress}')
    print()


def populate_empresas(conn, engine):
    print('populate_empresa')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS "empresa";')
    conn.commit()
    count = 0
    count = 0
    chunksize = 10 ** 6
    for file in os.listdir(base_path):
        if file.endswith('EMPRECSV'):
            print(file, count)
            for df in pd.read_csv(
                filepath_or_buffer=base_path + file,
                sep=';',
                skiprows=0,
                dtype='object',
                encoding='latin-1',
                chunksize=chunksize
            ):
                df.reset_index(inplace=True)
                del df['index']
                df.columns = ['cnpj_basico', 'razao_social', 'natureza_juridica', 'qualificacao_responsavel', 'capital_social', 'porte_empresa', 'ente_federativo_responsavel']
                df['capital_social'] = df['capital_social'].apply(lambda x: x.replace(',','.'))
                df['capital_social'] = df['capital_social'].astype(float)
                to_sql(df, name='empresa', con=engine, if_exists='append', index=False)
            count += 1


def populate_estabelecimento(conn, engine, end, name, columns):
    print('populate_table')
    cur = conn.cursor()
    cur.execute(f'DROP TABLE IF EXISTS "{name}";')
    conn.commit()
    count = 0
    chunksize = 10 ** 6
    for file in os.listdir(base_path):
        if file.endswith(end):
            print(file, count)
            for df in pd.read_csv(
                filepath_or_buffer=base_path + file,
                sep=';',
                skiprows=0,
                dtype='object',
                encoding='latin-1',
                chunksize=chunksize
            ):
                df.reset_index(inplace=True)
                del df['index']
                df.columns = columns
                df['ano_inicio_atividade'] = df['data_inicio_atividade'].apply(lambda x: x[:4])
                to_sql(df, name=name, con=engine, if_exists='append', index=False)
            count += 1


def populate_table(conn, engine, end, name, columns):
    print('populate_table')
    cur = conn.cursor()
    cur.execute(f'DROP TABLE IF EXISTS "{name}";')
    conn.commit()
    count = 0
    chunksize = 10 ** 6
    for file in os.listdir(base_path):
        if file.endswith(end):
            print(file, count)
            for df in pd.read_csv(
                filepath_or_buffer=base_path + file,
                sep=';',
                skiprows=0,
                dtype='object',
                encoding='latin-1',
                chunksize=chunksize
            ):
                df.reset_index(inplace=True)
                del df['index']
                df.columns = columns
                to_sql(df, name=name, con=engine, if_exists='append', index=False)
            count += 1



if __name__ == '__main__':
    dowload_files()
    extract_files()
    conn = get_connection()
    engine = get_engine()

    populate_empresas(conn, engine)

    end = 'ESTABELE'
    name = 'estabelecimento'
    columns = ['cnpj_basico', 'cnpj_ordem', 'cnpj_dv', 'identificador_matriz_filial', 'nome_fantasia', 'situacao_cadastral', 'data_situacao_cadastral',
    'motivo_situacao_cadastral', 'nome_cidade_exterior', 'pais', 'data_inicio_atividade', 'cnae_fiscal_principal', 'cnae_fiscal_secundaria', 'tipo_logradouro',
    'logradouro', 'numero', 'complemento', 'bairro', 'cep', 'uf', 'municipio', 'ddd_1', 'telefone_1', 'ddd_2', 'telefone_2', 'ddd_fax', 'fax', 
    'correio_eletronico', 'situacao_especial', 'data_situacao_especial']
    populate_estabelecimento(conn, engine, end, name, columns)

    end = 'SOCIOCSV'
    name = 'socios'
    columns = [
        'cnpj_basico', 'identificador_socio', 'nome_socio_razao_social',
        'cpf_cnpj_socio', 'qualificacao_socio', 'data_entrada_sociedade',
        'pais', 'representante_legal', 'nome_do_representante',
        'qualificacao_representante_legal', 'faixa_etaria']
    populate_table(conn, engine, end, name, columns)

    end = 'D30513'
    name = 'simples'
    columns = [
        'cnpj_basico', 'opcao_pelo_simples', 'data_opcao_simples',
        'data_exclusao_simples', 'opcao_mei', 'data_opcao_mei',
        'data_exclusao_mei'
    ]
    populate_table(conn, engine, end, name, columns)

    end = 'CNAECSV'
    name = 'cnae'
    columns = ['codigo', 'descricao']
    populate_table(conn, engine, end, name, columns)

    end = 'MOTICSV'
    name = 'moti'
    columns = ['codigo', 'descricao']
    populate_table(conn, engine, end, name, columns)

    end = 'MUNICCSV'
    name = 'munic'
    columns = ['codigo', 'descricao']
    populate_table(conn, engine, end, name, columns)

    end = 'NATJUCSV'
    name = 'natju'
    columns = ['codigo', 'descricao']
    populate_table(conn, engine, end, name, columns)

    end = 'PAISCSV'
    name = 'pais'
    columns = ['codigo', 'descricao']
    populate_table(conn, engine, end, name, columns)
