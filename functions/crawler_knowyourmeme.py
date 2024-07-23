from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.request
import os 

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

    