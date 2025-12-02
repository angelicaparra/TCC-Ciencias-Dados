import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
import time
import random

# =============================================
# Função de rerun compatível (novas e antigas versões)
# =============================================
def do_rerun():
    """Chama o rerun de forma compatível com várias versões do Streamlit."""
    try:
        # Versões novas
        st.rerun()
    except AttributeError:
        # Versões antigas
        st.experimental_rerun()

# =============================================
# 1. Definição das Variáveis de Entrada (Questionário)
# =============================================
variaveis_entrada = {
    'CD1': {'area': 'ciencia_dados', 'texto': "Gosto de resolver problemas usando matemática e programação", 'peso': 0.9},
    'CD2': {'area': 'ciencia_dados', 'texto': "Tenho interesse em análise de dados e inteligência artificial", 'peso': 1.0},
    'CD3': {'area': 'ciencia_dados', 'texto': "Me divirto trabalhando com planilhas e bancos de dados", 'peso': 0.7},
    'CD4': {'area': 'ciencia_dados', 'texto': "Tenho facilidade com estatística e raciocínio lógico", 'peso': 0.8},

    'GC1': {'area': 'gestao_comercial', 'texto': "Gosto de lidar com pessoas e fazer negócios", 'peso': 0.9},
    'GC2': {'area': 'gestao_comercial', 'texto': "Tenho facilidade para comunicação e persuasão", 'peso': 1.0},
    'GC3': {'area': "gestao_comercial", 'texto': "Me interesso por marketing e vendas", 'peso': 0.8},
    'GC4': {'area': 'gestao_comercial', 'texto': "Tenho perfil empreendedor e criativo", 'peso': 0.7},
    
    'LG1': {'area': 'logistica', 'texto': "Gosto de organizar processos e fluxos de trabalho", 'peso': 0.9},
    'LG2': {'area': 'logistica', 'texto': "Me interesso por cadeia de suprimentos e transportes", 'peso': 1.0},
    'LG3': {'area': 'logistica', 'texto': "Tenho facilidade com gestão de tempo e recursos", 'peso': 0.8},
    'LG4': {'area': 'logistica', 'texto': "Me adapto bem a situações que exigem planejamento detalhado", 'peso': 0.7}
}

nomes_cursos = {
    'ciencia_dados': 'Ciência de Dados 📊',
    'gestao_comercial': 'Gestão Comercial 💼',
    'logistica': 'Logística 🚚'
}

# Palavras-chave simples para classificar cada pergunta como "aptidão" ou "interesse"
KEYWORDS_APTIDAO = [
    'facilidade', 'estatística', 'raciocínio', 'raciocinio', 'organizar',
    'gestão de tempo', 'gestao de tempo', 'resolver', 'programação', 'programacao',
    'facil'
]
KEYWORDS_INTERESSE = [
    'interesse', 'gosto de', 'me interesso', 'marketing', 'vendas', 'comunicação', 'comunicacao',
    'cadeia de suprimentos', 'transportes', 'negócios', 'negocios'
]

def texto_eh_aptidao(texto):
    t = texto.lower()
    for kw in KEYWORDS_APTIDAO:
        if kw in t:
            return True
    return False

def texto_eh_interesse(texto):
    t = texto.lower()
    for kw in KEYWORDS_INTERESSE:
        if kw in t:
            return True
    return False

# =============================================
# 2. Cálculo dos Escores por Área (nota geral + aptidão + interesse)
# =============================================
def calcular_notas(respostas):
    """
    Retorna um dicionário por área com:
    {
      'nota' : média ponderada geral (0-10),
      'aptidao': média ponderada das perguntas consideradas aptidão (0-10),
      'interesse': média ponderada das perguntas consideradas interesse (0-10)
    }
    """
    areas = {v['area'] for v in variaveis_entrada.values()}
    notas = {
        area: {
            'soma': 0.0, 'peso': 0.0,
            'apt_soma': 0.0, 'apt_peso': 0.0,
            'int_soma': 0.0, 'int_peso': 0.0
        } 
        for area in areas
    }

    for key, value in respostas.items():
        meta = variaveis_entrada.get(key)
        if not meta:
            continue
        area = meta['area']
        peso = meta.get('peso', 1.0)
        nota = float(value)

        # acumuladores gerais
        notas[area]['soma'] += nota * peso
        notas[area]['peso'] += peso

        texto = meta['texto']

        # detectar aptidão/interesse por simples heurística
        if texto_eh_aptidao(texto):
            notas[area]['apt_soma'] += nota * peso
            notas[area]['apt_peso'] += peso
        if texto_eh_interesse(texto):
            notas[area]['int_soma'] += nota * peso
            notas[area]['int_peso'] += peso

    resultados = {}
    for area, vals in notas.items():
        # nota geral
        if vals['peso'] > 0:
            nota_geral = (vals['soma'] / vals['peso'])
        else:
            nota_geral = 0.0

        # aptidão
        if vals['apt_peso'] > 0:
            apt = (vals['apt_soma'] / vals['apt_peso'])
        else:
            apt = nota_geral

        # interesse
        if vals['int_peso'] > 0:
            inte = (vals['int_soma'] / vals['int_peso'])
        else:
            inte = nota_geral

        # garantir limites 0-10
        nota_geral = max(0.0, min(10.0, nota_geral))
        apt = max(0.0, min(10.0, apt))
        inte = max(0.0, min(10.0, inte))

        resultados[area] = {'nota': nota_geral, 'aptidao': apt, 'interesse': inte}

    return resultados

