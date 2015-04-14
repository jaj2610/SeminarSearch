from datetime import date, timedelta, datetime
import re

import warc
from bs4 import BeautifulSoup
import dateutil.parser as dparser

seminar_count = []
potential_dates = set()
potential_times = set()
potential_locs = set()


def has_seminar(s):
    x = filter(None, s.encode('utf-8').split('\n'))
    if not x:
        return
    for line in x:
        if re.match(r'.*(seminar)|(colloquium)|(forum)\s+.*', line, re.IGNORECASE):
            seminar_count.append(line)
            return True
    return False


def find_options(s):
    s = s.encode('utf-8').strip()
    if s:
        if re.match(r'.*time.*', s, re.IGNORECASE):
            m = re.match(r'.*?(\d?\s*\d:\s*\d\s*\d\s*([pa]\s*\.?m\s*\.?)?).*', s, re.IGNORECASE)
            if m:
                potential_times.add(m.group(1).strip())
                return True

        m = re.match(r'.*(location|where)\s*[\-\:\@]\s*(.*)', s, re.IGNORECASE)
        if m:
            potential_locs.add(m.group(2).strip())
            return True
        try:
            parsed_date = dparser.parse(s, fuzzy=True, default=(date.today() - timedelta(1)))

            if parsed_date == (date.today() - timedelta(1)) or parsed_date <= (date.today() - timedelta(18000)):
                return False

            potential_dates.add(parsed_date)
            return True

        except Exception as e:
            return False

    return False

f = warc.open(
    "heritrix-3.2.0/jobs/PSUcrawlSuccessfully/20150227014701/warcs/WEB-20150227014710630-00000-47191~localhost.localdomain~8083.warc.gz")
s = solr.SolrConnection('http://127.0.0.1:8203/solr/collection1')
for record in f:
    if record.type == 'response':
        if "psu.edu" not in record.url:
            continue
        seminar_count = []
        soup = BeautifulSoup(record.payload.read())
        seminars = soup.find_all(text=has_seminar)
        if len(seminar_count) >= 1:
            potential_dates = set()
            potential_times = set()
            potential_locs = set()
            tags = soup.find_all(text=find_options)
            print "----------"
            likelihood = min(len(seminar_count), 2)
            if potential_times:
                likelihood += 1
            if potential_dates:
                likelihood += 1
            if potential_locs:
                likelihood += 3
            if likelihood >= 5:
                fixed_times = []
                for time in potential_times:
                    try:
                        fixed_times.append(
                            datetime.strptime(time.replace('.', '').strip().strftime('%H:%M:00.932Z'), '%I:%M %p'))
                    except:
                        try:
                            fixed_times.append(
                                datetime.strptime(time.replace('.', '').strip().strftime('%H:%M:00.932Z'), '%I:%M %p'))
                        except:
                            pass
                etime = min(fixed_times)
                if not etime:
                    etime = '00:00:00.032Z'
                edate = max(potential_dates).strftime('%Y-%m-%dT') + ''
                if not edate:
                    edate = date.today().strftime('%Y-%m-%dT')
                s.add(URL=record.url,
                      eventdate=edate+etime,
                      title=soup.title,
                      speaker='Bobert',
                      path='',
                      recordOffset=1,
                      file_content=str(soup))
                s.commit()
                print potential_times
                print potential_dates
                print potential_locs
                print record.url
