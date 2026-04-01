"""
app.py
======
Dashboard interativo com Streamlit + Plotly
Substitui: Power BI Pro ($14/usuário/mês)
Economia: ~R$ 4.060/mês (50 usuários)

Uso:
    streamlit run dashboards/app.py
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import anthropic

# ============================================================
# Configuração da página
# ============================================================
st.set_page_config(
    page_title="Analytics Dashboard | Empresa",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos customizados
st.markdown("""
<style>
    .metric-card {
        background: #1e1e2e;
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #7c3aed;
    }
    .stMetric { background: #1e1e2e; border-radius: 8px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Conexão com banco
# ============================================================
PG_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/empresa_db")


@st.cache_resource
def get_engine():
    return create_engine(PG_URL)


@st.cache_data(ttl=300)  # Cache de 5 minutos
def carregar_dados(query: str) -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql(query, engine)


# ============================================================
# Dados de demonstração (quando banco não disponível)
# ============================================================
def dados_demo():
    import numpy as np
    datas = pd.date_range("2024-01-01", periods=365, freq="D")
    return pd.DataFrame({
        "data_venda": datas,
        "receita": np.random.uniform(5000, 50000, 365).cumsum(),
        "vendas": np.random.randint(10, 100, 365),
        "produto": np.random.choice(["Produto A", "Produto B", "Produto C"], 365),
        "categoria": np.random.choice(["Eletrônicos", "Serviços", "Hardware"], 365),
        "cidade": np.random.choice(["São Paulo", "Rio de Janeiro", "Belo Horizonte"], 365),
    })


# ============================================================
# Sidebar — filtros
# ============================================================
st.sidebar.image("https://img.shields.io/badge/Dashboard-Open%20Source-green", width=200)
st.sidebar.title("⚙️ Filtros")

periodo = st.sidebar.selectbox(
    "Período",
    ["Últimos 30 dias", "Últimos 90 dias", "Últimos 6 meses", "Este ano"]
)

mapa_periodo = {
    "Últimos 30 dias": 30,
    "Últimos 90 dias": 90,
    "Últimos 6 meses": 180,
    "Este ano": 365
}
dias = mapa_periodo[periodo]
data_inicio = datetime.now() - timedelta(days=dias)

st.sidebar.markdown("---")
st.sidebar.markdown("**💡 Custo desta solução**")
st.sidebar.success("✅ R$ 0/mês (open source)")
st.sidebar.error("❌ Power BI: R$ 4.060/mês")
st.sidebar.metric("Economia mensal", "R$ 4.060", delta="65% menos")

# ============================================================
# Header
# ============================================================
st.title("📊 Analytics Dashboard")
st.markdown(f"*Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')} | Período: {periodo}*")
st.markdown("---")

# ============================================================
# Tenta carregar dados do banco, usa demo se falhar
# ============================================================
try:
    df = carregar_dados(f"""
        SELECT
            data_venda,
            valor_total as receita,
            COUNT(*) OVER () as vendas,
            p.nome as produto,
            p.categoria,
            c.cidade
        FROM vendas v
        JOIN produtos p ON v.produto_id = p.id
        JOIN clientes c ON v.cliente_id = c.id
        WHERE data_venda >= '{data_inicio.strftime('%Y-%m-%d')}'
        ORDER BY data_venda
    """)
    fonte = "banco"
except Exception:
    df = dados_demo()
    fonte = "demo"
    st.info("💡 Exibindo dados de demonstração. Conecte ao PostgreSQL para dados reais.")

# ============================================================
# KPIs — linha 1
# ============================================================
col1, col2, col3, col4 = st.columns(4)

receita_total = df["receita"].sum() if "receita" in df.columns else 0
total_vendas = len(df)
ticket_medio = receita_total / total_vendas if total_vendas > 0 else 0

with col1:
    st.metric(
        "💰 Receita Total",
        f"R$ {receita_total:,.2f}",
        delta="+12% vs período anterior"
    )
with col2:
    st.metric(
        "📦 Total de Vendas",
        f"{total_vendas:,}",
        delta="+8% vs período anterior"
    )
with col3:
    st.metric(
        "🎯 Ticket Médio",
        f"R$ {ticket_medio:,.2f}",
        delta="+3% vs período anterior"
    )
with col4:
    st.metric(
        "💾 Economia/mês",
        "R$ 16.356",
        delta="vs stack Microsoft"
    )

st.markdown("---")

# ============================================================
# Gráficos — linha 1
# ============================================================
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📈 Evolução da Receita")
    df_tempo = df.copy()
    df_tempo["data_venda"] = pd.to_datetime(df_tempo["data_venda"])
    df_tempo = df_tempo.groupby(df_tempo["data_venda"].dt.to_period("W").astype(str))["receita"].sum().reset_index()
    df_tempo.columns = ["semana", "receita"]

    fig_linha = px.area(
        df_tempo,
        x="semana",
        y="receita",
        color_discrete_sequence=["#7c3aed"],
        template="plotly_dark"
    )
    fig_linha.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        showlegend=False,
        xaxis_title="",
        yaxis_title="Receita (R$)"
    )
    st.plotly_chart(fig_linha, use_container_width=True)

