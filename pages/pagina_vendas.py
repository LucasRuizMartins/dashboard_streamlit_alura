import pandas as pd 
import streamlit as st 
import requests
import plotly.express as px
from src import funcoes
from src import graficos
from src import receitas
from src import api
from src import environ


st.title('Dashboard de vendas')# :shopping_cart:')

st.sidebar.title('Filtros')
regiao = st.sidebar.selectbox('Região',environ.REGIOES)

if regiao == "Brasil":
    regiao = ''

todos_anos = st.sidebar.checkbox('Dados de todo o periodo', value='True')

if todos_anos:
    ano = ''
else:
    ano = st.sidebar.slider('Ano',2020,2023)

query_string = {
    'regiao':regiao.lower(),
    'ano':ano
    }


dados = api.get_base(query_string)

filtro_vendedores = st.sidebar.multiselect('Vendedores', dados['Vendedor'].unique())
if filtro_vendedores:
    dados = dados[dados['Vendedor'].isin(filtro_vendedores)]






#GUI

aba_1,aba_2,aba_3 = st.tabs(['Receita','Quantidade de vendas','Vendedores'])
with aba_1:
    receita_estados = receitas.por_estados(dados,'sum')
    receita_mensal = receitas.por_mes(dados,'sum')
    receita_categorias = receitas.por_categoria(dados)

    col_1,col_2 = st.columns(2)

    with col_1:
        #Graficos
        fig_mapa_receita       = graficos.mapa(receita_estados)
        fig_receita_categorias = graficos.receita_categoria(receita_categorias)
        
        
        st.metric(label='total',value= funcoes.formata_numero(dados['Preço'].sum(),'R$' ))
        st.plotly_chart(fig_mapa_receita,use_container_width=True)
        st.plotly_chart(fig_receita_categorias,use_container_width=True)
    with col_2:
        #Graficos        
        fig_receita_mensal     = graficos.receita_mensal(receita_mensal)
        fig_receita_estado     = graficos.receita_estado(receita_estados)
        
        st.metric(label='Quantidade de vendas',value= funcoes.formata_numero(dados.shape[0]))
        st.plotly_chart(fig_receita_mensal,use_container_width=True)
        st.plotly_chart(fig_receita_estado,use_container_width=True)


with aba_2:    
    #st.dataframe(contagem_vendas_estados)
    
    receita_mensal = receitas.por_mes(dados,'count')
    contagem_vendas_estados = receitas.por_estados(dados,'count')
    
    
    col_1,col_2 = st.columns(2)
    with col_1:
        fig_mapa_vendas       = graficos.mapa(contagem_vendas_estados)
        st.metric(label='total',value= funcoes.formata_numero(dados['Preço'].sum(),'R$' ))
        st.plotly_chart(fig_mapa_vendas,use_container_width=True)
        
    with col_2:
        fig_vendas_estado     = graficos.receita_estado(contagem_vendas_estados)
        fig_qtd_mensal = graficos.receita_mensal(receita_mensal)
        st.metric(label='Quantidade de vendas',value= funcoes.formata_numero(dados.shape[0]))
        st.plotly_chart(fig_vendas_estado,use_container_width=True)
        
    st.plotly_chart(fig_qtd_mensal,use_container_width=True)

with aba_3:
    qtd_vendedores = st.number_input('quantidade de vendedores',2,10,5)
    
    
    receita_vendedores = receitas.por_vendedores(dados)       
    fig_receita_vendedores = graficos.receita_vendedores(receita_vendedores,qtd_vendedores,'sum')
    fig_vendas_vendedores = graficos.receita_vendedores(receita_vendedores,qtd_vendedores,'count')
    
    col_1,col_2 = st.columns(2)
    with col_1:
        st.metric(label='total',value= funcoes.formata_numero(dados['Preço'].sum(),'R$' ))
        st.plotly_chart(fig_receita_vendedores,use_container_width=True)
    with col_2:
        st.metric(label='Quantidade de vendas',value= funcoes.formata_numero(dados.shape[0]))
        st.plotly_chart(fig_vendas_vendedores,use_container_width=True)