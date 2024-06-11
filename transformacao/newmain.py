# Importando as ferramentas
import pandas as pd
import sqlite3
import datetime
import json

# Função para ler JSON Lines
def read_jsonl(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        data = [json.loads(line) for line in lines]
    return pd.DataFrame(data)

# Leitura do meu arquivo jsonl
try:
    df = read_jsonl('../dados/dados.jsonl')
except Exception as e:
    print(f"Erro ao ler o arquivo JSON Lines: {e}")
    raise

# Setar o pandas para mostrar todas as colunas
pd.options.display.max_columns = None

# Adicionar coluna com o caminho da extração dos dados
df['source'] = 'https://lista.mercadolivre.com.br/luminarias-arandelas-externas'

# Adicionar coluna com a hora da extração
df['data_coleta'] = pd.to_datetime(datetime.datetime.now())

# Tratar tipos dos dados
df['preco'] = df['preco'].fillna(0).astype(float)
df['cents'] = df['cents'].fillna(0).astype(float)

# Tratamento da coluna reviews amount
df['reviews amount'] = df['reviews amount'].str.replace('[\(\)]', '', regex=True)
df['reviews amount'] = df['reviews amount'].fillna(0).astype(int)

# Tratamento da coluna loja
df['loja'] = df['loja'].fillna('nao_informado')

# Ajustar a coluna preco e centavos
df['price'] = df['preco'] + df['cents'] / 100

# Excluir colunas preco e centavos
df.drop(columns=['preco', 'cents'], inplace=True)

# Conectar no banco de dados
conn = sqlite3.connect('../dados/banco.db')

# Salvar arquivo no banco de dados
try:
    df.to_sql('base_dados', conn, if_exists='replace', index=False)
    print("Dados salvos no banco de dados com sucesso!")
except Exception as e:
    print(f"Erro ao salvar os dados no banco de dados: {e}")
    raise
finally:
    # Fechar conexão
    conn.close()

# Exibir as primeiras linhas do DataFrame
print(df.head())