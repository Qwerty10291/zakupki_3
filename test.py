import lxml.html
from lxml import etree
import re
doc = lxml.html.document_fromstring(open('test.html', 'r').read())
print(doc.xpath('//input')[0].text_content())
text = etree.tostring(doc.xpath('//input')[0], pretty_print=True, encoding='unicode')

name = re.findall(r'data\-name=\"(.*?)\sdata', text)
print(name[0])

print(''.join(map(lambda x: chr(int(x.replace('&#x', ''), 16)), name[0].split(';')[:-1])))