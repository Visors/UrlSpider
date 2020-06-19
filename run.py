from BaiduSpider import BaiduSpider
import sys

def main(keyword):
    baidu_spider = BaiduSpider()
    baidu_spider.search(keyword)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('no keyword!')
        sys.exit(-1)
    else:
        main(sys.argv[1])