from functions.crawler_google import google_crawler
from functions.crawler_knowyourmeme import knowyourmeme
from functions.train_to_metadata import metadata_maker
from functions.image_modifier import analyze
from tensorflow.keras.optimizers import Adam


print("구글 크롤러: 1, 노우유어밈 크롤러: 2, images to metadata: 3, 이미지 분석: 4, 이미지 예측: 5")
choose = input("뭐할래?\n")

if choose == '1':
    google_crawler()
elif choose == '2':
    knowyourmeme()
elif choose == '3':
    metadata_maker()
elif choose == '4':
    analyze()
