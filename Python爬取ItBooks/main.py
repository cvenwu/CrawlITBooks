import requests
import bs4
import xlwt


def data_write(file_path, datas):
    f = xlwt.Workbook(encoding='utf-8')
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)

    # 将数据写入第i行第j列
    i = 0
    for data in datas:
        sheet1.write(i, 0, data)
        i += 1
    f.save(file_path)


# 由于网站反爬虫，直接访问会返回403forbidden，所以设置头部浏览器代理
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                 '(KHTML, like Gecko) Chrome/34.0.1847.137 '
                  'Safari/537.36 LBBROWSER'
}

books_name = []
for i in range(1, 534):
    url = "https://itbook.download/?p=" + str(i) + "&tag=&search="
    resp = requests.get(url, headers=headers)
    respSoup = bs4.BeautifulSoup(resp.text)
    # print(resp.status_code)
    if resp.status_code == 200:
        print("--------------------开始爬取第%d页--------------------" % i)
        content_list = respSoup.select('.home-articles-title')
        for content in content_list:
            print(content.text)
            books_name.append(str(content.text))
        print("--------------------第%d页爬取结束--------------------" % i)
    else:
        print("--------------------爬取第%d页失败--------------------" % i)

data_write('./books.xls', books_name)

