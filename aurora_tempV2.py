import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.core.utils import ChromeType
from selenium_func import *
import logging



def get_num(temperatura):
    """Extrai o valor numérico de uma string e o converte em um número."""
    padrao = r"\d+\.?\d*"  # expressão regular para encontrar números
    temp_num = re.findall(padrao, temperatura)
    if len(temp_num) > 0:
        return float(temp_num[0])
    else:
        return None

def get_registros(navegador):
	
	aux,texto = get_text_xpath(navegador,'/html/body/div/av-frame/main/av-explorer/div/div[2]/av-plant-management-item/av-data-table[2]/div/div[2]/div/p')
	num_registros = int (get_num(texto))
	return num_registros

def mediana_temperaturas(temperaturas):

	temperaturas_ordenadas = sorted(temperaturas)

	meio = len(temperaturas_ordenadas) // 2

	if len(temperaturas_ordenadas) % 2 == 1:
		mediana = temperaturas_ordenadas[meio]

	else:
		mediana = (temperaturas_ordenadas[meio - 1] + temperaturas_ordenadas[meio]) / 2
	
	return mediana

def get_invs_temp(navegador):
	
	lista_user_medianas = []
	wait_time = 40
	# Espera até que a página seja completamente carregada totalmente
	wait = WebDriverWait(navegador, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
	time.sleep(5)
	ul_ui_width = navegador.find_element(By.XPATH,'/html/body/div/av-frame/main/av-explorer/div/div[1]/av-plant-management-tree/ul')
	wait_clickable_xpath(navegador,'/html/body/div/av-frame/main/av-explorer/div/div[1]/av-plant-management-tree/ul/li[1]/div/span[1]/button',20)
	
	list_user = ul_ui_width.find_elements(By.TAG_NAME,'li')
	num_user=1
	invs=list_user[0]
	mensagem_erro = 'NO SE HA ENCONTRADO NINGÚN DISPOSITIVO'
	list_temperaturas = []
	
	inversores = ul_ui_width.find_elements(By.TAG_NAME,'li')

	for li in list_user:
		wait_clickable_xpath(navegador,'/html/body/div/av-frame/main/av-explorer/div/div[1]/av-plant-management-tree/ul/li['+str(num_user)+']/div/span[1]/button',15)
		boll,nome_user = get_text_xpath(navegador,'/html/body/div/av-frame/main/av-explorer/div/div[1]/av-plant-management-tree/ul/li['+str(num_user)+']/div/span[2]')
		
		time.sleep(5)
		invs = li.find_element(By.CSS_SELECTOR,'ul.ui-list')
		inversores = invs.find_elements(By.TAG_NAME,'li')
		
		i = 1
		while i <= (len(inversores)):
			
			boll,name_inv = get_text_xpath(navegador,'/html/body/div/av-frame/main/av-explorer/div/div[1]/av-plant-management-tree/ul/li['+str(num_user)+']/ul/li['+str(i)+']/div/span[3]')
			
			if(name_inv != mensagem_erro):
				
				wait_clickable_xpath(navegador,'/html/body/div/av-frame/main/av-explorer/div/div[1]/av-plant-management-tree/ul/li['+str(num_user)+']/ul/li['+str(i)+']/div/span[3]',30)
				wait_clickable_xpath(navegador,'/html/body/div/av-frame/main/av-explorer/div/div[2]/av-plant-management-item/av-data-table[2]/div/div/button',30)
				num_registros = get_registros(navegador)

				for k in range(num_registros):
					wait_clickable_xpath(navegador,'/html/body/div/av-frame/main/av-explorer/div/div[2]/av-plant-management-item/av-data-table[2]/div/div[2]/table/tbody/tr['+str(k+2)+']/td[1]/button',30)
					time.sleep(5)
					quadro = navegador.find_element(By.XPATH,'/html/body/div/av-frame/main/av-explorer/div/div[2]/av-plant-management-item/div/av-explorer-device/table')
					elemento = WebDriverWait(quadro, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'TempInv')]")))
					proximo_elemento = elemento.find_element(By.XPATH, "following-sibling::*[1]")
					TempInv = proximo_elemento.text
					
					Temperatura = get_num(TempInv)
					
					list_temperaturas.append(Temperatura)
					wait_clickable_xpath(navegador,'/html/body/div/av-frame/main/av-explorer/div/div[2]/av-plant-management-item/av-data-table[2]/div/div[2]/table/tbody/tr['+str(k+2)+']/td[1]/button',30)
					time.sleep(5)
				wait_clickable_xpath(navegador,'/html/body/div/av-frame/main/av-explorer/div/div[2]/av-plant-management-item/av-data-table[2]/div/div/button',30)
			time.sleep(5)
			i+=1

		if(name_inv != mensagem_erro):
			mediana = mediana_temperaturas(list_temperaturas)
			list_temperaturas=[]
			lista_user_medianas.append([nome_user,mediana])
		else:
			lista_user_medianas.append([nome_user,0])
		    
		wait_clickable_xpath(navegador,'/html/body/div/av-frame/main/av-explorer/div/div[1]/av-plant-management-tree/ul/li['+str(num_user)+']/div/span[1]/button',30)
		time.sleep(5)
		num_user+=1

	return lista_user_medianas

def aurora_temp(url,login,password):

	# Abrindo e configurando o navegador onde a biblioteca selenium vai executar os comandos
	options = webdriver.ChromeOptions()
	options.add_argument("--start-maximized")
	options.add_argument('--log-level=3')
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	
	navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
	navegador.set_window_size(1080,1080)
	navegador.get(f'{url}')
	navegador.maximize_window()
	logging.basicConfig(level=logging.INFO)

	wait_time = 40
	# Espera até que a página seja completamente carregada totalmente
	wait = WebDriverWait(navegador, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
	wait_clickable_xpath(navegador,'/html/body/div[2]/div[3]',30)
	send_values_ID(navegador,"userId",login)
	send_values_ID(navegador,"password",password)
	wait_clickable_NAME(navegador,"login-btn",10)

	#lOOP para acessaar todos os usuários com alertas
	wait = WebDriverWait(navegador, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
	wait_clickable_xpath(navegador,'/html/body/av-navbar/header/div[1]/nav/div/av-navbar-item[2]/li/a',20)
	wait_clickable_xpath(navegador,'/html/body/av-navbar/header/div[1]/nav/div/av-navbar-item[2]/li/nav/ul/li[2]/a',20)
	wait = WebDriverWait(navegador, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
	user_info=[]
	lista_user_mediana = get_invs_temp(navegador)
	for user in lista_user_mediana:
		user_info.append({"dev_name":user[0],"dev_temp":user[1]})

	# print(user_info)

	return user_info
# print(aurora_temp(,,))