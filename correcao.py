import pandas as pd

# Tentar carregar o CSV ignorando erros
data = pd.read_csv('BAHIA_BELMONTE.csv', on_bad_lines='skip')

# Mostrar as primeiras linhas do DataFrame para verificar os dados
print(data.head())

# Contar o número de colunas em cada linha
with open('BAHIA_BELMONTE.csv', 'r') as file:
    lines = file.readlines()

column_counts = [len(line.split(',')) for line in lines]

# Mostrar a contagem de colunas para cada linha
for i, count in enumerate(column_counts):
    print(f"Linha {i+1}: {count} colunas")


# Identificar as linhas problemáticas
problematic_lines = [i for i, count in enumerate(column_counts) if count != 17]

# Remover as linhas problemáticas
with open('BAHIA_BELMONTE.csv', 'r') as file:
    lines = file.readlines()

cleaned_lines = [line for i, line in enumerate(lines) if i not in problematic_lines]

# Salvar o arquivo corrigido
with open('BAHIA_BELMONTE_clean.csv', 'w') as file:
    file.writelines(cleaned_lines)

# Carregar o CSV corrigido
data = pd.read_csv('BAHIA_BELMONTE_clean.csv')

# Mostrar as primeiras linhas do DataFrame para verificar os dados
print(data.head())
