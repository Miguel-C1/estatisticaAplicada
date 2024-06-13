import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, shapiro, normaltest, kstest

# Função para limpar e converter os dados
def clean_data(value):
    if isinstance(value, str):
        try:
            # Remove spaces and convert to float
            return float(value.replace(" ", "").replace(",", "."))
        except ValueError:
            return np.nan
    else:
        return value

# Carregar os dados do arquivo CSV corrigido
data = pd.read_csv('SAO_PAULO_TAUBATE_clean.csv', delimiter=';', decimal=',')

def dist_norml(data: pd.DataFrame):
    # Visualização de Dados
    for column in data.columns[2:]:
        sns.histplot(data[column], stat="density", linewidth=0)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mean[column], std_dev[column])
        plt.plot(x, p, 'k', linewidth=2)
        title = "Distribuição Normal: {}".format(column)
        plt.title(title)
        plt.xlabel(column)
        plt.ylabel('Densidade')
        plt.show()

def dist_norml_prd(data_standardized: pd.DataFrame):
    # Análise de Probabilidades
    for column in data_standardized.columns:
        sns.histplot(data_standardized[column], kde=True, stat="density", linewidth=0)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, 0, 1)
        plt.plot(x, p, 'k', linewidth=2)
        title = "Distribuição Normal Padronizada: {}".format(column)
        plt.title(title)
        plt.xlabel(column)
        plt.ylabel('Densidade')
        plt.show()

# Aplicar a função de limpeza em todas as colunas numéricas
for column in data.columns[2:]:  # Ignora as duas primeiras colunas que são Data e Hora
    data[column] = data[column].apply(clean_data)


numeric_data = data.iloc[:, 2:]  # Seleciona apenas as colunas numéricas após as duas primeiras

# Análise Descritiva
mean = numeric_data.mean()
median = numeric_data.median()
mode = numeric_data.mode().iloc[0]
std_dev = numeric_data.std()
variance = numeric_data.var()
kurtosis = numeric_data.kurtosis()
skewness = numeric_data.skew()

print(f"Média: \n{mean}\n")
print(f"Mediana: \n{median}\n")
print(f"Moda: \n{mode}\n")
print(f"Desvio Padrão: \n{std_dev}\n")
print(f"Variância: \n{variance}\n")
print(f"Curtose: \n{kurtosis}\n")
print(f"Assimetria: \n{skewness}\n")

# Criar DataFrame com estatísticas descritivas
desc_stats = pd.DataFrame({
    'Média': mean,
    'Mediana': median,
    'Moda': mode,
    'Desvio Padrão': std_dev,
    'Variância': variance,
    'Curtose': kurtosis,
    'Assimetria': skewness
})

# Salvar DataFrame em um arquivo CSV
desc_stats.to_csv('analise_descritiva.csv', index=True)



# Testes de Normalidade
def normality_tests(column_data):
    stat, p_shapiro = shapiro(column_data)
    stat, p_normaltest = normaltest(column_data)
    stat, p_kstest = kstest(column_data, 'norm', args=(mean[column_data.name], std_dev[column_data.name]))
    
    return p_shapiro, p_normaltest, p_kstest

for column in data.columns[2:]:
    p_shapiro, p_normaltest, p_kstest = normality_tests(data[column])
    print(f"Resultados dos testes de normalidade para {column}:\n")
    print(f"Shapiro-Wilk: p-value = {p_shapiro}")
    print(f"D'Agostino-Pearson: p-value = {p_normaltest}")
    print(f"Kolmogorov-Smirnov: p-value = {p_kstest}\n")

# Padronização
data_standardized = (data[data.columns[2:]] - mean) / std_dev
print(data_standardized.head())



