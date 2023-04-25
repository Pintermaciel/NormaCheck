from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import csv
import pandas as pd 
import time

'''options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')'''

navegador = webdriver.Chrome()      #options=options
navegador.get('https://www.iso.org/obp/ui/en/')
wait = WebDriverWait(navegador, 10)

filtro_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "v-select-optiongroup-xmltype")))
standards_input = filtro_div.find_element(By.XPATH, "//label[text()='Standards']/preceding-sibling::input")
standards_input.click()


search_box = navegador.find_element(By.XPATH, '//*[@id="obpui-105541713"]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/input')
search_box.send_keys('')
search_box.send_keys(Keys.RETURN)
time.sleep(60)

wait.until(EC.presence_of_element_located((By.CLASS_NAME, "v-label-std-title")))

def acha_titulos():
    titulos = {}
    page_count = 0
    count = 0
    
    while True:
        print('inicio do loop')
        try:
            time.sleep(30)
            wait = WebDriverWait(navegador, 30)
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "v-label-std-title")))
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "v-label-std-ref")))
        except:
            print("Exceção, verificar código")
            time.sleep(2)
            continue
        print('aguardando pagina')
        
        for i in range(3): # tenta encontrar os títulos até 3 vezes
            std_refs = navegador.find_elements(By.CLASS_NAME, "v-label-std-ref")
            std_titles = navegador.find_elements(By.CLASS_NAME, "v-label-std-title")
            if std_refs: # se os títulos forem encontrados, interrompe o loop
                break
            else:
                time.sleep(1) # espera 1 segundo antes de tentar novamente
            
        refs = [ref.text for ref in std_refs]
        titles = [title.text for title in std_titles]
        for i in range(len(refs)):
            titulos[refs[i]] = titles[i]
            count += 1
        if count % 10 == 0:
            page_count += 1
            print(f"Collected {count} titles from {page_count} pages")
        if page_count % 5 == 0:
            filename = f"{count}_stardards{page_count}_pages.csv"
            with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
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
                writer.writerow(['ISO', 'VERSAO', 'IDIOMA', 'descricao'])
                for row in df.itertuples(index=False, name=None):
                    writer.writerow(row)
                print(f"Saved {filename}")
                
                
        try:
            if page_count % 3 == 0:
                print("Espera 10 seguntos antes de continuar ...")
                time.sleep(10)
            next_button = navegador.find_element(By.XPATH, "//div[@class='v-button v-widget i-paging v-button-i-paging last v-button-last']")
            if next_button.get_attribute("class") == "v-button v-widget i-paging v-button-i-paging last v-button-last v-disabled":
                break
            next_button.click()
            print("Proxima Página")
            time.sleep(5)
            
        except StaleElementReferenceException:
            print("Elemento não encontrado, aguardando 1 segundo...")
            time.sleep(1)
            continue
        except:
            print("Excessão, verificar codigo")
            time.sleep(2)
            pass
            
    return titulos

titulos = acha_titulos()
print(titulos)

