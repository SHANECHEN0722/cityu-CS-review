from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import json
import time

# f12查看要爬取的数据是否是静态页面，发现点赞数和评分是动态加载的，所以不使用bs4，使用selenium
browser = webdriver.Chrome()
browser.get("https://www.imdb.com/title/tt0111161/reviews")
button = browser.find_element(By.CSS_SELECTOR, "button[class='ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-base ipc-btn--theme-base ipc-btn--button-radius ipc-btn--on-accent2 ipc-text-button ipc-see-more__button']")
browser.execute_script('arguments[0].scrollIntoView(false);', button)
time.sleep(1)
button.click()
StoreData = []
amount = 0
#JS 异步请求（Ajax），加载需要时间，而且 Selenium 默认不会等数据
time.sleep(3)
reviews = browser.find_elements(By.CSS_SELECTOR, "article.user-review-item")[:30]
for el in reviews:
    amount=amount+1
    username = el.find_element(By.CSS_SELECTOR, "a[data-testid='author-link']").text
    reviewdate = el.find_element(By.CSS_SELECTOR, "li[class='ipc-inline-list__item review-date']").text
    reviewtxt = el.find_element(By.CSS_SELECTOR, "h3[class='ipc-title__text ipc-title__text--reduced']").text
    reviewhelpfulcount = el.find_element(By.CSS_SELECTOR, "span[class='ipc-voting__label__count ipc-voting__label__count--up']").text
    reviewnonhelpfulcount = el.find_element(By.CSS_SELECTOR, "span[class='ipc-voting__label__count ipc-voting__label__count--down']").text
    rating = el.find_elements(By.CSS_SELECTOR, "span[class='ipc-rating-star--rating']")
    if rating:
        rating = rating[0].text + '/(10)'
    else:
        rating = el.find_element(By.CSS_SELECTOR, "h3[class='ipc-title__text ipc-title__text--reduced']").text

    StoreData.append({
        "Source": "IMDB",
        "UserName": username,
        "ReviweDate": reviewdate,
        "Reviewtext": reviewtxt,
        "Helpfulcount": reviewhelpfulcount,
        "Nonhelpfulcount": reviewnonhelpfulcount,
        "Rating": rating
        })

browser.quit()

# 保存文件
filename = 'reviewIMDB.csv'
df = pd.DataFrame(StoreData)
df.to_csv(filename, index=False)

StoreData.append({
        "Amount": amount
        })
        
with open("reviewIMDB.json",'w',encoding='utf-8') as json_file:
    json.dump(StoreData,json_file,indent = 4, ensure_ascii=False)
