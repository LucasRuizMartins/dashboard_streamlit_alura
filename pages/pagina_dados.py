import streamlit as st
import pandas as pd
from src import api
from src import funcoes

st.title('DADOS BRUTOS')

query_string = {
    'regiao':'',
    'ano':''
    }

dados = api.get_base(query_string)


with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas',list(dados.columns),list(dados.columns))
    
    
st.sidebar.title('Filtros')

with st.sidebar.expander('Nome Produto'):
    produtos = st.multiselect('Selecione os produtos',
                                      list(dados['Produto'].unique()),
                                      list(dados['Produto'].unique()))

with st.sidebar.expander('Preço do produto'):
    maior = dados['Preço'].max()
    menor = dados['Preço'].min()
    preco = st.slider('Faixa de Preço', menor, maior, (menor, maior))

with st.sidebar.expander('Data'):
    data_compra = st.date_input('Selecione a data',
                                  (dados['Data da Compra'].min(),
                                  dados['Data da Compra'].max()))

with st.sidebar.expander('Categoria'):
    categorias = st.multiselect('Selecione a categoria',
                                  list(dados['Categoria do Produto'].unique()),
                                  list(dados['Categoria do Produto'].unique()))

with st.sidebar.expander('UF'):
    locais = st.multiselect('Selecione o local da compra',
                                  list(dados['Local da compra'].unique()),
                                  list(dados['Local da compra'].unique()))
  
with st.sidebar.expander('Tipo pagamento'):
    pagamentos = st.multiselect('Selecione o tipo de pagamento',
                                  list(dados['Tipo de pagamento'].unique()),
                                  list(dados['Tipo de pagamento'].unique()))  


query = '''
`Produto` in @produtos and \
@preco[0] <= `Preço` and  `Preço`  <= @preco[1] and \
@data_compra[0] <= `Data da Compra` and  `Data da Compra` <= @data_compra[1] 
'''


dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]
    
st.dataframe(dados_filtrados)

st.markdown(f' a tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas')


st.markdown('escreva um nome para o arquivo')

coluna_1, coluna_2 = st.columns(2)

with coluna_1:
    nome_arquivo = st.text_input('', label_visibility='collapsed', value='dados')
    nome_arquivo += '.csv'
with coluna_2:
    st.download_button('fazer download em csv', 
                       data = funcoes.converter_csv(dados_filtrados),
                       file_name=nome_arquivo,
                       mime='text/csv',
                       on_click=funcoes.mensagem_sucesso)