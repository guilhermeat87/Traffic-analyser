import pandas as pd

file_path = '/home/ubuntu/upload/Cenário_semáforoEusébio_delay.xls'

# Tentar ler o arquivo. Como é um .xls antigo, pode precisar de xlrd.
# O Manus já tem pandas instalado.
try:
    df = pd.read_excel(file_path)
    print("Colunas encontradas:")
    print(df.columns.tolist())
    print("\nPrimeiras 10 linhas:")
    print(df.head(10))
    
    # Verificar se existem várias seções (NWB, SEB, etc)
    # Pelo CSV anterior, parece que os nomes das seções estão em colunas específicas
    # ou são linhas que quebram a tabela.
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
