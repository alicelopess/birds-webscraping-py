from datetime import date

# Variáveis do Site
## URL do site Wikiaves
url_wikiaves = "https://www.wikiaves.com.br/buscaavancada.php"

## Campo de Pesquisa
campo_pesquisa = "/html/body/div/div[1]/div/div[2]/div/div/div[1]/div/form/div[1]/div[7]/div/span"
input_campo_pesquisa = '//*[@id="cidade"]'
sugestao_campo_pesquisa = "/html/body/div/div[1]/div/div[2]/div/div/div[1]/div/form/div[1]/div[7]/div/span/div/div/p[1]"

## Botão Enviar
send_btn = '//*[@id="buscar"]'

## Filtro de Ano
campo_ano_start = '//*[@id="buscaform"]/div[1]/div[11]/div[1]'
input_ano_start = '//*[@id="dataInicioRegistro"]'

campo_ano_end = '//*[@id="buscaform"]/div[1]/div[11]/div[3]'
input_ano_end = '//*[@id="dataFimRegistro"]'

## Total de Registros por Municipio => total_registros
## Total de Registros por Municipio por Periodo de Tempo => total_registros_ano
xpath_total_registros = '//*[@id="wa-registros-total"]'

## HTML dos Registros
xpath_dados = '//*[@id="wa-record-grid"]'


# Variáveis do Projeto
## Lista de Municipios
##Municipios
#municipios = ["Santarém",
#"Belém",
#"Cananéia",
#"Joinville",
#"Teresópolis",
#"Manaus",
#"Brasília",
#"Boa Vista",
#"Cuiabá",
#"São Paulo",
#"Rio de Janeiro",
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

##Municipios Teste
municipios= ["Governador Dix-Sept Rosado"]

## Filtro por Periodo de Tempo
lista_anos = [["01/01/1900", "31/12/2010"], ["01/01/2011", "31/07/2011"], ["01/08/2011", "31/12/2011"], ["01/01/2012", "31/07/2012"], ["01/08/2012", "31/12/2012"], ["01/01/2013", "31/07/2013"], ["01/08/2013", "31/12/2013"], ["01/01/2014", "31/07/2014"], ["01/08/2014", "31/12/2014"], ["01/01/2015", "31/07/2015"], ["01/08/2015", "31/12/2015"], ["01/01/2016", "31/07/2016"], ["01/08/2016", "31/12/2016"], ["01/01/2017", "31/07/2017"], ["01/08/2017", "31/12/2017"], ["01/01/2018", "31/07/2018"], ["01/08/2018", "31/12/2018"], ["01/01/2019", "31/07/2019"], ["01/08/2019", "31/12/2019"], ["01/01/2020", "31/07/2020"], ["01/08/2020", "31/12/2020"], ["01/01/2021", "31/07/2021"], ["01/08/2021", "31/12/2021"], ["01/01/2022", "31/07/2022"], ["01/08/2022", "31/12/2022"], ["01/01/2023", "31/07/2023"], ["01/08/2023", f"{date.today().strftime('%D/%M/%Y')}"]]