# =============================================
# 3. Sistema Fuzzy
# =============================================
aptidao = ctrl.Antecedent(np.arange(0, 11, 1), 'aptidao')
interesse = ctrl.Antecedent(np.arange(0, 11, 1), 'interesse')
perfil = ctrl.Consequent(np.arange(0, 101, 1), 'perfil')

aptidao['baixa'] = fuzz.trimf(aptidao.universe, [0, 0, 5])
aptidao['media'] = fuzz.trimf(aptidao.universe, [0, 5, 10])
aptidao['alta'] = fuzz.trimf(aptidao.universe, [5, 10, 10])

interesse['baixo'] = fuzz.trimf(interesse.universe, [0, 0, 5])
interesse['medio'] = fuzz.trimf(interesse.universe, [0, 5, 10])
interesse['alto'] = fuzz.trimf(interesse.universe, [5, 10, 10])

perfil['baixo'] = fuzz.trimf(perfil.universe, [0, 0, 50])
perfil['medio'] = fuzz.trimf(perfil.universe, [0, 50, 100])
perfil['alto'] = fuzz.trimf(perfil.universe, [50, 100, 100])

rules = [
    ctrl.Rule(aptidao['alta'] & interesse['alto'], perfil['alto']),
    ctrl.Rule(aptidao['media'] | interesse['medio'], perfil['medio']),
    ctrl.Rule(aptidao['baixa'] & interesse['baixo'], perfil['baixo']),
    ctrl.Rule(aptidao['alta'] & interesse['medio'], perfil['alto']),
    ctrl.Rule(aptidao['media'] & interesse['alto'], perfil['alto']),
    ctrl.Rule(aptidao['baixa'] & interesse['medio'], perfil['baixo'])
]

sistema_perfil = ctrl.ControlSystem(rules)

# =============================================
# 4. Avaliar perfil e exibir resultados
# =============================================
def avaliar_perfil():
    """Avalia o perfil do usuário e exibe os resultados com porcentagens corretas."""
    notas_por_area = calcular_notas(st.session_state.respostas)
    resultados = {}

    for area, dados_area in notas_por_area.items():
        nota_geral = dados_area['nota']
        apt = dados_area['aptidao']
        inte = dados_area['interesse']

        avaliador_local = ctrl.ControlSystemSimulation(sistema_perfil)
        avaliador_local.input['aptidao'] = apt
        avaliador_local.input['interesse'] = inte
        avaliador_local.compute()
        perfil_valor = avaliador_local.output['perfil']  # 0–100

        if perfil_valor >= 70:
            classificacao = "Recomendado"
            emoji = "🤩"
        elif perfil_valor >= 40:
            classificacao = "Potencial"
            emoji = "😎"
        else:
            classificacao = "Não recomendado"
            emoji = "🤷‍♂️"

        resultados[nomes_cursos[area]] = {
            'pontuacao': nota_geral,
            'aptidao': apt,
            'interesse': inte,
            'perfil': perfil_valor,
            'classificacao': classificacao,
            'emoji': emoji
        }

    df_resultados = pd.DataFrame(
        {
            'Área': list(resultados.keys()),
            'Porcentagem': [dados['perfil'] for dados in resultados.values()]
        }
    )

    st.header("Chegou o Resultado! 🎉")
    st.markdown("Aqui está o quanto cada área combina com a sua vibe (porcentagem fuzzy).")
    st.bar_chart(df_resultados.set_index("Área"))

    st.subheader("Análise Completa 👇")
    cols = st.columns(len(resultados))

    for i, (curso, dados) in enumerate(resultados.items()):
        with cols[i]:
            st.metric(
                label=f"**{curso}**",
                value=f"{dados['perfil']:.1f}%"
            )
            st.markdown(f"**Classificação:** {dados['emoji']} {dados['classificacao']}")
            st.markdown(f"**Nota geral:** {dados['pontuacao']:.1f}/10")
            st.markdown(f"**Aptidão (estimada):** {dados['aptidao']:.1f}/10")
            st.markdown(f"**Interesse (estimado):** {dados['interesse']:.1f}/10")

# =============================================
# 5. Interface Streamlit
# =============================================
st.set_page_config(page_title="Qual a sua Vibe?", layout="centered")

if 'shuffled_questions' not in st.session_state:
    st.session_state.shuffled_questions = random.sample(list(variaveis_entrada.keys()), len(variaveis_entrada))
    st.session_state.current_question = 0
    st.session_state.respostas = {}

st.title("Qual a sua Vibe Profissional? 🤔")
st.markdown("Responda cada afirmação de 0 a 10 — **0** = não me representa, **10** = super me representa.")
st.write("---")

total_perguntas = len(st.session_state.shuffled_questions)

if st.session_state.current_question < total_perguntas:
    key = st.session_state.shuffled_questions[st.session_state.current_question]
    dados_pergunta = variaveis_entrada[key]

    st.subheader(f"Pergunta {st.session_state.current_question + 1} de {total_perguntas}")
    st.markdown(f"**{dados_pergunta['texto']}**")

    resposta = st.radio(
        "Nota:",
        options=list(range(11)),
        index=5,
        horizontal=True,
        key=key
    )

    st.write("---")
    if st.button("Próxima ⏩"):
        st.session_state.respostas[key] = int(resposta)
        st.session_state.current_question += 1
        do_rerun()

else:
    with st.spinner("Uhuul! Calculando seu perfil..."):
        time.sleep(1.2)
    avaliar_perfil()
    st.write("---")
    if st.button("Refazer"):
        st.session_state.shuffled_questions = random.sample(list(variaveis_entrada.keys()), len(variaveis_entrada))
        st.session_state.current_question = 0
        st.session_state.respostas = {}
        do_rerun()
