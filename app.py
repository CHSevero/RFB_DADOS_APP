import streamlit as st
import pandas as pd
from helpers import get_connection
from queries import (
  run_query,
  year_chart,
  state_chart,
  first_query_year,
  first_query_state,
  second_query_year,
  second_query_state,
  third_query_year,
  third_query_state,
  fourth_query_year,
  fourth_query_state,
  fifth_query_year,
  fifth_query_state,
  sixth_query_year,
  sixth_query_state
)
import altair as alt


conn = get_connection()
cur = conn.cursor()

st.set_page_config(layout="wide")
st.markdown('# RFB CNPJ APP')

st.markdown('# Consultas')
col1, col2 = st.columns(2)

start = col1.slider('Inicio', min_value=1960, max_value=2023, value=2022, key='fq1.1')
end = col2.slider('Fim', min_value=1960, max_value=2023, value=2023, key='fq1.2')
if start > end:
  st.error('Inicio está maior que o fim.', icon="🚨")
else:
  col1.markdown('## Agrupamento por ano')
  col2.markdown('## Agrupamento por estado')
  @st.cache_data
  def get_first_query_year(start, end):
    return first_query_year(cur, start, end)
  chart = year_chart('Número de empresas abertas', get_first_query_year(start, end))
  col1.altair_chart(chart, use_container_width=True)
  @st.cache_data
  def get_first_query_state(start, end):
    return first_query_state(cur, start, end)
  chart = state_chart('Número de empresas abertas', get_first_query_state(start, end))
  col2.altair_chart(chart, use_container_width=True)


  @st.cache_data
  def get_second_query_year(start, end):
    return second_query_year(cur, start, end)
  chart = year_chart('Número de empresas abertas: Simples Nacional', get_second_query_year(start, end))
  col1.altair_chart(chart, use_container_width=True)
  @st.cache_data
  def get_second_query_state(start, end):
    return second_query_state(cur, start, end)
  chart = state_chart('Número de empresas abertas: Simples Nacional', get_second_query_state(start, end),)
  col2.altair_chart(chart, use_container_width=True)


  @st.cache_data
  def get_third_query_year(start, end):
    return third_query_year(cur, start, end)
  chart = year_chart('Número de empresas abertas: MEI', get_third_query_year(start, end))
  col1.altair_chart(chart, use_container_width=True)
  @st.cache_data
  def get_third_query_state(start, end):
    return third_query_state(cur, start, end)
  chart = state_chart('Número de empresas abertas: MEI', get_third_query_state(start, end))
  col2.altair_chart(chart, use_container_width=True)

  @st.cache_data
  def get_fourth_query_year(start, end):
   return fourth_query_year(cur, start, end)
  chart = year_chart('Número de empresas de desenvolvimento de software abertas', get_fourth_query_year(start, end))
  col1.altair_chart(chart, use_container_width=True)
  @st.cache_data
  def get_fourth_query_state(start, end):
    return fourth_query_state(cur, start, end)
  chart = state_chart('Número de empresas de desenvolvimento de software abertas', get_fourth_query_state(start, end))
  col2.altair_chart(chart, use_container_width=True)


  @st.cache_data
  def get_fifth_query_year(start, end):
    return fifth_query_year(cur, start, end)
  chart = year_chart('Número de empresas de desenvolvimento de software abertas: Simples Nacional', get_fifth_query_year(start, end)) 
  col1.altair_chart(chart, use_container_width=True)

  @st.cache_data
  def get_fifth_query_state(start, end):
    return fifth_query_state(cur, start, end)
  chart = state_chart('Número de empresas de desenvolvimento de software abertas: Simples Nacional', get_fifth_query_state(start, end))
  col2.altair_chart(chart, use_container_width=True)


  @st.cache_data
  def get_sixth_query_year(start, end):
    return sixth_query_year(cur, start, end)
  chart = year_chart('Número de empresas de  manutenção de computadores: MEI', get_fifth_query_year(start, end))
  col1.altair_chart(chart, use_container_width=True)

  @st.cache_data
  def get_sixth_query_state(start, end):
    return sixth_query_state(cur, start, end)
  chart = state_chart('Número de empresas de  manutenção de computadores: MEI', get_sixth_query_state(start, end))
  col2.altair_chart(chart, use_container_width=True)