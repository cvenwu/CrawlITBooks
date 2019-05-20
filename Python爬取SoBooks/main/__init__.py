import requests
from bs4 import BeautifulSoup
import re
import threading

URL = "https://sobooks.cc"
navbar_links = []


def get_category_link(URL):
    """
    爬取导航栏各个分类下书籍的URL，并将其添加到一个列表中
    :param URL:
    :return:
    """
    data = requests.get(URL).text
    bs = BeautifulSoup(data)
    navbar_contents = bs.select('.menu-item')
    # 匹配URL的正则表达式
    pattern = '(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?'
    for navbar_content in navbar_contents:
        pattern = re.compile(pattern)
        navbar_link = pattern.search(str(navbar_content))
        navbar_links.append(navbar_link.group())
    return navbar_links


if __name__ == '__main__':
    urls = get_category_link(URL)
    for url in urls:
        print(url)