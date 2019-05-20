from selenium import webdriver
import re
browser = webdriver.Chrome()

browser.get('https://sobooks.cc/books/12580.html')
secret_key = browser.find_element_by_class_name('euc-y-i')
secret_key.send_keys('2019777')
browser.find_element_by_class_name('euc-y-s').click()

print(str(browser.find_element_by_class_name('e-secret').text)[-4:])





