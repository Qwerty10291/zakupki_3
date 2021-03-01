from lxml.html import document_fromstring
import requests

links = list(map(lambda x: x.replace('\n', ''), open('links copy.txt', 'r').readlines()))
tags = ['технологи', 'программ', 'информационн', 'телекоммуникационн']

def fz_44_handler(link):
    