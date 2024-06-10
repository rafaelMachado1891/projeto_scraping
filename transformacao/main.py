# importando as ferramentas
import pandas as pd
import sqlite3
import datetime

# leitura do meu arquivo jsonl

df = pd.read_json('../../dados/dados.jsonl',lines=True)

# setar o pandas para mostrar todas as colunas
pd.options.display.max_columns = None

# adicionar coluna com o caminho da extração dos dados 

df['source'] = 'https://lista.mercadolivre.com.br/luminarias-arandelas-externas'

# adicionar coluna com a hora da extração 

df['data_coleta'] = pd.to_datetime(datetime.datetime.now())

# tratar tipos dos dados 

df['preco'] = df['preco'].fillna(0).astype(float)
df['preco'] = df['cents'].fillna(0).astype(float)

# tratamento da coluna reviews amount
df['reviews amount'] = df['reviews amount'].str.replace('[\(\)]','',regex=True)
df['reviews amount'] = df['reviews amount'].fillna(0).astype(int)

# tratamento da coluna loja
df['loja'] = df['loja'].fillna('nao_informado')

# ajustar a coluna preco e centavos 
df['price'] = df['preco'] + df['cents'] / 100

# excluir colunas preco e centavos
df.drop(columns=['preco','cents'])

# conectar no banco de dados

conn = sqlite3.connect('../../dados/banco.db')

# salvar arquivo no banco de dados

df.to_sql('base_dados', conn, if_exists='replace', index=False)

# fechar conexao 

conn.close()
print(df.head())