from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,csv,os
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

PastasAP = ''

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized') 
options.add_argument('--disable-popup-blocking')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver,timeout=10)
     
def Radisson():
    os.chdir(PastasAP)
    link = 'https://atlantica.letsbook.com.br/reserva/busca?hotel=117'      
    driver.get(link)
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,'#main-layout > div.q-page-container > div > div > main > article > div.lb-search.lb-bg-c5 > div.location-dates > div.location-dates-date-wrapper > div.lb-field.lb-search-field.location-dates--checkin > div.lb-field-content > label > div > div').click()
    time.sleep(3)
    dias = driver.find_elements(By.CLASS_NAME, "vc-day-content")

    dados = []

    for dia in dias:
        try:
            data = dia.get_attribute("aria-label")  
            preco_elem = dia.find_element(By.CLASS_NAME, "lb-text__caption-2")
            preco_raw = preco_elem.text.strip()
            preco = float(preco_raw.replace("R$", "").replace(".", "").replace(",", ".").strip())

            dados.append([ data,preco])
        except Exception as e:
            continue  
    
    with open('Tarifas_Radisson.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Dia','price'])
        writer.writerows(dados)
            
def Bugan():
    os.chdir(PastasAP)
    link = 'https://atlantica.letsbook.com.br/reserva/busca?hotel=22'      
    driver.get(link)
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,'#main-layout > div.q-page-container > div > div > main > article > div.lb-search.lb-bg-c5 > div.location-dates > div.location-dates-date-wrapper > div.lb-field.lb-search-field.location-dates--checkin > div.lb-field-content > label > div > div').click()
    time.sleep(3)
    dias = driver.find_elements(By.CLASS_NAME, "vc-day-content")

    dados = []

    for dia in dias:
        try:
            data = dia.get_attribute("aria-label")  
            preco_elem = dia.find_element(By.CLASS_NAME, "lb-text__caption-2")
            preco_raw = preco_elem.text.strip()

            preco = float(preco_raw.replace("R$", "").replace(".", "").replace(",", ".").strip())

            dados.append([ data,preco])
        except Exception as e:
            continue  # Pula dias sem preço ou que não estão ativos
    print(dados)
    
    with open('Tarifas_Bugan.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Dia','price'])
        writer.writerows(dados)

def Novo_hotel():
    try:
        link = 'https://www.booking.com/hotel/br/novotel-recife-marina.pt-br.html'
        driver.get(link)
        wait = WebDriverWait(driver, 10)
        time.sleep(4)
        try:
            botao_pessoas = driver.find_elements(By.CLASS_NAME, 'ab2c86b370')
            time.sleep(4)
            if botao_pessoas:
                botao_pessoas[0].click()
                
                try:
                    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'de576f5064')))
                    botao_retirar = driver.find_elements(By.CSS_SELECTOR, '#\:ri\: > div > div:nth-child(2) > div.e301a14002 > button.de576f5064.b46cd7aad7.e26a59bb37.c295306d66.c7a901b0e7.c857f39cb2')
                    if botao_retirar:
                        botao_retirar[0].click()
                        print("Botão de retirar crianças clicado")
                    else:
                        print("Botão de retirar crianças não encontrado, ignorando...")
                except TimeoutException:
                    print("Botão de retirar crianças não apareceu, ignorando...")
            else:
                print("Botão de pessoas não encontrado, ignorando...")


            botoes_pesquisa = driver.find_elements(By.CLASS_NAME, 'b769347817 a7e79c28d6')
            time.sleep(2)
            if len(botoes_pesquisa) >= 2:
                botoes_pesquisa[1].click()
                print("Segundo botão de pesquisa clicado")
            else:
                print("Segundo botão de pesquisa não encontrado, ignorando...")

        except Exception as e:
            print(f"Erro ao manipular adultos/crianças: {e}")

    except Exception as e:
        print(f"Erro ao tentar acessar o link: {e}")

        