import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, shapiro, normaltest, kstest, f_oneway
import dist_norml
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
#data = pd.read_csv('sp_tb_clean.csv', delimiter=';', decimal=',')
#data = pd.read_csv('BAHIA_BELMONTE_clean.csv', delimiter=';', decimal=',')
data = pd.read_csv('SAO_PAULO_TAUBATE_clean.csv', delimiter=';', decimal=',')

def normality_tests(column_data):
    stat, p_shapiro = shapiro(column_data)
    stat, p_normaltest = normaltest(column_data)
    stat, p_kstest = kstest(column_data, 'norm', args=(mean[column_data.name], std_dev[column_data.name]))
    
    return p_shapiro, p_normaltest, p_kstest



# Aplicar a função de limpeza em todas as colunas numéricas
for column in data.columns[2:]:  # Ignora as duas primeiras colunas que são Data e Hora
    data[column] = data[column].apply(clean_data)

numeric_data = data.iloc[:, 2:]  # Seleciona apenas as colunas numéricas após as duas primeiras

# analise descritiva de apenas uma deterinada semana
numeric_data_semn = data.loc[(data['Data'] >= '01/03/2024') & (data['Data'] <= '07/03/2024')].iloc[:, 2:]



def analise_desc(numeric_data: pd.DataFrame, nome_arquivo='analise_descritiva.csv'):
    # Análise Descritiva
    mean = numeric_data.mean()
    median = numeric_data.median()
    mode = numeric_data.mode().iloc[0]
    std_dev = numeric_data.std()
    variance = numeric_data.var()
    kurtosis = numeric_data.kurtosis()
    skewness = numeric_data.skew()

    quartiles = numeric_data.quantile([0.25, 0.5, 0.75])
    #print(f"Média: \n{mean}\n")
    #print(f"Mediana: \n{median}\n")
    #print(f"Moda: \n{mode}\n")
    #print(f"Desvio Padrão: \n{std_dev}\n")
    #print(f"Variância: \n{variance}\n")
    #print(f"Curtose: \n{kurtosis}\n")
    #print(f"Assimetria: \n{skewness}\n")
    #print(f"Quartis: \n{quartiles}\n")

    # Criar DataFrame com estatísticas descritivas
    desc_stats = pd.DataFrame({
        'Média': mean,
        'Mediana': median,
        'Moda': mode,
        'Desvio Padrão': std_dev,
        'Variância': variance,
        'Curtose': kurtosis,
        'Assimetria': skewness,
        '1º Quartil': quartiles.loc[0.25],
        '2º Quartil (Mediana)': quartiles.loc[0.5],
        '3º Quartil': quartiles.loc[0.75]
    })
    # Salvar DataFrame em um arquivo CSV
    desc_stats.to_csv(nome_arquivo, index=True)
    
    return mean, std_dev

mean, std_dev = analise_desc(numeric_data)

analise_desc(numeric_data=numeric_data_semn, nome_arquivo='analise_descritiva_semana.csv')

def create_boxplot(data: pd.DataFrame, columns=None):

    if columns is None:
        columns = data.columns[2:]
    # Boxplot
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=data[columns], orient='h', )
    plt.title('Boxplot das Variáveis Numéricas')
    plt.xlabel('Valor')
    plt.show()

# Criar lista para armazenar resultados dos testes de normalidade
results_list = []

# Iterar sobre cada coluna numérica
for column in data.columns[2:]:
    p_shapiro, p_normaltest, p_kstest = normality_tests(numeric_data_semn[column])
    
    # Adicionar resultados à lista
    results_list.append({
        'Coluna': column,
        'Shapiro-Wilk p-value': p_shapiro,
        'D\'Agostino-Pearson p-value': p_normaltest,
        'Kolmogorov-Smirnov p-value': p_kstest
    })

# Criar DataFrame a partir da lista de resultados
results = pd.DataFrame(results_list)

# Salvar resultados em um arquivo CSV
results.to_csv('testes_normalidade_semanal.csv', index=False)


# dist_norml.dist_norml(data=data, columns=['Temp. Ins. (C)', 
#                                'Temp. Max. (C)',
#                                  'Temp. Min. (C)',
#                                 'Pto Orvalho Ins. (C)',
#                                'Pto Orvalho Max. (C)',
#                                'Pto Orvalho Min. (C)',
#                                'Pressao Ins. (hPa)'])

# dist_norml.dist_norml_by_month(data=data, columns=['Temp. Ins. (C)', 
#                                'Temp. Max. (C)',
#                                  'Temp. Min. (C)',
#                                 'Pto Orvalho Ins. (C)',
#                                'Pto Orvalho Max. (C)',
#                                'Pto Orvalho Min. (C)',
#                                'Pressao Ins. (hPa)'])

create_boxplot(data, columns=['Temp. Ins. (C)', 'Temp. Max. (C)', 'Temp. Min. (C)'])
#create_boxplot(data, columns=['Umi. Ins. (%)', 'Umi. Max. (%)', 'Umi. Min. (%)'])
#create_boxplot(data, columns=['Pto Orvalho Ins. (C)', 'Pto Orvalho Max. (C)', 'Pto Orvalho Min. (C)'])
create_boxplot(data, columns=['Pressao Ins. (hPa)', 'Pressao Max. (hPa)', 'Pressao Min. (hPa)'])

# ['Data', 'Hora (UTC)', 'Temp. Ins. (C)', 'Temp. Max. (C)',
#       'Temp. Min. (C)', 'Umi. Ins. (%)', 'Umi. Max. (%)', 'Umi. Min. (%)',   
#       'Pto Orvalho Ins. (C)', 'Pto Orvalho Max. (C)', 'Pto Orvalho Min. (C)',
#      'Pressao Ins. (hPa)', 'Pressao Max. (hPa)', 'Pressao Min. (hPa)',      
#      'Vel. Vento (m/s)', 'Dir. Vento (m/s)', 'Raj. Vento (m/s)',
#      'Radiacao (KJ/m²)', 'Chuva (mm)']

