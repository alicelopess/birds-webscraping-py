import uteis
import constants
import time

# 1 - Definir Variáveis
## Arquivo constants.py

# 2 - Abrir o navegador - Firefox
uteis.open_nav()

# 3 - Realizar Primeira Pesquisa
for municipio in constants.municipios_teste:
    print('=' * 30)
    print(f'Iniciando Coleta de {municipio.upper()}...')

    # Definir uma lista que vai conter dicionários com os dados importantes de cada registro
    birds_list = []

    # Total de Registros por Municipio => total_registros
    total_registros = uteis.search(municipio)
    print(f'Total de Registros de {municipio}: {total_registros}')
    time.sleep(2)
    
    # Iniciando a Pesquisa, com filtro de período de tempo
    ## Pesquisar por ano -> Início do for anos
    for ano in constants.lista_anos:
        # Total de Registros por Municipio por Periodo de Tempo => total_registros_ano
        total_registros_ano = uteis.filter_search(ano)

        # 4 - Pegar Dados Gerais
        print('-' * 30)
        print(f'PERÍODO DE TEMPO: {ano}')

        if total_registros_ano == "#":
            total_registros_ano = 0
            print(f'Número total de registros: {total_registros_ano}')
        else:
            print(f'Número total de registros: {total_registros_ano}')
        
        ## Scroll na Página
        uteis.scroll()

        # 5 - Trazer Dados Gerais
        birds = uteis.bring_data()

        # 6 - Extrair Dados Importantes
        ## Iterar pela lista birds para extrair os dados importantes de cada registro
        for bird in birds:
            bird_data = uteis.extract_data(bird)
            # Passar cada objeto para a lista 
            birds_list.append(bird_data)
            time.sleep(2)

        ## Pesquisar por ano -> Fim do for anos
        print(f'Finalizei esse período de tempo: {ano}\nColetei essa quantidade de registros: {str(len(birds))}')
        print('-' * 30)

    # 7 - Gerar Planilha
    uteis.create_df(birds_list, municipio)

    if len(birds_list) == int(total_registros):
      print(f'✅ [Coleta finalizada]  {municipio.upper()} com {len(birds_list)} registros.')
    else:
        print(f'⚠️ [Coleta INCOMPLETA!]  {municipio.upper()} com {len(birds_list)} registros.\nFaltam {int(total_registros) - len(birds_list)} registros!')
    print('=' * 30)

    ## Esperar e recomeçar
    time.sleep(5)
