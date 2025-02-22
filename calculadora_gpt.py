import streamlit as st

class GPTCostCalculator:
    def __init__(self, exchange_rate=5.73):
        self.exchange_rate = exchange_rate
        self.gpt4o_avg_cost = 4.58  # Média dos custos do GPT-4o
        self.gpt4o_mini_avg_cost = 0.275  # Média dos custos do GPT-4o mini
    
    def calc_executions_per_million(self, tokens_per_execution):
        return 1_000_000 / tokens_per_execution
    
    def calc_cost_for_executions(self, model, num_executions, tokens_per_execution):
        if model == 'GPT-4o':
            cost_per_million = self.gpt4o_avg_cost
        elif model == 'GPT-4o mini':
            cost_per_million = self.gpt4o_mini_avg_cost
        else:
            return "Modelo inválido"
        
        total_tokens = num_executions * tokens_per_execution
        cost_usd = (total_tokens / 1_000_000) * cost_per_million
        cost_brl = cost_usd * self.exchange_rate
        
        return {'cost_usd': cost_usd, 'cost_brl': cost_brl}

calculator = GPTCostCalculator()

st.title("📊 GPT Cost Calculator")

model = st.selectbox("💻 Escolha o modelo:", ["GPT-4o", "GPT-4o mini"])
function_name = st.text_input("🛠 Nome da Função (ex: Resposta de comentário)")
tokens_per_exec = st.number_input("🔢 Média de tokens por execução:", min_value=1, value=500)
num_execs = st.number_input("🔄 Número de execuções (deixe 0 para calcular execuções por 1M tokens):", min_value=0, value=0)

if st.button("📌 Calcular"):
    executions_per_million = calculator.calc_executions_per_million(tokens_per_exec)
    
    st.subheader("📌 Resultados")
    st.markdown(f"<div style='padding:10px; border-radius:10px; background-color:#1E1E1E; color:white;'>"
                f"<b>🛠 Função:</b> {function_name if function_name else 'Não especificado'}<br>"
                f"<b>🔢 Execuções possíveis por 1M tokens:</b> {executions_per_million:.2f}"
                f"</div>", unsafe_allow_html=True)
    
    if num_execs > 0:
        cost_for_execs = calculator.calc_cost_for_executions(model, num_execs, tokens_per_exec)
        st.markdown(f"<div style='padding:10px; border-radius:10px; background-color:#1E1E1E; color:white;'>"
                    f"<b>🔄 Número de execuções:</b> {num_execs}<br>"
                    f"<b>💰 Custo:</b> ${cost_for_execs['cost_usd']:.2f} USD / R${cost_for_execs['cost_brl']:.2f} BRL"
                    f"</div>", unsafe_allow_html=True)
