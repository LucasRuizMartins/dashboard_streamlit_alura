import plotly.express as px


def mapa(df):
    fig = px.scatter_geo(df,
                        lat='lat',
                        lon='lon',
                        scope='south america',
                        size='Preço',
                        template='seaborn',
                        hover_name='Local da compra',
                        hover_data = {'lat':False,'lon':False},
                        title="Receita por estado")
    
    # --- INÍCIO DA PERSONALIZAÇÃO PARA FUNDO TRANSPARENTE ---
    fig.update_layout(
        # Define a cor de fundo do papel (área ao redor do gráfico) como transparente
        paper_bgcolor='rgba(0,0,0,0)',
        # Define a cor de fundo do próprio gráfico (área do mapa) como transparente
        plot_bgcolor='rgba(0,0,0,0)',        
        # Opcional: Ajustar a cor do texto do título para que ele apareça em temas escuros
        # title_font_color="white", # Descomente se o seu tema for escuro
    )
    
    # Adicional para scatter_geo: Garantir que o próprio oceano/fundo geográfico não seja branco
    fig.update_geos(
        bgcolor='rgba(0,0,0,0)', # Fundo geográfico transparente
        showocean=True, # Mostrar oceano
        oceancolor='rgba(0,0,0,0)', # Cor do oceano transparente
        showlakes=True, # Mostrar lagos
        lakecolor='rgba(0,0,0,0)', # Cor dos lagos transparente
        showrivers=True, # Mostrar rios
        rivercolor='rgba(0,0,0,0)' # Cor dos rios transparente
    )
    # --- FIM DA PERSONALIZAÇÃO ---
    
    return fig



def receita_mensal(df):
    fig = px.line(df,
                x='Mes',
                y='Preço',
                markers=True,
                range_y=(0,df.max()),
                color='Ano',
                line_dash='Ano',
                title = 'Receita mensal'
                )
    fig.update_layout(yaxis_title='Receita')
    return fig


def receita_estado(df):
    fig = px.bar(df.head(5),
                 x='Local da compra',
                 y='Preço',
                 text_auto = True,
                 title='Top 5 estados (receita)'
                 )
    
    fig.update_layout(yaxis_title='Receita')
    return fig

def receita_categoria(df):
    fig = px.bar(df.head(5),
                 text_auto = True,
                 title='Receita por categoria'
                 )
    
    fig.update_layout(yaxis_title='Receita')
    return fig



def receita_vendedores(df,qtd,operacao):
    titulo = f'top {qtd} vendedores receita' if operacao == 'sum' else f'top {qtd} numero de vendas'
    
    df_vendedores = df[[operacao]].sort_values(by=operacao, ascending=False).head(qtd)
    
    fig = px.bar(df_vendedores,
                 x=operacao,
                 y=df_vendedores.index,
                 text_auto = True,
                 title= titulo
                 )
    
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig