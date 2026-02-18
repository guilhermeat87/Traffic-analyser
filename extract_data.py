import pandas as pd
import numpy as np

def process_traffic_data(file_path):
    # Ler o arquivo pulando as linhas de cabeçalho iniciais se necessário, 
    # mas como a estrutura é irregular, vamos ler tudo e filtrar manualmente.
    df = pd.read_excel(file_path)
    
    results = []
    current_section = None
    current_direction = None
    
    # Mapeamento de colunas baseado na visualização anterior
    # Coluna 0: Interval Ending / Section Name / Direction
    # Coluna 1: Total Delay (min)
    # Coluna 2: Avg Delay (sec/veh)
    # Coluna 3: Stopped Time (mins)
    # Coluna 4: Avg Stopped Time (sec/veh)
    # Coluna 5: Number of Stops
    # Coluna 6: Avg # Stops (stops/veh)
    
    for index, row in df.iterrows():
        val0 = str(row[0]).strip()
        
        # Detectar se é uma linha de cabeçalho de seção (ex: NWB, SEB)
        if val0 in ['NWB', 'SEB', 'EB', 'WB']:
            current_section = val0
            continue
        
        # Detectar se é uma linha de direção (ex: Sentido Fortaleza)
        if 'Sentido' in val0:
            current_direction = val0
            continue
            
        # Detectar se é uma linha de dados (formato HH:MM:SS)
        if ':' in val0 and len(val0.split(':')) == 3:
            time_interval = val0
            try:
                data = {
                    'Section': current_section,
                    'Direction': current_direction,
                    'Time': time_interval,
                    'Total_Delay_min': row[1],
                    'Avg_Delay_sec_veh': row[2],
                    'Stopped_Time_min': row[3],
                    'Avg_Stopped_Time_sec_veh': row[4],
                    'Number_of_Stops': row[5],
                    'Avg_Stops_veh': row[6]
                }
                results.append(data)
            except:
                pass
                
        # Detectar linha de sumário
        if val0 == 'Summary':
            try:
                data = {
                    'Section': current_section,
                    'Direction': current_direction,
                    'Time': 'Summary',
                    'Total_Delay_min': row[1],
                    'Avg_Delay_sec_veh': row[2],
                    'Stopped_Time_min': row[3],
                    'Avg_Stopped_Time_sec_veh': row[4],
                    'Number_of_Stops': row[5],
                    'Avg_Stops_veh': row[6]
                }
                results.append(data)
            except:
                pass

    return pd.DataFrame(results)

file_path = '/home/ubuntu/upload/Cenário_semáforoEusébio_delay.xls'
df_results = process_traffic_data(file_path)
print(df_results.to_string())
df_results.to_csv('/home/ubuntu/processed_results.csv', index=False)
