import streamlit as st
# Certifique-se de que 'CPF' e 'CPF.validate' estejam corretamente importados
from cpf_generator import CPF 
from streamlit_tree_select import tree_select
import requests
import json
import time

# --- Mapeamento de Valores (Para exibição limpa dos resultados) ---
# Dicionário simples para mapear o 'value' técnico ao 'label' legível.
CERT_MAP = {
    "Debitos_Federais": "Certidão de Débitos Federais",
    "Antecedentes_Criminais": "Certidão de Antecedentes Criminais",
    "debitos_estaduais": "Certidão de Débitos Estaduais",
    "tce_key": "Certidão TCE",
    "Quitação_Eleitoral": "Certidão de Quitação Eleitoral",
}

# ----------------------------------------------------
# Inicialização do Estado da Sessão
# ----------------------------------------------------
if 'cert_results' not in st.session_state:
    st.session_state['cert_results'] = None

# ----------------------------------------------------
# Configurações de Página e Título Principal
# ----------------------------------------------------
st.set_page_config(layout="wide", page_title="Sistema de Certidões API")

# NOVA FUNCIONALIDADE: INCLUSÃO DA IMAGEM
# Atenção: Este caminho de arquivo é local e pode não funcionar em ambientes de nuvem.
st.image("/home/alanancy/Documentos/Streamlit/frontPyton/img/image.png", width=300)

st.title("Cadeia de Certidões ")

st.markdown("""
Este sistema permite a emissão de certidões digitais utilizando a API do conecta.gov.
""")

# ----------------------------------------------------
# 1. Definição dos Dados da Árvore
# ----------------------------------------------------
tree_data = [
    {
        "label": "Certidões Disponíveis",
        "value": "Todas_as_Certidões",
        "key": "Cadeias_de_Certidões",
        "children": [
            {
                "label": "Certidões Federais",
                "value": "Federais",
                "children": [
                    {"label": "📄 Receita Federal", "value": "Debitos_Federais"},
                    {"label": "📄 Criminal", "value": "Antecedentes_Criminais"},
                ],
            },
            {
                "label": "Certidões Estaduais",
                "value": "Estaduais",
                "children": [
                    {"label": "📄 Débitos Estaduais", "value": "debitos_estaduais"},
                    {"label": "📄 TCE", "value": "Tribunal_Contas_Estadual"},
                ],
            },
            {"label": "📄 Certidões Tribunal Superior Eleitoral", "value": "Quitação_Eleitoral"},
        ],
    },
]

# ----------------------------------------------------
# 2. Renderização na Barra Lateral (st.sidebar)
# ----------------------------------------------------
with st.sidebar:
    st.header("Seleção de Certidões") # CABEÇALHO ATUALIZADO

    # SELETOR DE ÁRVORE
    certidao_selecao = tree_select(
        tree_data,
        checked=["Debitos_Federais"],
        key="tree_select_certidoes"
    )
    
    st.markdown("---")

    # MENSAGEM DE INSTRUÇÃO ATUALIZADA
    st.info("Para emitir, digite o documento (CPF OU CNPJ) na área principal e clique em 'Emitir Certidões'.")

    st.markdown("---")
    
    # --- BLOCO: RESULTADOS DA EMISSÃO (COM ÍCONES) ---
    if st.session_state['cert_results']:
        st.subheader("✅ Certidões Emitidas")
        st.markdown("---")
        
        # Itera sobre os resultados armazenados no estado da sessão
        for value in st.session_state['cert_results']:
            label = CERT_MAP.get(value, value)
            # Simula um link de download com ícone de PDF
            st.markdown(f"""
            <div style="padding: 5px 0; border-bottom: 1px solid #eee;">
                📄 <a href='#' style='text-decoration: none; color: #1f77b4;'>{label}</a>
            </div>
            """, unsafe_allow_html=True)
    # ---------------------------------------------------------

# ----------------------------------------------------
# 3. Área Principal: Input de Documento e Processamento
# ----------------------------------------------------

# Input do CPF/CNPJ na ÁREA PRINCIPAL
cpf_cnpj = st.text_input("Digite o número do CPF ou CNPJ para emitir a certidão (somente números):", max_chars=14)

def valida_cpf(documento):
    if len(documento) == 11:
        return CPF.validate(documento)
    elif len(documento) == 14 and documento.isdigit():
        return True # Substitua por validação de CNPJ real
    return False

# Formata o documento (apenas para exibição)
documento_formatado = CPF.format(cpf_cnpj) if len(cpf_cnpj) == 11 else cpf_cnpj

# Botão de Emissão
if st.button("Emitir Certidões"):
    if not cpf_cnpj:
        st.warning("Por favor, digite um CPF ou CNPJ.")
        st.session_state['cert_results'] = None # Limpa resultados anteriores
    elif not valida_cpf(cpf_cnpj):
        st.error("Documento inválido. Por favor, insira um CPF ou CNPJ válido.")
        st.session_state['cert_results'] = None # Limpa resultados anteriores
    else:
        # Pega as certidões selecionadas
        tipos_selecionados = certidao_selecao['checked']
        
        st.subheader(f"Processando para o documento: {documento_formatado}")
        st.info(f"Certidões selecionadas para emissão: {', '.join(tipos_selecionados)}")

        # Simulação de Processamento
        with st.spinner('Processando a emissão das certidões...'):
            progress_bar = st.progress(0)   
            for i in range(1, 101):
                time.sleep(0.01)
                progress_bar.progress(i)
            
            # --- ATUALIZA O ESTADO DA SESSÃO COM OS RESULTADOS ---
            st.session_state['cert_results'] = tipos_selecionados
            # ---------------------------------------------------

            st.success('Certidões emitidas com sucesso! Verifique a barra lateral para os links de download.')
            st.balloons() # Mantido o balão na conclusão
            
            st.markdown("### Detalhes da Emissão (Simulação de Retorno da API)")
            st.json({
                "documento": documento_formatado,
                "status": "CONCLUIDO",
                "certidoes_emitidas": tipos_selecionados,
                "data_emissao": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # FORÇA A RE-EXECUÇÃO DO SCRIPT PARA GARANTIR A ATUALIZAÇÃO DA SIDEBAR
            st.rerun()