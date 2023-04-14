from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd 
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

navegador = webdriver.Chrome(options=options)
navegador.get('https://www.iso.org/obp/ui/en/')
wait = WebDriverWait(navegador, 10)

filtro_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "v-select-optiongroup-xmltype")))
standards_input = filtro_div.find_element(By.XPATH, "//label[text()='Standards']/preceding-sibling::input")
standards_input.click()


search_box = navegador.find_element(By.XPATH, '//*[@id="obpui-105541713"]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/input')
search_box.send_keys('')
search_box.send_keys(Keys.RETURN)
wait

wait.until(EC.presence_of_element_located((By.CLASS_NAME, "v-label-std-title")))

def acha_titulos():
    titulos = {}
    while True:
        time.sleep(60)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "v-label-std-title")))
        std_refs = navegador.find_elements(By.CLASS_NAME, "v-label-std-ref")
        std_titles = navegador.find_elements(By.CLASS_NAME, "v-label-std-title")
        for i in range(len(std_refs)):
            titulo = std_titles[i].text
            ref = std_refs[i].text
            titulos[ref] = titulo
        
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "v-label-std-title")))
            next_button = navegador.find_element(By.XPATH, "//div[@class='v-button v-widget i-paging v-button-i-paging last v-button-last']")
            if next_button.get_attribute("class") == "v-button v-widget i-paging v-button-i-paging last v-button-last v-disabled":
                break
            next_button.click()
            wait.until(EC.staleness_of(std_refs[-1]))
        except:
            break
            
    return titulos

titulos = acha_titulos()
print(titulos)

df = pd.DataFrame.from_dict(titulos, orient='index').reset_index().rename(columns={'index': 'chave', 0: 'descricao'})
df = df.explode('chave')
df = df.fillna('')
df[['ISO', 'VERSAO']] = df['chave'].str.split(':', expand=True)
df[['colunaex','IDIOMA']] = df['chave'].str.split('(', expand=True)
df['ISO'] = df['ISO'].str.split('(', n=1).str.get(0)
df['VERSAO'] = df['VERSAO'].str.split('(', n=1).str.get(0)
df['IDIOMA'] = df['IDIOMA'].str.split(')', n=1).str.get(0)
df = df.drop('chave', axis=1)
df = df.drop('colunaex', axis=1)
df
df.to_csv('iso_standards.csv', index=False, sep=";")