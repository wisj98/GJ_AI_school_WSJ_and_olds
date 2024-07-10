from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.request
import os 

keyword = input("검색어 입력: ")
color = input("""색상 입력 - (red, orange, yellow, green, mint, etc...)
               """)
scroll = int(input("스크롤 횟수(1~10):"))

url = f"https://www.google.com/search?q={keyword}&sca_esv=951454d4e44807ae&hl=ko&udm=2&tbas=0&tbs=ic:specific,isc:{color}"
driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()

for _ in range(scroll):  # 5번 스크롤 예시, 필요에 따라 조정
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

images = driver.find_elements(By.CLASS_NAME, "YQ4gaf")
img_checked = []
for img in images:
    if int(img.get_attribute('height')) >= 50 and img.get_attribute('src') not in img_checked:
        img_checked.append(img.get_attribute('src'))

path = f"images/{keyword}"
if not os.path.isdir(path) :
    os.mkdir(path)

for index, link in enumerate(img_checked):
    urllib.request.urlretrieve(link, f'{path}/{index}.jpg')