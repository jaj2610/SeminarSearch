import dateutil.parser as dparser
from datetime import date, timedelta
import re

from bs4 import BeautifulSoup
from dragnet import content_extractor

seminar_count = 0
potential_dates = []
potential_times = []
potential_locs = []

def has_seminar(s):
    global seminar_count
    x = filter(None,s.encode('utf-8').split('\n'))
    if not x:
        return
    for line in x:
        if re.match(r'.*(seminar)|(colloquium)|(session).*',line,re.IGNORECASE):
            seminar_count += 1
            return True
    return False


def has_time(s):
    s = s.encode('utf-8').strip()
    if s:
        if re.match(r'.*time.*',s,re.IGNORECASE):
                m = re.match(r'.*?(\d?\s*\d:\s*\d\s*\d\s*([pa]\s*\.?m\s*\.?)?).*',s,re.IGNORECASE)
                if m:
                    potential_times.append(m.group(1).strip())
                    return True

        m = re.match(r'.*(location|where)\s*[\-\:\@]\s*(.*)',s,re.IGNORECASE)
        if m:
            potential_locs.append(m.group(2).strip())
            return True
        try:
            parsed_date = dparser.parse(s,fuzzy=True, default=(date.today() - timedelta(1)))
            
            if parsed_date == (date.today() - timedelta(1)):
                return False

            potential_dates.append(parsed_date)
            return True

        except Exception as e:
            return False

    return False

f = open('test.html')
# print f.read().encode('utf-8')
content = content_extractor.analyze(f.read().encode('utf-8'),blocks=True)
print [c.text for c in content]
# print content
# soup = BeautifulSoup(content)
# # print soup.get_text()
# seminars = soup.find_all(text=has_seminar)
# if seminar_count >= 1:
#     tags = soup.find_all(text=has_time)
#     print tags
#     print potential_times
#     print potential_dates
#     print potential_locs
