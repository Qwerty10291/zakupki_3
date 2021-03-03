from os import link
from selenium import webdriver
import time
driver = webdriver.Chrome()
links = ''


names = list(map(lambda x: x.replace('\n', ''), open('name1.txt', 'r', encoding='utf-8').readlines()))
for i in names:
    try:
        driver.get('https://zakupki.gov.ru/epz/order/extendedsearch/search.html')
        driver.find_element_by_xpath('//*[@id="searchOptionsEditContainer"]/div/div[8]/div[1]/div').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@for="af"]').click()
        driver.find_element_by_xpath('//*[@for="ca"]').click()
        driver.find_element_by_xpath('//*[@for="pa"]').click()
        driver.find_element_by_id('customerAnchor').click()
        time.sleep(1)
        name_input = driver.find_element_by_id('customerInputDialog')
        name_input.send_keys(i)
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div[1]/div/div/div/div[1]/div[2]/div/div[1]/div/label').click()
        driver.find_element_by_xpath('//*[@id="modal-customer"]/div/div[4]/div/div/button[2]').click()
        driver.find_element_by_xpath('//*[@id="searchOptionsEditContainer"]/div/div[19]/div/div[3]/div/button').click()
        links += driver.current_url + '\n'
    except KeyboardInterrupt:
        exit()
    except:
        print(i)
    time.sleep(1)

print(links, file=open('links2.txt', 'w'))