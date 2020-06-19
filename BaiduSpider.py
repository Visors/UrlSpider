from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import queue
import time


class BaiduData:
    def __init__(self, title, link):
        self.title = title
        self.link = link


class BaiduSpider:
    # 类变量ChromeOption
    op = Options()
    op.add_argument('--headless')
    op.add_argument('--disable-gpu')
    op.add_argument('--no-sandbox')
    op.add_argument('log-level=3')

    # 加载错误报头
    load_fail = "Can't load this page!"

    def __init__(self):
        # 基本信息
        self.id_tot = 0  # 总结果数
        self.item_tot = 0  # 总有效结果数
        # webdriver
        # driver用于请求搜索界面
        self.driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=BaiduSpider.op)
        self.driver.set_page_load_timeout(10)
        # url_driver用于请求百度跳转链接获取真链接
        self.url_driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=self.op)
        self.url_driver.set_page_load_timeout(15)
        # 返回数据
        self.data = queue.Queue()

    def getTrueUrl(self, url):
        self.url_driver.maximize_window()
        try:
            self.url_driver.get(url)
        except:
            return self.load_fail
        return self.url_driver.current_url

    def getPageItem(self):
        time.sleep(2)
        list = self.driver.find_elements_by_class_name('c-container')
        self.id_tot += len(list)
        for i in list:
            title = i.find_element_by_tag_name('a').text
            print(title)
            fake_url = i.find_element_by_tag_name('a').get_attribute('href')
            print(fake_url)
            true_url = self.getTrueUrl(fake_url)
            print(true_url)
            if true_url == self.load_fail:
                continue
            else:
                self.data.put(BaiduData(title, true_url))
                self.item_tot += 1

    def flip(self):
        try:
            self.driver.find_element_by_link_text('下一页>').click()
        except:
            raise IndexError("There is no next page!")

    def getPageNum(self):
        list = self.driver.find_elements_by_xpath("//*[@class='pc']")
        for i in list:
            print(i)
        print(len(list))
        return min(len(list), 5)

    def search(self, keyword):
        self.driver.maximize_window()
        try:
            self.driver.get('https://www.baidu.com')
        except:
            self.driver.close()
            self.url_driver.close()
            raise ConnectionError(self.load_fail)

        # 模拟搜索
        self.driver.find_element_by_id('kw').send_keys(keyword)
        self.driver.find_element_by_id('su').click()

        # self.getPageItem()

        page_num = self.getPageNum()

        # for i in range(2, page_num + 1):
        #     self.flip()
        #     self.getPageItem()
        #
        # return self.data


if __name__ == '__main__':
    baidu_spider = BaiduSpider()
    data = baidu_spider.search('MacBook')
    while not data.empty():
        item = data.get()
        print(item.title)
        print(item.link)
