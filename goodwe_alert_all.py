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



def goodwe_alert_all(url,login,password):

	options = webdriver.ChromeOptions()
	options.add_argument("--start-maximized")
	options.add_argument('--log-level=3')
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	
	navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
	navegador.set_window_size(1080,1080)
	navegador.get(f'{url}')
	navegador.maximize_window()
	logging.basicConfig(level=logging.INFO)
	logging.info('Start of program')
	user_info = []
	wait_time = 40
	# Espera até que a página seja completamente carregada totalmente
	wait = WebDriverWait(navegador, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
	
	send_values_ID(navegador,'username',login)
	send_values_ID(navegador,'password',password)
	wait_clickable_xpath(navegador,'/html/body/div[2]/div[1]/div/div[1]/div/form/div[4]/input[1]',30)
	
	# wait = WebDriverWait(navegador, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
	wait_clickable_xpath(navegador,'/html/body/div[1]/ul/li[2]/a',30)
	
	wait_clickable_xpath(navegador,'/html/body/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/input',30)
	
	
	wait_clickable_xpath(navegador,'/html/body/div[6]/div[1]/div[1]/ul/li[3]/span',30)
	wait = WebDriverWait(navegador, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
	tag_body = navegador.find_element(By.TAG_NAME,'body')
	div_rumain = tag_body.find_element(By.CSS_SELECTOR,'div.runmaintenance')
	div_maintable = div_rumain.find_element(By.CSS_SELECTOR,'div.main-table')
	div_view = div_maintable.find_element(By.CSS_SELECTOR,'div.view-info')
	div_table = div_view.find_element(By.CSS_SELECTOR,'div.table-body.table-layout')
	div_paging = div_view.find_element(By.CSS_SELECTOR,'div.paging')
	div_gdw = div_paging.find_element(By.CSS_SELECTOR,'div.gdw-pager')
	list_paginas = div_gdw.find_elements(By.TAG_NAME,'a')
	quant_paginas = ((len(list_paginas)) - 2)
	lista_linhas = div_table.find_elements(By.TAG_NAME,'ul')
	i = 2	
	while i <= quant_paginas:
		
		tag_body = navegador.find_element(By.TAG_NAME,'body')	
		div_rumain = tag_body.find_element(By.CSS_SELECTOR,'div.runmaintenance')
		div_maintable = div_rumain.find_element(By.CSS_SELECTOR,'div.main-table')
		div_view = div_maintable.find_element(By.CSS_SELECTOR,'div.view-info')
		div_table = div_view.find_element(By.CSS_SELECTOR,'div.table-body.table-layout')
		lista_linhas = div_table.find_elements(By.TAG_NAME,'ul')

		for user in lista_linhas:
			user_colunas = user.find_elements(By.TAG_NAME,'li')
			dev_name = user_colunas[0]
			dev_info = user_colunas[1]
			dev_alert = user_colunas[3]
			user_info.append({"dev_alert":dev_alert.text,"dev_name":dev_name.text,"dev_info":dev_info.text.strip('\n')})
		
		wait_clickable_xpath(navegador,'/html/body/div[2]/div[2]/div[2]/div[4]/div/a['+str(i+1)+']',30)
		time.sleep(20)
		
		i+=1

	return user_info

goodwe_alert_all(,,)