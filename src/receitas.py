import pandas as pd 

def por_estados(df,func):
    receita_estados = df.groupby('Local da compra')[['Preço']].agg(func)#.sum()
   
    receita_estados = df.drop_duplicates(
        subset='Local da compra')[['Local da compra','lat','lon']].merge(
        receita_estados,left_on='Local da compra',
        right_index=True
    ).sort_values('Preço',ascending=False)
    return receita_estados


def por_mes(df,func):
    receita_mensal = df.set_index('Data da Compra').groupby(pd.Grouper(freq='ME'))['Preço'].agg(func).reset_index()
    receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
    receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name()
    return receita_mensal


def por_categoria(df):
    receita_categoria =  df.groupby('Categoria do Produto')[['Preço']].sum().sort_values(by="Preço", ascending=False)
    return receita_categoria
    
    

def por_vendedores(df):
    receita_vendedores =  df.groupby('Vendedor')[['Preço']].agg(['sum','count'])
    receita_vendedores.columns = receita_vendedores.columns.get_level_values(1)
    
    return receita_vendedores
 
 
 
#  vendas_estados = pd.DataFrame(dados.groupby('Local da compra')['Preço'].count())
# vendas_estados = dados.drop_duplicates(
#     subset = 'Local da compra')[['Local da compra','lat', 'lon']].merge(
#         vendas_estados, left_on = 'Local da compra', right_index = True).sort_values('Preço', ascending = False)