import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuração da página para usar toda a largura
st.set_page_config(
    page_title="Ultra Wide Dashboard - Auto Ajuste",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS para maximizar o espaço horizontal
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 100% !important;
        width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    .element-container {
        margin: 0 !important;
    }
    .stPlotlyChart, .stPyplot {
        margin: 0 !important;
        padding: 0 !important;
    }
    header[data-testid="stHeader"] {
        height: 0 !important;
    }
    div[data-testid="column"] {
        padding: 0 0.25rem !important;
    }
    h1 {
        margin-top: 0 !important;
        margin-bottom: 1rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# JavaScript para detectar dimensões da tela
st.markdown("""
<script>
function getScreenInfo() {
    return {
        width: window.screen.width,
        height: window.screen.height,
        availWidth: window.screen.availWidth,
        availHeight: window.screen.availHeight,
        innerWidth: window.innerWidth,
        innerHeight: window.innerHeight
    };
}
</script>
""", unsafe_allow_html=True)

st.title("🖥️ Dashboard Ultra Wide - Auto Ajuste Inteligente")

# Seção de controles manuais
st.sidebar.header("⚙️ Configurações")
st.sidebar.markdown("**Ajuste manual ou deixe no automático**")

# Detectar largura aproximada (método alternativo via Streamlit)
# Como não temos acesso direto ao JavaScript, usamos estimativas baseadas em padrões
auto_mode = st.sidebar.checkbox("🤖 Modo Automático", value=True)

if auto_mode:
    st.sidebar.info("Modo automático ativado - o sistema ajustará com base em estimativas otimizadas")
    # Configurações automáticas baseadas em padrões comuns
    num_cols = 12  # Padrão para ultra wide
    chart_width = 2.5
    chart_height = 3.5
else:
    st.sidebar.markdown("### 🎛️ Controles Manuais")
    
    # Seletor de resolução comum
    resolution_preset = st.sidebar.selectbox(
        "Preset de Resolução:",
        [
            "Ultra Wide 3440x1440",
            "Ultra Wide 2560x1080", 
            "4K 3840x2160",
            "QHD 2560x1440",
            "Full HD 1920x1080",
            "Personalizado"
        ]
    )
    
    # Definir configurações baseadas no preset
    preset_configs = {
        "Ultra Wide 3440x1440": {"cols": 14, "width": 2.2, "height": 3.2},
        "Ultra Wide 2560x1080": {"cols": 12, "width": 2.5, "height": 3.0},
        "4K 3840x2160": {"cols": 16, "width": 2.0, "height": 3.0},
        "QHD 2560x1440": {"cols": 10, "width": 2.8, "height": 3.5},
        "Full HD 1920x1080": {"cols": 8, "width": 3.0, "height": 3.8},
        "Personalizado": {"cols": 8, "width": 3.0, "height": 3.8}
    }
    
    if resolution_preset != "Personalizado":
        config = preset_configs[resolution_preset]
        num_cols = config["cols"]
        chart_width = config["width"]
        chart_height = config["height"]
        st.sidebar.success(f"✅ Usando preset: {resolution_preset}")
        st.sidebar.write(f"- Colunas: {num_cols}")
        st.sidebar.write(f"- Tamanho gráfico: {chart_width}x{chart_height}")
    else:
        st.sidebar.markdown("#### Configuração Manual")
        num_cols = st.sidebar.slider("Número de Colunas", 4, 20, 12)
        chart_width = st.sidebar.slider("Largura do Gráfico", 1.5, 4.0, 2.5, 0.1)
        chart_height = st.sidebar.slider("Altura do Gráfico", 2.0, 5.0, 3.5, 0.1)

# Mostrar informações da configuração atual
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    st.metric("📊 Colunas", num_cols)
with col_info2:
    st.metric("📏 Largura Gráfico", f"{chart_width}")
with col_info3:
    st.metric("📐 Altura Gráfico", f"{chart_height}")

# Botão para testar diferentes densidades
st.markdown("### 🧪 Teste Rápido de Densidade")
density_test = st.radio(
    "Escolha uma densidade para testar:",
    ["Baixa (6 gráficos)", "Média (padrão)", "Alta (+4 gráficos)", "Máxima (+8 gráficos)"],
    index=1,
    horizontal=True
)

# Ajustar número de colunas baseado no teste
if density_test == "Baixa (6 gráficos)":
    test_cols = max(6, num_cols - 4)
elif density_test == "Média (padrão)":
    test_cols = num_cols
elif density_test == "Alta (+4 gráficos)":
    test_cols = num_cols + 4
else:  # Máxima
    test_cols = min(20, num_cols + 8)

st.info(f"🎯 Usando {test_cols} colunas para este teste")

# Gerar os gráficos
cols = st.columns(test_cols)

# Configuração do matplotlib
plt.rcParams.update({
    'figure.figsize': (chart_width, chart_height),
    'axes.titlesize': 8,
    'axes.labelsize': 6,
    'xtick.labelsize': 6,
    'ytick.labelsize': 6,
    'figure.titlesize': 8
})

# Diferentes tipos de gráficos para variar
chart_types = ['bar', 'line', 'scatter', 'pie']

for i, col in enumerate(cols):
    with col:
        # Alternar tipos de gráfico
        chart_type = chart_types[i % len(chart_types)]
        
        fig, ax = plt.subplots(figsize=(chart_width, chart_height))
        
        if chart_type == 'bar':
            x = np.arange(5)
            y = np.random.randint(1, 10, size=5)
            bars = ax.bar(x, y, color=f'C{i%10}', alpha=0.7)
            ax.set_title(f'Barras {i+1}', fontsize=8, pad=2)
            ax.set_xticks([])
            
        elif chart_type == 'line':
            x = np.linspace(0, 10, 20)
            y = np.sin(x + i) + np.random.normal(0, 0.1, 20)
            ax.plot(x, y, color=f'C{i%10}', linewidth=2)
            ax.set_title(f'Linha {i+1}', fontsize=8, pad=2)
            ax.set_xticks([])
            
        elif chart_type == 'scatter':
            x = np.random.randn(30)
            y = np.random.randn(30)
            ax.scatter(x, y, color=f'C{i%10}', alpha=0.7, s=20)
            ax.set_title(f'Dispersão {i+1}', fontsize=8, pad=2)
            ax.set_xticks([])
            
        else:  # pie
            sizes = np.random.randint(1, 5, 3)
            ax.pie(sizes, labels=['A', 'B', 'C'], autopct='%1.0f%%', 
                   colors=[f'C{(i+j)%10}' for j in range(3)])
            ax.set_title(f'Pizza {i+1}', fontsize=8, pad=2)
        
        # Configurações comuns
        ax.tick_params(axis='y', labelsize=6)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        fig.tight_layout(pad=0.3)
        st.pyplot(fig, use_container_width=True, clear_figure=True)

# Seção de métricas responsivas
st.markdown("---")
st.subheader("📈 Métricas Responsivas")

# Ajustar número de métricas baseado na largura
metrics_cols = min(test_cols, 10)  # Máximo 10 métricas
metric_columns = st.columns(metrics_cols)

for i, col in enumerate(metric_columns):
    with col:
        st.metric(
            label=f"KPI {i+1}",
            value=f"{np.random.randint(100, 9999):,}",
            delta=f"{np.random.randint(-500, 500):+,}"
        )

# Dicas e informações
st.markdown("---")
st.markdown("### 💡 Dicas de Otimização")

tip_cols = st.columns(2)
with tip_cols[0]:
    st.info("""
    **🎯 Para encontrar sua configuração ideal:**
    1. Comece com o preset mais próximo da sua resolução
    2. Use o teste de densidade para ver o que fica melhor
    3. Ajuste manualmente se necessário
    4. Salve as configurações que funcionaram
    """)

with tip_cols[1]:
    st.success("""
    **📊 Configurações Recomendadas:**
    - **Ultra Wide (3440px)**: 12-16 colunas
    - **4K Wide**: 14-18 colunas
    - **QHD**: 8-12 colunas
    - **Full HD**: 6-10 colunas
    """)

# Informações técnicas (expandível)
with st.expander("🔧 Informações Técnicas"):
    st.write(f"""
    **Configuração Atual:**
    - Colunas em uso: {test_cols}
    - Tamanho dos gráficos: {chart_width} x {chart_height}
    - Modo: {'Automático' if auto_mode else 'Manual'}
    - Densidade: {density_test}
    
    **Para implementar em produção:**
    - Copie as configurações que funcionaram melhor
    - Considere criar diferentes layouts para diferentes páginas
    - Use `st.session_state` para salvar preferências do usuário
    """)

st.markdown("---")
st.caption("💻 Desenvolvido para aproveitar ao máximo telas ultra wide")