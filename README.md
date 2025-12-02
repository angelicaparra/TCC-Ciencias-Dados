# 🎯 Qual a Sua Vibe Profissional?  
Aplicação interativa desenvolvida em **Python + Streamlit** que utiliza **Lógica Fuzzy** para avaliar o perfil do usuário e indicar qual área profissional mais combina com suas habilidades e interesses.

O projeto foi criado como parte de um estudo para o **TCC**, aplicando conceitos de Inteligência Artificial, tomada de decisão imprecisa, análise de dados e experiência do usuário.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.12**
- **Streamlit** – interface web interativa
- **Scikit-Fuzzy (skfuzzy)** – motor de inferência fuzzy
- **Numpy & Pandas** – cálculo e manipulação de dados
- **NetworkX** – suporte interno ao sistema fuzzy

---

## 🧠 Como funciona o sistema?

O usuário responde um questionário com notas de **0 a 10**, representando o quanto cada afirmação faz sentido para ele.

Cada pergunta é ligada a uma área profissional:

- 📊 Ciência de Dados  
- 💼 Gestão Comercial  
- 🚚 Logística  

O algoritmo então:

1. **Calcula média ponderada das respostas**
2. Classifica cada pergunta automaticamente como:
   - **Aptidão**
   - **Interesse**
3. Utiliza um modelo de **Lógica Fuzzy** para simular julgamento humano:
   - Baixa / Média / Alta aptidão
   - Baixo / Médio / Alto interesse
4. Gera uma **porcentagem final (0–100%)** para cada área
5. Exibe:
   - Percentual de compatibilidade  
   - Nota base  
   - Aptidão e interesse estimados  
   - Classificação final:
     - 🤩 **Recomendado**
     - 😎 **Potencial**
     - 🤷‍♂️ **Não recomendado**

---

## 🖥️ Demonstração (local)

Para rodar o projeto no seu computador:

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO

python -m venv venv
.\venv\Scripts\activate   # Windows

pip install -r requirements.txt

python -m streamlit run app.py
