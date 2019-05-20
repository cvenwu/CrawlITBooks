from selenium import webdriver
browser = webdriver.Chrome()

browser.get('https://sobooks.cc/books/12580.html')

print(browser.find_element_by_class_name('euc-y-s').tag_name)
