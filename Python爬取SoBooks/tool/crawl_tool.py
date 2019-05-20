import requests
from bs4 import BeautifulSoup
import re

URL = "https://sobooks.cc"
VERIFY_KEY = '2019777'

def convert_to_beautifulsoup(data):
    """
    用于将传过来的data数据包装成BeautifulSoup对象
    :param data: 对应网页的html内容数据
    :return: 对应data的BeautifulSoup对象
    """
    bs = BeautifulSoup(data, "html.parser")
    return bs


def url_pattern():
    """
    匹配URL的正则表达式
    :return:
    """
    pattern = '(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?'
    pattern = re.compile(pattern)
    return pattern


def get_category_link(url):
    """
    爬取导航栏各个分类下的URL，并将其添加到一个列表中
    :param URL:
    :return:
    """
    navbar_links = []
    data = requests.get(url).text
    bs = convert_to_beautifulsoup(data)
    navbar_contents = bs.select('.menu-item')
    for navbar_content in navbar_contents:
        pattern = url_pattern()
        navbar_link = pattern.search(str(navbar_content))
        navbar_links.append(navbar_link.group())
    return navbar_links


def get_url_content(url):
    """
    返回url对应网页的内容，用于分析和提取有价值的内容
    :param url: 网页地址
    :return: url对应的网页html内容
    """
    return requests.get(url).text


def get_book_card_content(url, data):
    """
    得到每页书籍卡片的内容，从而为获取书籍作者名字和链接提供方便
    :param url: 网页的url地址
    :param data: url对应的网页内容
    :return:
    """
    books_perpage = convert_to_beautifulsoup(data).select('h3')
    return books_perpage


def get_url_book(url, data):
    """
    获得对应页面URL链接存放的每个书籍对应的URL
    :param url: 网页的url地址
    :param data: url对应的网页内容
    :return: 返回该URL所在页面的每个书籍对应的URL组成的列表
    """
    book_links = []
    # 通过h3标签查找每页书籍
    books_perpage = get_book_card_content(url, data)
    for book_content in books_perpage:
        pattern = url_pattern()
        # 获取每本书的链接
        book_link = pattern.search(str(book_content))
        book_links.append(book_link.group())
    return book_links


def has_next_page(url, data):
    """
    判断url对应的页面是否有 下一页
    :param url: 网页的url地址
    :param data: url对应的网页内容
    :return: 有下一页   返回下一页对应的URL地址
             没有下一页  返回False
    """
    bs = BeautifulSoup(data, "html.parser")
    next_page = bs.select('.next-page')
    if next_page:
        url_next_page = url_pattern().search(str(next_page))
        return url_next_page.group()
    else:
        return False


def get_url_books_name(url, data):
    """
      判断url对应的页面是否有 下一页
      :param url: 网页的url地址
      :param data: url对应的网页内容
      :return: 返回url对应网址的书籍名称组成的列表
    """
    books_name = []
    books_perpage = get_book_card_content(url, data)
    for book in books_perpage:
        book_name = book.select('a')[0].get('title')
        books_name.append(book_name)
    return books_name


def analy_url_page(url):
    """
    分析url对应的网址，包括如下几个方面
    1. 提取当前url所有书籍的链接
    2. 判断当前url是否有下一页，如果有重复上面步骤，
                            如果没有，继续从新的分类开始爬取，
                                    如果新的分类已经爬取完成，则爬取完成
    :param url: 网页的url地址
    :return: None
    """
    while url:
        url_html_content = get_url_content(url)
        url_links_page = get_url_book(url, url_html_content)
        url_next_page = has_next_page(url, url_html_content)
        books_name = get_url_books_name(url, url_html_content)
        print(has_next_page(url, url_html_content))
        print(url_links_page)
        print(books_name)
        url = url_next_page


def get_book_baidu_neturl(url):
    """
    获取每个书籍详情页面的百度网盘链接
    :param url: 每本书详情页面的URL
    :return: 返回每本书的百度网盘链接，如果没有返回 False
    """
    data = requests.get(url).text
    bs = convert_to_beautifulsoup(data)
    for a_links in bs.select('a'):
        if a_links.get_text() == '百度网盘':
            book_baidu_url = a_links.get('href')
    # 提取百度网盘链接的正则表达式
    pattern = '(http|ftp|https):\/\/pan\.[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?'
    pattern = re.compile(pattern)
    book_baidu_url = pattern.search(book_baidu_url).group()
    return book_baidu_url


def get_book_baidu_password(url):
    """
    获取对应url链接存储的书籍百度网盘的提取密码
    :param url: 要获取提取密码的url链接所对应的书籍
    :return: 如果存在返回提取密码
             否则返回False
    """
    """
    @TODO 1. 尝试使用爬虫的方式获取提交的页面来获得百度网盘提取码
          2. 如果不可以的话，就使用selenium模拟浏览器来爬取内容吧
    """
    pass




if __name__ == '__main__':
    # print(get_url_book("https://sobooks.cc/lishizhuanji"))
    # analy_url_page("https://sobooks.cc/lishizhuanji")

    get_book_baidu_neturl('https://sobooks.cc/books/12159.html')