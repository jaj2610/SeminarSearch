from bs4 import BeautifulSoup

import re



def has_seminar(s):
    x = filter(None,s.encode('utf-8').split('\n'))
    if not x:
        return
    for line in x:
        if re.match(r'.*(seminar)|(time)|(location)|(date).*',line,re.IGNORECASE):
            return True
    return False


def has_time(s):
    x = filter(None,s.encode('utf-8').split('\n'))
    if not x:
        return
    for line in x:
        if re.match(r'.*time.*',line,re.IGNORECASE):
            # print line
            return True

    return False

f = open('test.html')
# print f.read().encode('utf-8')
soup = BeautifulSoup(f.read().encode('utf-8'))
tags = soup.find_all(text=has_time)
print tags
tags = soup.find_all(text=has_seminar)
print tags
