import streamlit as st 


st.set_page_config(layout='wide')

pagina_dashboard = st.Page(
    "pages/pagina_vendas.py", 
    title="Dashboard de Vendas", 
    icon="🛒", 
    default=True
)


pagina_dados = st.Page(
    "pages/pagina_dados.py", 
    title="Dashboard de Vendas", 
    icon="📊"
)

pg = st.navigation([pagina_dashboard, pagina_dados])


pg.run()
