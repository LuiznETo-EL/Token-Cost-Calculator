import streamlit as st

class GPTCostCalculator:
    def __init__(self, exchange_rate=5.73):
        self.exchange_rate = exchange_rate
        self.gpt4o = {'input': 2.50, 'cached_input': 1.25, 'output': 10.00}
        self.gpt4o_mini = {'input': 0.150, 'cached_input': 0.075, 'output': 0.600}
    
    def calc_executions_per_million(self, model, function_type, tokens_per_execution):
        if model == 'GPT-4o':
            cost_per_million = self.gpt4o.get(function_type, 0)
        elif model == 'GPT-4o mini':
            cost_per_million = self.gpt4o_mini.get(function_type, 0)
        else:
            return "Modelo inválido"
        
        executions = 1_000_000 / tokens_per_execution
        return executions
    
    def calc_cost_for_executions(self, model, function_type, num_executions, tokens_per_execution):
        if model == 'GPT-4o':
            cost_per_million = self.gpt4o.get(function_type, 0)
        elif model == 'GPT-4o mini':
            cost_per_million = self.gpt4o_mini.get(function_type, 0)
        else:
            return "Modelo inválido"
        
        total_tokens = num_executions * tokens_per_execution
        cost_usd = (total_tokens / 1_000_000) * cost_per_million
        cost_brl = cost_usd * self.exchange_rate
        
        return {'cost_usd': cost_usd, 'cost_brl': cost_brl}

calculator = GPTCostCalculator()

st.title("GPT Cost Calculator")

model = st.selectbox("Escolha o modelo:", ["GPT-4o", "GPT-4o mini"])
function_type = st.selectbox("Escolha a função:", ["input", "cached_input", "output"])
tokens_per_exec = st.number_input("Tokens por execução:", min_value=1, value=500)
num_execs = st.number_input("Número de execuções:", min_value=1, value=2000)

if st.button("Calcular"):
    executions_per_million = calculator.calc_executions_per_million(model, function_type, tokens_per_exec)
    cost_for_execs = calculator.calc_cost_for_executions(model, function_type, num_execs, tokens_per_exec)
    
    st.write(f"**Execuções por 1M tokens:** {executions_per_million:.2f}")
    st.write(f"**Custo:** ${cost_for_execs['cost_usd']:.2f} USD / R${cost_for_execs['cost_brl']:.2f} BRL")
