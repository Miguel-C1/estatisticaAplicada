import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, shapiro, normaltest, kstest, f_oneway

def dist_norml(data: pd.DataFrame, columns=None):
    if columns is None:
        columns = data.columns[2:]  # Seleciona todas as colunas numéricas após as duas primeiras

    for column in columns:
        sns.histplot(data[column], stat="density", linewidth=0)
        mean = data[column].mean()
        std_dev = data[column].std()
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mean, std_dev)
        plt.plot(x, p, 'k', linewidth=2)
        title = f"Distribuição Normal: {column}"
        plt.title(title)
        plt.xlabel(column)
        plt.ylabel('Densidade')
        plt.show()

def dist_norml_by_month(data: pd.DataFrame, columns=None):
    
    if columns is None:
        columns = data.columns[2:]
        
    # Converter a coluna de data para datetime
    data['Data'] = pd.to_datetime(data['Data'], format='%d/%m/%Y')
    
    # Extrair o mês da data
    data['Mês'] = data['Data'].dt.month_name()

    # Loop pelos meses únicos
    unique_months = data['Mês'].unique()
    for month in unique_months:
        month_data = data[data['Mês'] == month]

        # Selecionar colunas numéricas após as duas primeiras

        for column in columns:
            sns.histplot(month_data[column], stat="density", linewidth=0)
            mean = month_data[column].mean()
            std_dev = month_data[column].std()
            xmin, xmax = plt.xlim()
            x = np.linspace(xmin, xmax, 100)
            p = norm.pdf(x, mean, std_dev)
            plt.plot(x, p, 'k', linewidth=2)
            title = f"Distribuição Normal - {month}: {column}"
            plt.title(title)
            plt.xlabel(column)
            plt.ylabel('Densidade')
            plt.show()

def dist_norml_prd(data_standardized: pd.DataFrame, columns=None):
    if columns is None:
        columns = data_standardized.columns  # Seleciona todas as colunas numéricas

    for column in columns:
        sns.histplot(data_standardized[column], kde=True, stat="density", linewidth=0)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, 0, 1)  # Média 0 e desvio padrão 1 para distribuição normal padrão
        plt.plot(x, p, 'k', linewidth=2)
        title = f"Distribuição Normal Padronizada: {column}"
        plt.title(title)
        plt.xlabel(column)
        plt.ylabel('Densidade')
        plt.show()