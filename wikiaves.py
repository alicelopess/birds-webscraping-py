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
lista_municipios = ["Grossos"]
#NOTA: Deixei apenas SP para realizar teste

# 3. Realizar primeira pesquisa
# Abrir url com driver
nav.get(url)
time.sleep(3)
# Pesquisar primeiro município 
# Identificar XPath do campo de pesquisa e selecionar elemento com click
nav.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/div/div[1]/div/form/div[1]/div[7]/div/span").click()

# Escrever o nome do primeiro município usando send_keys
pyperclip.copy(lista_municipios[0])
nav.find_element(By.XPATH, '//*[@id="cidade"]').send_keys(Keys.CONTROL+ 'v')
time.sleep(1)

# Enviar Pesquisa
# Clicar no Primeiro Estado Sugerido
nav.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/div/div[1]/div/form/div[1]/div[7]/div/span/div/div/p[1]").click()

# Identificar Botão de buscar e clicar
nav.find_element(By.XPATH, '//*[@id="buscar"]').click()
time.sleep(2)

# 4. Trazer os dados
# Scroll até o final da página para garantir que todos os registros serão coletados
# Determine o tamanho inicial da página
last_height = nav.execute_script('return document.body.scrollHeight')
print(last_height)
while True:
    # Scroll até o final da página
    nav.execute_script('window.scrollTo(0, document.body.scrollHeight)')

    # Espere carregar
    time.sleep(2)

    # Compare o tamanho da página e redefina a variável
    new_height = nav.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    else:
        last_height = new_height

time.sleep(5)

# Identificar os dados que eu quero coletar
# Todos os registros
dados = nav.find_element(By.XPATH, '//*[@id="wa-record-grid"]')

# Atribuir HTML dos dados a uma variável
html_dados = dados.get_attribute('outerHTML')

# Parsear o HTML
parser_html_dados = BeautifulSoup(html_dados, 'html.parser')
parser_html_dados.prettify()

# Encontrar cada registro dentro do HTML
birds = parser_html_dados.find_all('div', class_ = 'wa-grid-item wa-record-mobile')
#NOTA: Birds é uma lista

birds_list = []
for bird in birds:
    # Extrair href do registro
    first_div = bird.find('div', class_="m-portlet")
    a = first_div.find('a')
    a_href = a.get('href')

  # Extrair src da imagem
    img = a.find('img')
    img_src = img.get('src')

    bird_data = {
        'm-portlet-href': a_href,
        'm-portlet-img-src': img_src
    }

    birds_list.append(bird_data)
    # Extrair nome do registro
    # Extrair segundo href
    # Extrair Segundo nome
    # Extrair Nome do Autor
    # Extrair link do perfil do autor
    # Extrair data do registro

# 5. Tratar os dados
# Converter birds em JSON

print(birds_list)