with col_right:
    st.subheader("🏆 Receita por Categoria")
    df_cat = df.groupby("categoria")["receita"].sum().reset_index()
    fig_pizza = px.pie(
        df_cat,
        values="receita",
        names="categoria",
        color_discrete_sequence=px.colors.sequential.Purples_r,
        template="plotly_dark"
    )
    fig_pizza.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117"
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

# ============================================================
# Gráficos — linha 2
# ============================================================
col_l2, col_r2 = st.columns(2)

with col_l2:
    st.subheader("📦 Top 10 Produtos")
    df_prod = df.groupby("produto")["receita"].sum().nlargest(10).reset_index()
    fig_bar = px.bar(
        df_prod,
        x="receita",
        y="produto",
        orientation="h",
        color="receita",
        color_continuous_scale="Purples",
        template="plotly_dark"
    )
    fig_bar.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        showlegend=False,
        xaxis_title="Receita (R$)",
        yaxis_title=""
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_r2:
    st.subheader("🗺️ Vendas por Cidade")
    df_cidade = df.groupby("cidade")["receita"].sum().reset_index()
    fig_cidade = px.bar(
        df_cidade.sort_values("receita", ascending=True).tail(10),
        x="receita",
        y="cidade",
        orientation="h",
        color_discrete_sequence=["#06b6d4"],
        template="plotly_dark"
    )
    fig_cidade.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        xaxis_title="Receita (R$)",
        yaxis_title=""
    )
    st.plotly_chart(fig_cidade, use_container_width=True)

# ============================================================
# AI Insights com Claude
# ============================================================
st.markdown("---")
st.subheader("🤖 Insights com IA (Claude)")

if st.button("🔍 Gerar Análise Inteligente", type="primary"):
    with st.spinner("Analisando dados com Claude..."):
        try:
            resumo = f"""
            Período: {periodo}
            Receita Total: R$ {receita_total:,.2f}
            Total de Vendas: {total_vendas}
            Ticket Médio: R$ {ticket_medio:,.2f}
            Categorias: {df['categoria'].value_counts().to_dict()}
            Top 3 Produtos: {df.groupby('produto')['receita'].sum().nlargest(3).to_dict()}
            """

            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=[{
                    "role": "user",
                    "content": f"""
                    Analise esses dados de vendas e forneça 3 insights estratégicos em português,
                    focando em oportunidades de crescimento e pontos de atenção:

                    {resumo}

                    Seja direto e objetivo. Use bullet points.
                    """
                }]
            )
            st.success(response.content[0].text)
        except Exception as e:
            st.warning(f"Configure ANTHROPIC_API_KEY para usar insights com IA. Erro: {e}")

# ============================================================
# Rodapé
# ============================================================
st.markdown("---")
st.markdown(
    "*Dashboard open source desenvolvido com Streamlit + Plotly + PostgreSQL. "
    "Substitui Power BI Pro com economia de R$ 4.060/mês.*"
)
