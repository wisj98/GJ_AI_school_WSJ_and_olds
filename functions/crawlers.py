from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request
import os

def google_crawler():
    keyword = input("검색어 입력: ")
    folder = f"images\\{input("PATH 입력:")}"
    color = input("""색상 입력 - (red, orange, yellow, green, mint, etc...)
                """)
    scroll = int(input("스크롤 횟수(1~10):"))

    url = f"https://www.google.com/search?q={keyword}&sca_esv=951454d4e44807ae&hl=ko&udm=2&tbas=0&tbs=ic:specific,isc:{color}"
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

    for _ in range(scroll):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    images = driver.find_elements(By.CLASS_NAME, "YQ4gaf")
    img_checked = []
    for img in images:
        if int(img.get_attribute('height')) >= 50 and img.get_attribute('src') not in img_checked:
            img_checked.append(img.get_attribute('src'))

    path = f"images/{folder}"
    if not os.path.isdir(path) :
        os.mkdir(path)

    start = list(map(lambda x: int(x.split('.')[0]), os.listdir(path)))
    start.sort()
    print(start)
    start = start[-1] if len(start) != 0 else 0

    for index, link in enumerate(img_checked[:-3]):
        try: 
            time.sleep(0.5)
            urllib.request.urlretrieve(link, f'{path}/{start + index + 1}.jpg')
            print(f'{path}/{start + index + 1}.jpg DONE')
        except:
            print(f'{path}/{start + index + 1}.jpg FAIL')

def knowyourmeme():
    keyword = input("검색어 입력: ")
    folder = f"images\\{input("PATH 입력:")}"
    scroll = int(input("스크롤 횟수(횟수 당 10~20장):"))

    url = f"https://knowyourmeme.com/memes/{keyword}/photos"

    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

    for i in range(scroll):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        print(f"{i+1}/{scroll}")

    images = driver.find_elements('xpath', '//*[@loading="lazy"]')
    img_checked = []

    print(len(images))

    for img in images:
        if int(img.get_attribute('height')) >= 50 and img.get_attribute('src') not in img_checked:
            img_checked.append(img.get_attribute('src'))

    path = f"images/{folder}"
    if not os.path.isdir(path) :
        os.mkdir(path)

    start = list(map(lambda x: int(x.split('.')[0]), os.listdir(path)))
    start.sort()
    start = start[-1] if len(start) != 0 else 0
    print(f"Starts downloading from {start + 1}.jpg")

    for index, link in enumerate(img_checked[:-3]):
        try: 
            time.sleep(1)
            urllib.request.urlretrieve(link, f'{path}/{start + index + 1}.jpg')
            print(f'{path}/{start + index + 1}.jpg DONE')
        except:
            print(f'{path}/{start + index + 1}.jpg FAIL')
