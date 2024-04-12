# from selenium import webdriver


# driver = webdriver.Chrome()

# driver.get("http://selenium.dev")

# driver.quit()

import concurrent.futures  
import json  
from selenium import webdriver  
from selenium.common.exceptions import WebDriverException  
  
# 初始化WebDriver选项（如果需要的话）  
chrome_options = webdriver.ChromeOptions()  
# 例如，你可以设置无头模式（不显示浏览器窗口）  
chrome_options.add_argument("--headless")  
  
# 定义获取网页标题的函数  
def get_page_title(url):  
    try:  
        driver = webdriver.Chrome(options=chrome_options)  
        driver.get(url)  
        title = driver.title  
        driver.quit()  # 关闭WebDriver  
        return title  
    except WebDriverException as e:  
        print(f"Error occurred while getting title for URL {url}: {e}")  
        return None  
  
# 主函数  
def main():  
    # 加载包含URL的JSON文件  
    with open('urls.json', 'r') as f:  
        urls = json.load(f)  
      
    # 创建线程池，限制为5个线程  
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:  
        # 使用map函数将urls列表中的每个元素传递给get_page_title函数  
        # executor.map会异步地执行函数，并返回一个迭代器  
        future_to_url = {executor.submit(get_page_title, url): url for url in urls}  
          
        # 获取所有结果  
        results = []  
        for future in concurrent.futures.as_completed(future_to_url):  
            url = future_to_url[future]  
            try:  
                title = future.result()  
                results.append(title)  
            except Exception as exc:  
                print(f'generated an exception: {exc}')  
                results.append(None)  
      
    # 保存结果到文件  
    with open('titles.txt', 'w', encoding='utf-8') as f:  
        for title in results:  
            if title is not None:  
                f.write(f'{title}\n')  
      
    print("Titles saved to file.")  
  
if __name__ == "__main__":  
    main()
