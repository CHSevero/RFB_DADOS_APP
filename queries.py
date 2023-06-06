import pandas as pd
import altair as alt


def run_query(cur, query):
    print('run_query')
    cur.execute(query)
    tmp = cur.fetchall()
    columns = [row[0] for row in cur.description]
    return pd.DataFrame(tmp, columns=columns)


def year_chart(title, df):
    return alt.Chart(df, title=title).mark_bar().encode(x='ano', y='quantidade')


def state_chart(title, df):
    return alt.Chart(df, title=title).mark_bar().encode(x=alt.X('estado', sort='y'), y='quantidade')


def first_query_year(cur, start, end):
    query = f"""
    SELECT ano_inicio_atividade as ano, count(data_inicio_atividade) as quantidade
    FROM estabelecimento E
    INNER JOIN cnae C
    ON E.cnae_fiscal_principal = C.codigo
    WHERE ano_inicio_atividade BETWEEN '{start}' AND '{end}'
    GROUP BY 1;
    """
    return run_query(cur, query)


def first_query_state(cur, start, end):
    query = f"""
    SELECT E.uf as estado, count(E.cnpj_basico) as quantidade
    FROM estabelecimento E
    INNER JOIN cnae C ON E.cnae_fiscal_principal = C.codigo
    INNER JOIN pais on pais.codigo = E.pais
    WHERE ano_inicio_atividade BETWEEN '{start}' AND '{end}'
      AND pais.descricao = 'BRASIL'
    GROUP BY 1
    ORDER BY 2 ASC;
    """
    return run_query(cur, query)


def second_query_year(cur, start, end):
    query = f"""
    SELECT ano_inicio_atividade as ano, count(data_inicio_atividade) as quantidade
    FROM estabelecimento ES
    INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
    INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
    WHERE SI.opcao_pelo_simples = 'S' AND ano_inicio_atividade BETWEEN '{start}' AND '{end}'
    GROUP BY 1;
    """
    return run_query(cur, query)


def second_query_state(cur, start, end):
    query = f"""
    SELECT ES.uf as estado, count(ES.cnpj_basico) as quantidade
    FROM estabelecimento ES
    INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
    INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
    INNER JOIN pais on pais.codigo = ES.pais
    WHERE ano_inicio_atividade BETWEEN '{start}' AND '{end}'
      AND pais.descricao = 'BRASIL'
    GROUP BY 1
    ORDER BY 2 ASC;
    """
    return run_query(cur, query)


def third_query_year(cur, start, end):
    query = f"""
    SELECT ano_inicio_atividade as ano, count(data_inicio_atividade) as quantidade
    FROM estabelecimento ES
    INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
    INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
    WHERE SI.opcao_mei = 'S' AND ano_inicio_atividade BETWEEN '{start}' AND '{end}'
    GROUP BY 1;
    """
    return run_query(cur, query)


def third_query_state(cur, start, end):
    query = f"""
    SELECT ES.uf as estado, count(ES.cnpj_basico) as quantidade
    FROM estabelecimento ES
    INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
    INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
    INNER JOIN pais on pais.codigo = ES.pais
    WHERE ano_inicio_atividade BETWEEN '{start}' AND '{end}'
      AND pais.descricao = 'BRASIL'
    GROUP BY 1
    ORDER BY 2 ASC;
    """
    return run_query(cur, query)


def fourth_query_year(cur, start, end):
    query = f"""
    SELECT ano_inicio_atividade as ano, count(data_inicio_atividade) as quantidade
    FROM estabelecimento E
    INNER JOIN cnae C
    ON E.cnae_fiscal_principal = C.codigo
    WHERE ano_inicio_atividade BETWEEN '{start}' AND '{end}'
        AND C.codigo IN ('6201500', '6201501', '6202300', '6203100', '6204000', '6209100')
    GROUP BY 1
    ORDER BY 1;
    """
    return run_query(cur, query)


