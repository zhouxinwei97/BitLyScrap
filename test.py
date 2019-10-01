from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import requests


# website urls
base_url = ["https://bit.ly/2oMFEAt+", "https://bit.ly/2mbPcUx+"]

for links in base_url:
    driver = webdriver.Chrome()
    driver.get(links)
    clicks_wrapper = driver.find_elements_by_xpath("/html/body/div/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/span[1]")[0]
    clicks =clicks_wrapper.text
    print(clicks)