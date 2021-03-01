from os import link


links = list(map(lambda x: x.replace('\n', ''), open('links copy.txt', 'r').readlines()))
tags = ['технолог', 'информа']
for i in links:
    for tag in tags:
        print(i.format(tag))