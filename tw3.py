from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# from twitter.util import Standardization_time
# from twitter.util import Standardization_cout
import pymysql
import time
import random
from pymongo import MongoClient 
import os
import json
from datetime import datetime, timedelta
 
def Accessing_web_pages():
    
    # 创建一个ChromeOptions实例
    options = Options()
    # 设置为无头模式
    options.add_argument('--headless')
    # 创建浏览器实例
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # 首先访问Twitter的主页以设置域
    driver.get("https://twitter.com")
    
    # 添加Cookie到浏览器实例
    cookies = {

    }
    
    # 添加Cookie
    for key, value in cookies.items():
        cookie = {'name': key, 'value': value, 'domain': '.twitter.com'}
        driver.add_cookie(cookie)
    # time.sleep(random.uniform(2, 4.5))
    # 重新加载或访问目标网页

        # 获取当前工作目录
    current_directory = os.getcwd()

    # 构建user.json文件的完整路径
    userJson = os.path.join(current_directory, 'user.json')
    # 检查文件是否存在
    if os.path.exists(userJson):
        # 打开并读取JSON文件
        with open(userJson, 'r') as file:
            data = json.load(file)
        # print("JSON 文件内容：", data)
            for item in data:
                print(item);
                driver.get(item);
                get_data(driver);
    else:
        print("找不到 user.json 文件")
    
    # time.sleep(random.uniform(2, 4.5))
     # 获取数据
    
 
def get_data(driver):
    import time
    import random
    from datetime import datetime
    # 创建MongoDB客户端连接  
    client = MongoClient('mongodb://localhost:27017/')  
 
    # 选择数据库，如果不存在则会创建  
    db = client['twbase']  # 替换为你的数据库名  
 
    # 选择集合（表），如果不存在则会创建  
    collection = db['twlist']  # 替换为你的集合名
 
 
    crawled_tweets_urls  = []

    # while retries < max_retries:
    driver.execute_script("window.scrollBy(0, {});".format(random.randint(200, 800)))
    time.sleep(random.uniform(2, 4.5))

    # 这里设置最长等待时间为10秒
    article_content = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='cellInnerDiv']/div/div/article"))
    )
    for article in article_content:
        try:
            # 获取推文的网址
            tweet_url = article.find_element(By.XPATH, ".//time/..").get_attribute("href")

            if tweet_url not in crawled_tweets_urls:
                crawled_tweets_urls.append(tweet_url)
                try:
                    # 获取用户名
                    username = article.find_element(By.XPATH, ".//div[@data-testid='User-Name']//span").text
                    # 获取已置顶
                    top_name = article.find_element(By.XPATH, ".//div[@data-testid='socialContext']").text
                    
                    # 获取推文内容
                    tweet_content = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text

                    # 获取发布日期
                    publish_date = article.find_element(By.XPATH, ".//time").get_attribute('datetime')
                    publish_date = Standardization_time(publish_date)

                    # 获取评论数
                    comments = article.find_element(By.XPATH,
                                                    ".//div[@data-testid='reply']//span").text if article.find_elements(
                        By.XPATH, ".//div[@data-testid='reply']//span") else "0"
                    comments = Standardization_cout(comments)

                    # 获取转发数
                    retweets = article.find_element(By.XPATH,
                                                    ".//div[@data-testid='retweet']//span").text if article.find_elements(
                        By.XPATH, ".//div[@data-testid='retweet']//span") else "0"
                    retweets = Standardization_cout(retweets)

                    # 获取点赞数
                    likes = article.find_element(By.XPATH,
                                                ".//div[@data-testid='like']//span").text if article.find_elements(
                        By.XPATH, ".//div[@data-testid='like']//span") else "0"
                    likes = Standardization_cout(likes)

                    # 获取查看次数（如果可用）
                    views = article.find_element(By.XPATH,
                                                ".//a[contains(@href,'analytics')]//span").text if article.find_elements(
                        By.XPATH, ".//a[contains(@href,'analytics')]//span") else "0"
                    views = Standardization_cout(views)

                    #爬取时间
                    get_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # 获取今天的日期
                    t_date = datetime.strptime(get_time, "%Y-%m-%d %H:%M:%S").date()
                    p_date = datetime.strptime(publish_date, "%Y-%m-%d %H:%M:%S").date()
                    print("t_date", t_date, "---", p_date)
                    print("top_name", top_name)
                    print("tweet_content", tweet_content)
                    # if(top_name):
                    #     if t_date == p_date:
                    #         print("这条数据是今天发布的！")
                    #     else:
                    #         print("这条数据不是今天发布的。")
                    #         # break
                    # else:
                    #     print("非置顶内容")
                        # break
                    # 抓取数据并存储到字典
                    # tweet_data = {
                    #     "tweet_url": tweet_url,
                    #     "username": username,
                    #     "tweet_content": tweet_content,
                    #     "publish_date": publish_date,
                    #     "comments": comments if comments else "0",
                    #     "retweets": retweets if retweets else "0",
                    #     "likes": likes if likes else "0",
                    #     "views": views if views else "0",
                    #     "get_time": get_time
                    # }

                    # result = collection.insert_one(tweet_data)  
                    # print(f"Inserted document ID: {result.inserted_id}")  

                except Exception as e:
                    print(f'提取信息时出错: {e}')
            else:
                continue
        except Exception as e:
            print(f'提取信息时出错: {e}')
 
 
def Standardization_time(publish_date):
    # 将日期转换为标准格式
    from datetime import datetime, timedelta
 
    # 将字符串转换为datetime对象
    utc_dt = datetime.strptime(publish_date, "%Y-%m-%dT%H:%M:%S.%fZ")
 
    # 由于中国是UTC+8，我们将UTC时间加上8小时得到中国时间
    # 注意：这里简单地加上时差，如果需要考虑夏令时等复杂情况，使用pytz库会更准确
    china_dt = utc_dt + timedelta(hours=8)
 
    # 将日期格式化为所需格式
    formatted_date = china_dt.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date
 
def Standardization_cout(str):
    try:
        # 移除逗号
        views_str_cleaned = str.replace(',', '')
 
        # 将清理后的字符串转换为整数
        views_int = int(views_str_cleaned)
        return views_int
    except:
        pass

if __name__ == '__main__':
    Accessing_web_pages()
