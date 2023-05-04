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


def fusion_alert(url,login,password):
     
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
    user_info = []
    wait_time = 40
    # Espera até que a página seja completamente carregada
    wait = WebDriverWait(navegador, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    
    send_values_xpath(navegador,'/html/body/div/div[2]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div[3]/input[1]',login)
    send_values_ID(navegador,'value',password)
    wait_clickable_xpath(navegador,'/html/body/div/div[2]/div[2]/div/div[3]/div[4]/div/div/span',30)

    wait_clickable_xpath(navegador,'/html/body/div[2]/div/div[2]/div/div/div[2]/span[5]/span',30)
    wait_clickable_xpath(navegador,'/html/body/div[2]/div/div[4]/div/div/div[1]/div/div/div[1]/div/section/div/a[2]/span[2]',30)
    time.sleep(30)
    return user_info
fusion_alert(,,)