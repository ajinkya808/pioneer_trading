import pandas as pd
import numpy as np
import xlrd
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
import time
import logging
import json
from bs4 import BeautifulSoup

class data_fetch:
    def __init__(self, operating_dir, chromeDriver_dir):
        
        op = webdriver.ChromeOptions()
        p = {"download.default_directory": operating_dir +
             "\\Data_Fetch", "safebrowsing.enabled": "false"}
        op.add_experimental_option("prefs", p)
        op.add_experimental_option("excludeSwitches", ["enable-automation"])
        op.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(executable_path=chromeDriver_dir, options=op)
        driver.implicitly_wait(3)
        
        driver.get("https://www.nseindia.com/option-chain")
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="equity_optionchain_select"]/option[4]').click()
        driver.implicitly_wait(20)
        #driver.find_element_by_xpath('//*[@id="downloadOCTable"]').click()
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        result = soup.find('table',{'class': 'common_table w-100'})
        table_rows = result.find_all('tr')
        
        l = []

        for tr in table_rows:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            l.append(row)
        
        equity_derivatives_table = pd.DataFrame(l)
        self.data=equity_derivatives_table
  
