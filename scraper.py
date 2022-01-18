from selenium.webdriver.edge.service import Service
from selenium import webdriver

import time
import pandas as pd

s = Service(r'C:\Users\toxic\Downloads\chromedriver_win32\chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get("google.com")
page_title = driver.title
print(page_title)
