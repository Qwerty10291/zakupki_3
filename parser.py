from lxml.html import document_fromstring
import requests
import re
import csv
import time

main_link = 'https://zakupki.gov.ru'
links = list(map(lambda x: x.replace('\n', ''), open('links1.txt', 'r').readlines()))
tags = ['технологи', 'программ', 'информационн', 'телекоммуникационн']

session = requests.Session()
session.headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}

csv_doc = csv.writer(open('out.csv', 'w'), delimiter=';', quotechar='"')

def fz_44_handler(link):
    main_data = session.get(link)
    main_data.raise_for_status()

    doc = document_fromstring(main_data.text)

    order_name = doc.xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/span[2]/text()')[0]
    customer_name = doc.xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/span[2]/a/text()')[0]
    custom_way = doc.xpath('/html/body/div[2]/div/div[2]/div/div/section[1]/span[2]/text()')[0]
    customer_adress = doc.xpath('/html/body/div[2]/div/div[3]/div/div/section[3]/span[2]/text()')[0]

    results_data = session.get(link.replace('common-info.html', 'supplier-results.html'))
    results_data.raise_for_status()

    doc = document_fromstring(results_data.text)

    table = doc.xpath('/html/body/div[2]/div/div[3]/div/div/section/div/table')
    if table:
        supplier = table[0].xpath('./tbody/tr[1]/td[3]/text()')[0]
        price = table[0].xpath('./tbody/tr[1]/td[4]/text()')[0]
        supplier_date = table[0].xpath('./tbody/tr[1]/td[5]/text()')[0]
    else:
        supplier = ''
        price = ''
        supplier_date = ''
    
    return ['фз 44', customer_name, order_name, custom_way, customer_adress,
            supplier, price, supplier_date]

def fz_223_handler(link):
    main_data = session.get(link)
    main_data.raise_for_status()
    doc = document_fromstring(main_data.text)

    order_name = doc.xpath('/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[2]/text()')[0]
    custom_way = doc.xpath('/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[2]/text()')[0]

    customer_data_container = doc.xpath('//div[@class="noticeTabBoxWrapper"]/table/tbody')
    customer_adress = ''
    customer_name = ''
    if customer_data_container:
        for con in customer_data_container[1].xpath('./tr'):
            if 'нахожден' in con.xpath('./td[1]')[0].text_content():
                customer_adress = con.xpath('./td[2]/text()')[0]
            if 'организ' in con.xpath('./td[1]')[0].text_content():
                customer_name = con.xpath('./td[2]/text()')[0]
    
    document_link = link.replace('common-info.html', 'contractInfo.html')
    doc_data = session.get(document_link)
    doc_data.raise_for_status()

    doc_doc = document_fromstring(doc_data.text)
    dogovor_container = doc_doc.xpath('//table[@id="contract"]/tbody/tr[1]/td[2]/a/@onclick')
    if dogovor_container:
        dogovor_link = re.findall(r'\'(.*?)\'', dogovor_container[0])[0]
        dogovor_data = session.get(dogovor_link.replace('general-information.html', 'subject-contract.html') + '&viewMode=FULL')
        dogovor_data.raise_for_status()
        print(dogovor_data.text)
        dogovor_doc = document_fromstring(dogovor_data.text)

        dogovor_info_container = dogovor_doc.xpath('//div[@class="noticeTabBoxWrapper"]')[0]

        dogovor_price = dogovor_info_container.xpath('./table//tr[1]/td[2]/text()')[0]
        dogovor_date = dogovor_info_container.xpath('./table//tr[5]/td[2]/text()')[0]

    else:
        dogovor_price = ''
        dogovor_date = ''
    
    return ['фз 223', customer_name, order_name, custom_way, customer_adress,
            '', dogovor_price, dogovor_date]

def normalizer(text):
    return re.sub(r'\s+', ' ', text.replace('\n', ''))

for link in links:
    for tag in tags:
        print(f'link: {link}, tag: {tag}')
        query = session.get(link.format(tag))
        query.raise_for_status()
        query_doc = document_fromstring(query.text)
        for i in query_doc.xpath('//div[@class="registry-entry__header-mid__number"]/a/@href'):
            if 'ea44' in i:
                data = fz_44_handler(main_link + i)
            elif '223' in i:
                data = fz_223_handler(i)
            print(list(map(normalizer, data)))
            csv_doc.writerow(map(normalizer, data))
            time.sleep(0.1)