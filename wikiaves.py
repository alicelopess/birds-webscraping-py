from pyclbr import Class
import time
from pkg_resources import BINARY_DIST
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip
import json

# 1. Abrir o navegador - Firefox
# Criar um serviço de ajuste do selenium no navegador
options = Options()

# Abrir navegador com webdriver
nav = webdriver.Firefox(options=options)

# 2. Definir variáveis
url = "https://www.wikiaves.com.br/buscaavancada.php"
#lista_municipios = ["Santarém",
#"Cananéia",
#"Joinville",
#"Teresópolis",
#"Manaus",
#"Brasília",
#"Boa Vista",
#"Cuiabá",
#"São Paulo",
#"Rio de Janeiro",
#"Belém",
#"Goiânia",
#"Florianópolis",
#"Belo Horizonte",
#"Campinas",
#"Ubatuba",
#"Salesópolis",
#"Peruíbe",
#"Chapada dos Guimarães",
#"Ilhéus",
#"Porto Seguro",
#"Angra dos Reis",
#"Foz do Iguaçu"]

# Lista Teste
lista_municipios = ["Pau dos Ferros", "Grossos", "Governador Dix-Sept Rosado"]

# 3. Realizar primeira pesquisa
for municipio in lista_municipios:
    # Abrir url com driver
    nav.get(url)
    time.sleep(3)

    # Pesquisar primeiro município 
    ## Identificar XPath do campo de pesquisa e selecionar elemento com click
    nav.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/div/div[1]/div/form/div[1]/div[7]/div/span").click()

    ## Escrever o nome do primeiro município usando send_keys
    pyperclip.copy(municipio)
    nav.find_element(By.XPATH, '//*[@id="cidade"]').send_keys(Keys.CONTROL+ 'v')
    time.sleep(1)

    # Enviar Pesquisa
    ## Clicar no Primeiro Estado Sugerido
    nav.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/div/div[1]/div/form/div[1]/div[7]/div/span/div/div/p[1]").click()

    ## Identificar Botão de buscar e clicar
    nav.find_element(By.XPATH, '//*[@id="buscar"]').click()
    time.sleep(3)

    # Coletar quantidade de registros do municipio
    quantidade_registros = nav.find_element(By.XPATH, '//*[@id="wa-registros-total"]').text

    # 4. Trazer os dados
    ## Scroll até o final da página para garantir que todos os registros serão coletados
    ### Determine o tamanho inicial da página
    last_height = nav.execute_script('return document.body.scrollHeight')
    print(last_height)
    while True:
        # Scroll até o final da página
        nav.execute_script('window.scrollTo(0, document.body.scrollHeight)')

        # Espere carregar
        time.sleep(4)

        # Compare o tamanho da página e redefina a variável
        new_height = nav.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            ## Double Check (carregamento lento)
            time.sleep(10)
            new_height = nav.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            else:
                last_height = new_height
        else:
            last_height = new_height

    time.sleep(5)
    print(last_height)

    ## Identificar os dados que eu quero coletar
    dados = nav.find_element(By.XPATH, '//*[@id="wa-record-grid"]')

    ## Atribuir HTML dos dados a uma variável
    html_dados = dados.get_attribute('outerHTML')

    ## Parsear o HTML
    parser_html_dados = BeautifulSoup(html_dados, 'html.parser')
    parser_html_dados.prettify()

    ## Encontrar cada registro dentro do HTML da página
    birds = parser_html_dados.find_all('div', class_ = 'wa-grid-item wa-record-mobile')

    # 5. Tratar os dados
    ## Definir uma lista que vai conter dicionários com os dados importantes de cada registro
    birds_list = []

    ## Iterar pela lista birds para extrair os dados importantes de cada registro
    for bird in birds:
        # Extrair href do registro
        main_div = bird.find('div', class_="m-portlet")
        a = main_div.find('a')
        a_href = a.get('href')

        # Extrair src da imagem do pássaro
        img = a.find('img')
        img_src = img.get('src')

        # Extrair o link do nome do pássaro
        ## Verificar se o link do nome do pássaro existe
        content_div = main_div.find('div', class_="m-portlet__body")
        sp_div = content_div.find('div', class_="sp")
        if sp_div.find('a', class_="m-link"):
            sp_a = sp_div.find('a', class_="m-link")
            bird_name_href= sp_a.get('href')
        else:
            bird_name_href= "N/A"

        # Extrair nome do pássaro
        # Extrair nome do pássaro - 'en'
        ## Verificar se o nome do pássaro existe
        if sp_div.findAll('a', class_="m-link"):
            bird_name_html = sp_div.findAll('a', class_="m-link")
            bird_name = []
            for a in bird_name_html:
                bird_name.append(a.text)
        else:
            bird_name = ["N/A", "N/A"]

        # Extrair nome do Autor
        author_div = content_div.find('div', class_="author")
        bird_author_html = author_div.findAll('a', class_="m-link")
        ## Verificar se o nome do autor existe
        if len(bird_author_html) == 1:
            ### O nome do município sempre vai existir
            bird_author = [bird_author_html.text, "N/A"]
        else:
            bird_author = []
            for a in bird_author_html:
                bird_author.append(a.text)
        
        # Extrair link do perfil do autor
        all_bird_author_href = author_div.findAll('a', class_="m-link")
        ## Verificar se o link do perfil do autor existe
        if len(all_bird_author_href) == 1:
            ### O link do nome do município sempre vai existir
            bird_author_href = [all_bird_author_href.get('href'), "N/A"]
        else:
            bird_author_href = []
            for a in all_bird_author_href:
                bird_author_href.append(a.get('href'))

        # Extrair data do registro
        ## Verificar se a data do registro existe
        if content_div.find('div', class_="date"):
            bird_date = content_div.find('div', class_="date").text
        else:
            bird_date = "N/A"

        # Transformar cada registro em um objeto com os dados importantes
        bird_data = {
            'm-portlet-href':'https://www.wikiaves.com.br' + a_href,
            'm-portlet-img-src': img_src,
            'sp-link':'https://www.wikiaves.com.br' +  bird_name_href,
            'sp-name': bird_name[0],
            'sp-name-en': bird_name[1],
            'city': bird_author[0],
            'author-name': bird_author[1],
            'city-link':'https://www.wikiaves.com.br' + bird_author_href[0],
            'author-profile-link':'https://www.wikiaves.com.br' + bird_author_href[1],
            'date': bird_date
        }

        # Passar cada objeto para a lista 
        birds_list.append(bird_data)
        
    ## Converter a lista em JSON
    json_string = json.dumps(birds_list, indent=4)

    ## Criar um arquivo JSON - Identificar por cidade
    with open(f'birds{"_".join(municipio.lower().split())}.json', 'w') as outfile:
        outfile.write(json_string)

    time.sleep(3)
    ## Transformar JSON em Planilha Excel - Identificar por cidade
    df_json = pd.read_json(f'birds{"_".join(municipio.lower().split())}.json')
    df_json.to_excel(f'birds{"_".join(municipio.lower().split())}.xlsx')

    ## Esperar e recomeçar
    time.sleep(2)

    print('✅ [Coleta finalizada] ' + municipio + ' com ' + str(len(birds)) + ' registros.')
