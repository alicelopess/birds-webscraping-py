import constants
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import pyperclip
import json
import time

# Definir Navegador
## Criar um serviço de ajuste do selenium no navegador
options = Options()
## Abrir navegador com webdriver
nav = webdriver.Firefox(options=options)

#Função para Abrir Navegador
def open_nav():
  return nav

#Função para Realizar Pesquisa
def search(municipio):
  # Abrir url do site 
  nav.get(constants.url_wikiaves)
  time.sleep(2)

  # Identificar XPath do campo de pesquisa e selecionar elemento com click
  nav.find_element(By.XPATH, constants.campo_pesquisa).click()

  # Escrever o Nome do Município
  pyperclip.copy(municipio)
  nav.find_element(By.XPATH, constants.input_campo_pesquisa).send_keys(Keys.CONTROL+ 'v')
  time.sleep(1)

  # Selecionar Sugestão
  nav.find_element(By.XPATH, constants.sugestao_campo_pesquisa).click()
  time.sleep(1)

  # Enviar Pesquisa
  nav.find_element(By.XPATH, constants.send_btn).click()
  time.sleep(1)

  # Coletar Valor Total de Registros do Municipio
  return nav.find_element(By.XPATH, constants.xpath_total_registros).text

#Função para Filtrar Pesquisa de Municipios com MUITOS Registros
def filter_search(ano):
  # Abrir url do site 
  nav.get(constants.url_wikiaves)
  time.sleep(2)

  # Identificar XPath do campo de pesquisa e selecionar elemento com click
  nav.find_element(By.XPATH, constants.campo_pesquisa).click()

  # Escrever o Nome do Município
  pyperclip.copy(constants.municipios[0])
  nav.find_element(By.XPATH, constants.input_campo_pesquisa).send_keys(Keys.CONTROL+ 'v')
  time.sleep(2)

  # Selecionar Sugestão
  nav.find_element(By.XPATH, constants.sugestao_campo_pesquisa).click()
  time.sleep(1)

  # Selecionar Filtro
  # Ano de Início
  nav.find_element(By.XPATH, constants.campo_ano_start).click()
  pyperclip.copy(ano[0])
  nav.find_element(By.XPATH, constants.input_ano_start).send_keys(Keys.CONTROL+ 'v')
  time.sleep(1)

  # Ano de Fim
  nav.find_element(By.XPATH, constants.campo_ano_end).click()
  pyperclip.copy(ano[1])
  nav.find_element(By.XPATH, constants.input_ano_end).send_keys(Keys.CONTROL+ 'v')
  time.sleep(2)

  # Enviar Pesquisa
  nav.find_element(By.XPATH, constants.send_btn).click()

  # Coletar Valor Total de Registros do Municipio por Período de Tempo
  return nav.find_element(By.XPATH, constants.xpath_total_registros).text

#Função para Pegar Dados Gerais
def scroll():
  # Scroll até o final da página para garantir que todos os registros serão coletados
  ## Determine o tamanho inicial da página
  last_height = nav.execute_script('return document.body.scrollHeight')
  while True:
    # Scroll até o final da página
    nav.execute_script('window.scrollTo(0, document.body.scrollHeight)')

    # Espere carregar
    time.sleep(4)

    # Compare o tamanho da página e redefina a variável
    new_height = nav.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
      break
    else:
      last_height = new_height

#Função para Trazer Dados Gerais
def bring_data():
  #Dados Brutos
  dados = nav.find_element(By.XPATH, constants.xpath_dados)
  
  #Tratar Dados
  ## Atribuir HTML dos dados a uma variável
  html_dados = dados.get_attribute('outerHTML')

  ## Parsear o HTML
  parser_html_dados = BeautifulSoup(html_dados, 'html.parser')

  ## Encontrar html cada registro dentro do html dos dados e passar para uma lista
  birds = parser_html_dados.find_all('div', class_ = 'wa-grid-item wa-record-mobile')
  return birds

#Função para Extrair Dados Importantes
def extract_data(bird_html):
  # Extrair href do registro
  main_div = bird_html.find('div', class_="m-portlet")
  a = main_div.find('a')
  a_href = a.get('href')

  # Extrair src da imagem do registro
  img = a.find('img')
  img_src = img.get('src')

  # Definir uma variável para a div de conteúdo
  content_div = main_div.find('div', class_="m-portlet__body")

  # Extrair informações da espécie
  ## Extrair o link do nome da espécie
  ### Verificar se o link do nome da espécie existe
  try:
    sp_div = content_div.find('div', class_="sp")
    sp_a = sp_div.find('a', class_="m-link")
    bird_name_href= sp_a.get('href')
  except:
    bird_name_href= "N/A"

  ## Extrair nome da esécie
  ## Extrair nome da esécie - 'en'
  ### Verificar se o nome da espécie existe
  try:
    sp_div = content_div.find('div', class_="sp")
    bird_name_html = sp_div.findAll('a', class_="m-link")
    bird_name = []
    for a in bird_name_html:
      bird_name.append(a.text)
  except:
    bird_name = ["N/A", "N/A"]

  # Extrair informações do Autor
  ## Definir uma variável para a div de autor
  author_div = content_div.find('div', class_="author")

  ## Extrair nome do Autor
  bird_author_html = author_div.findAll('a', class_="m-link")
                
  bird_author = []
  for a in bird_author_html:
    bird_author.append(a.text)
                
  ## Extrair link do perfil do autor
  all_bird_author_href = author_div.findAll('a', class_="m-link")
                
  bird_author_href = []
  for a in all_bird_author_href:
    bird_author_href.append(a.get('href'))

  # Extrair data do registro
  bird_date = content_div.find('div', class_="date").text

  # Transformar cada registro em um objeto com os dados importantes
  bird_data = {
    'register-link':'https://www.wikiaves.com.br' + a_href,
    'register-img-src': img_src,
    'sp-link':'https://www.wikiaves.com.br' +  bird_name_href,
    'sp-name': bird_name[0],
    'sp-name-en': bird_name[1],
    'city': bird_author[0],
    'author-name': bird_author[1],
    'city-link':'https://www.wikiaves.com.br' + bird_author_href[0],
    'author-profile-link':'https://www.wikiaves.com.br' + bird_author_href[1],
    'register-date': bird_date
  }
    
  return bird_data

#Função para Transformar os Arquivos em Excel
def create_df(birds_list, municipio):
  ## Converter a lista em JSON
  json_string = json.dumps(birds_list, indent=4)

  ## Criar um arquivo JSON - Identificar por cidade
  with open(f'birds{"_".join(municipio.lower().split())}.json', 'w') as outfile:
    outfile.write(json_string)

  time.sleep(3)
  ## Transformar JSON em Planilha Excel - Identificar por cidade
  df_json = pd.read_json(f'birds{"_".join(municipio.lower().split())}.json')
  df_json.to_excel(f'birds{"_".join(municipio.lower().split())}.xlsx')