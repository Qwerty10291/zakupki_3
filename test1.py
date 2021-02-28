import lxml.html
import lxml.etree
import requests
import re

names = list(map(lambda x: x.replace('\n', ''), open('name.txt', 'r').readlines()))
for name in names:
    data = requests.get(f'https://zakupki.gov.ru/epz/organization/chooseOrganization/chooseOrganizationTableModal.html?searchString={name}&inputId=customer&page=1&pageSize=10&organizationType=ALL&placeOfSearch=FZ_44,FZ_223&isBm25Search=true', headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'})
    try:
        doc = lxml.html.document_fromstring(data.text)
        print(doc.xpath('//input[1]/@*'))
    except:
        print(data.text)
        print(name)