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

def crawl_daily_tweets(keywords, start_date, days):
    from datetime import datetime, timedelta
 
    # 将关键词字符串分割成列表
    keyword_list = keywords.split(',')
 
    # 转换字符串日期为datetime对象
    start = datetime.strptime(start_date, "%Y-%m-%d")
 
    for keyword in keyword_list:
        for i in range(days):
            day = start + timedelta(days=i)
            # 对于每一天，构建一个网址
            day_str = day.strftime("%Y-%m-%d")  # 转换回字符串格式
            next_day_str = (day + timedelta(days=1)).strftime("%Y-%m-%d")
            # website_address = f"https://twitter.com/search?q={keyword.strip()}%20until%3A{next_day_str}%20since%3A{day_str}&src=typed_query"
 
            # 在这里调用你的爬取函数，传入构建的网址
            Accessing_web_pages(website_address,keyword)
 
def Accessing_web_pages(target_url,keyword):
    
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
    time.sleep(random.uniform(2, 4.5))
    # 重新加载或访问目标网页
    driver.get(target_url)
    time.sleep(random.uniform(2, 4.5))
     # 获取数据
    get_data(driver,keyword)
    # # 创建浏览器实例
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
 
    # # 导航到登录页面
    # driver.get("https://twitter.com/login")
 
    # # 等待足够的时间，以便手动登录
    # input("请登录后按Enter键继续...")
 
    # # 登录成功后，保存Cookies到一个变量
    # cookies = driver.get_cookies()
 
    # # 重用之前保存的Cookies
    # for cookie in cookies:
    #     driver.add_cookie(cookie)
 
    # # 使用带有之前Cookies的driver访问需要登录状态的页面
    # driver.get(target_url)
 
    # try:
    #     # 等待直到“接受Cookies”按钮出现
    #     accept_button = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'css-1qaijid') and contains(text(), 'Accept all cookies')]"))
    #     )
 
    #     # 点击页面同意cookies按钮
    #     accept_button.click()
    # except:
    #     pass
 
    # # 获取数据
    # get_data(driver,keyword)
 
def get_data(driver,keyword):
    import time
    import random
    from datetime import datetime
    # 数据库连接配置
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'tw',
        'charset': 'utf8mb4',
    }
 
    # 建立数据库连接
    mysql_db = pymysql.connect(**config)
 
    # 创建游标对象
    cursor = mysql_db.cursor()
 
    # 创建表的SQL语句（如果还没有创建）
    create_table_sql = """
                            CREATE TABLE IF NOT EXISTS tweets (
                                tweet_url VARCHAR(255) NOT NULL PRIMARY KEY,
                                username VARCHAR(100) NOT NULL,
                                tweet_content TEXT NOT NULL,
                                publish_date DATETIME,
                                comments INT DEFAULT 0,
                                retweets INT DEFAULT 0,
                                likes INT DEFAULT 0,
                                views INT DEFAULT 0,
                                get_time DATETIME NOT NULL,
                                keyword VARCHAR(100)
                            );
                            """
 
    # 执行创建表的SQL语句
    try:
        cursor.execute(create_table_sql)
        mysql_db.commit()
        print("Table created successfully.")
    except Exception as e:
        mysql_db.rollback()
        print(f"Failed to create table: {e}")
    finally:
        cursor.close()
 
    crawled_tweets_urls  = []
    # 初始化变量以跟踪滚动
    last_height = driver.execute_script("return document.body.scrollHeight")
    max_retries = 5  # 允许的最大重试次数
    retries = 0  # 当前重试次数
    while retries < max_retries:
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
 
                        #关键词
                        keyword = keyword
 
                        #爬取时间
                        get_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
                        # 抓取数据并存储到字典
                        tweet_data = {
                            "tweet_url": tweet_url,
                            "username": username,
                            "tweet_content": tweet_content,
                            "publish_date": publish_date,
                            "comments": comments if comments else "0",
                            "retweets": retweets if retweets else "0",
                            "likes": likes if likes else "0",
                            "views": views if views else "0",
                            "get_time": get_time,
                            "keyword": keyword
                        }
 
                        # 数据库连接配置
                        config = {
                            'host': 'localhost',
                            'user': 'root',
                            'password': 'root',
                            'database': 'tw',
                            'charset': 'utf8mb4',
                        }
                        
 
                        # 建立数据库连接
                        mysql_db = pymysql.connect(**config)
 
                        # 创建游标对象
                        cursor = mysql_db.cursor()
 
                        # 插入或更新数据的SQL语句模板
                        insert_or_update_sql = """
                        INSERT INTO tweets (
                            tweet_url, username, tweet_content, publish_date, 
                            comments, retweets, likes, views, get_time, keyword
                        ) VALUES (%(tweet_url)s, %(username)s, %(tweet_content)s, %(publish_date)s, 
                        %(comments)s, %(retweets)s, %(likes)s, %(views)s, %(get_time)s, %(keyword)s)
                        ON DUPLICATE KEY UPDATE 
                            username=VALUES(username), 
                            tweet_content=VALUES(tweet_content), 
                            publish_date=VALUES(publish_date), 
                            comments=VALUES(comments), 
                            retweets=VALUES(retweets), 
                            likes=VALUES(likes), 
                            views=VALUES(views), 
                            get_time=VALUES(get_time), 
                            keyword=VALUES(keyword);
                        """
 
                        # 执行插入或更新数据的SQL语句
                        try:
                            cursor.execute(insert_or_update_sql, tweet_data)
                            mysql_db.commit()
                            print("Data inserted or updated successfully.")
                        except Exception as e:
                            mysql_db.rollback()
                            print(f"Insert or update data error: {e}")
                        finally:
                            cursor.close()
 
                        print(
                            f"Tweet URL: {tweet_url}, Username: {username}, Tweet_content: {tweet_content}, Date: {publish_date}, Comments: {comments}, Retweets: {retweets}, Likes: {likes}, Views: {views}, Get_time: {get_time}, Keyword: {keyword}")
                        print('-----------')
                    except Exception as e:
                        print(f'提取信息时出错: {e}')
                else:
                    continue
            except Exception as e:
                print(f'提取信息时出错: {e}')
 
        # 检查页面滚动高度是否有变化
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            retries += 1
            print(f"第{retries}次重试...")
        else:
            last_height = new_height
            retries = 0  # 重置重试次数
            print("检测到新内容，继续爬取...")
 
    #input("已到达页面底部或重试次数已达上限，按Enter键继续...")
 
 
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
    crawl_daily_tweets("亚伦.布什内尔","2024-02-26",2)