def fourth_query_state(cur, start, end):
    query = f"""
    SELECT E.uf as estado, count(E.cnpj_basico) as quantidade
    FROM estabelecimento E
    INNER JOIN cnae C ON E.cnae_fiscal_principal = C.codigo
    INNER JOIN pais on pais.codigo = E.pais
    WHERE ano_inicio_atividade BETWEEN '{start}' AND '{end}'
        AND C.codigo IN ('6201500', '6201501', '6202300', '6203100', '6204000', '6209100')
        AND pais.descricao = 'BRASIL'
    GROUP BY 1
    ORDER BY 2 ASC;
    """
    return run_query(cur, query)


def fifth_query_year(cur, start, end):
    query = f"""
    SELECT ano_inicio_atividade as ano, count(data_inicio_atividade) as quantidade
    FROM estabelecimento ES
    INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
    INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
    INNER JOIN cnae CN ON ES.cnae_fiscal_principal = CN.codigo
    WHERE SI.opcao_pelo_simples = 'S' 
        AND ano_inicio_atividade BETWEEN '{start}' AND '{end}'
        AND CN.codigo IN ('6201500', '6201501', '6202300', '6203100', '6204000', '6209100')
    GROUP BY 1
    ORDER BY 1;
    """
    return run_query(cur, query)


def fifth_query_state(cur, start, end):
    query = f"""
    SELECT ES.uf as estado, count(ES.cnpj_basico) as quantidade
    FROM estabelecimento ES
    INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
    INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
    INNER JOIN cnae CN ON ES.cnae_fiscal_principal = CN.codigo
    INNER JOIN pais on pais.codigo = ES.pais
    WHERE SI.opcao_pelo_simples = 'S' 
      AND ano_inicio_atividade BETWEEN '{start}' AND '{end}'
      AND CN.codigo IN ('6201500', '6201501', '6202300', '6203100', '6204000', '6209100')
      AND pais.descricao = 'BRASIL'
    GROUP BY 1
    ORDER BY 2 ASC;
    """
    return run_query(cur, query)


def sixth_query_year(cur, start, end):
    query = f"""
    SELECT ano_inicio_atividade as ano, count(data_inicio_atividade) as quantidade
    FROM estabelecimento ES
    INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
    INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
    INNER JOIN cnae CN ON ES.cnae_fiscal_principal = CN.codigo
    WHERE SI.opcao_mei = 'S' 
        AND ano_inicio_atividade BETWEEN '{start}' AND '{end}'
        AND CN.codigo IN ('6201500', '6201501', '6202300', '6203100', '6204000', '6209100', '9511800')
    GROUP BY 1;
    """
    return run_query(cur, query)


def sixth_query_year(cur, start, end):
    query = f"""
    SELECT ano_inicio_atividade as ano, count(data_inicio_atividade) as quantidade
    FROM estabelecimento ES
    INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
    INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
    INNER JOIN cnae CN ON ES.cnae_fiscal_principal = CN.codigo
    WHERE SI.opcao_mei = 'S' 
        AND ano_inicio_atividade BETWEEN '{start}' AND '{end}'
        AND CN.codigo IN ('6201500', '6201501', '6202300', '6203100', '6204000', '6209100', '9511800')
    GROUP BY 1;
    """
    return run_query(cur, query)

def sixth_query_state(cur, start, end):
    query = f"""
    SELECT ES.uf as estado, count(ES.cnpj_basico) as quantidade
    FROM estabelecimento ES
    INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
    INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
    INNER JOIN cnae CN ON ES.cnae_fiscal_principal = CN.codigo
    WHERE SI.opcao_mei = 'S' 
      AND ano_inicio_atividade BETWEEN '{start}' AND '{end}'
      AND CN.codigo IN ('6201500', '6201501', '6202300', '6203100', '6204000', '6209100', '9511800')
    GROUP BY 1
    ORDER BY 2 ASC;
    """
    return run_query(cur, query)
