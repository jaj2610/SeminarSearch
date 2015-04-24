from datetime import date, timedelta, datetime
import re

import dateregex
from dragnet import content_extractor, content_comments_extractor
from bs4 import BeautifulSoup

class Parser(object):

    def __init__(self):
        self.reset_data()

    def find_info(self, s):
        # Times
        m = re.match(r'.*?(\d?\s*\d:\s*\d\s*\d\s*([pa]\s*\.?m\s*\.?)?).*', s, re.IGNORECASE)
        if m:
            self.potential_times.add(m.group(1).strip())

        # Locations
        m = re.match(r'.*(location|where)\s*[\-\:\@]?\s*(.*)', s, re.IGNORECASE)
        if m:
            self.potential_locs.add(m.group(2).strip())
        
        # Dates
        [self.potential_dates.add(date) for date in dateregex.get_dates(s)]

    def reset_data(self):
        self.seminar_texts = []
        self.potential_dates = set()
        self.potential_times = set()
        self.potential_locs = set()

    def read_doc(self, html):
        
        self.reset_data()

        # blocks = content_comments_extractor.analyze(html,blocks=True)
        blocks = BeautifulSoup(html).get_text().split('\n')
        blocks = filter(lambda x: x != '',[block.strip().encode('ascii','ignore') for block in blocks])
        [self.has_seminar(block) for block in blocks]
        if len(self.seminar_texts) > 0:
            [self.find_info(block) for block in blocks]
            print self.potential_times
            print self.potential_dates
            print self.potential_locs
            print "------"
            likelihood = min(len(self.seminar_texts), 2)
            if self.potential_times:
                likelihood += 1
            if self.potential_dates:
                likelihood += 1
            if self.potential_locs:
                likelihood += 3
            if likelihood >= 5:
                fixed_times = []
                for time in self.potential_times:
                    try:
                        fixed_times.append(
                            datetime.strptime(time.replace('.', '').strip().strftime('%H:%M:00.932Z'), '%I:%M %p'))
                    except:
                        try:
                            fixed_times.append(
                                datetime.strptime(time.replace('.', '').strip().strftime('%H:%M:00.932Z'), '%I:%M %p'))
                        except:
                            pass
                try:
                    etime = min(fixed_times)
                except:
                    etime = '00:00:00.032Z'
                try:
                    edate = max(self.potential_dates).strftime('%Y-%m-%dT') + ''
                except:
                    edate = date.today().strftime('%Y-%m-%dT')
                try:
                    title = "Title"
                except:
                    title = "Seminar"
                speaker = ""
                return {'eventdate':edate+etime,
                        'title':title,
                        'speaker':speaker,
                        'path':'',
                        # 'file_content':html,
                        'recordOffset':1                        
                        }
        return None

    def has_seminar(self,s):
        if re.match(r'.*(seminar)|(colloquium)|(forum)\s+.*', s, re.IGNORECASE):
            self.seminar_texts.append(s)
            return True
        return False



