from datetime import date, timedelta, datetime
import re

from dragnet import content_extractor, content_comments_extractor
from bs4 import BeautifulSoup

import dateregex
import timeregex


class Parser(object):

    def __init__(self):
        self.reset_data(full=True)

    def find_info(self, tag):
        score = 5
        for line in filter(None,tag.text.split('\n')):
            # print line
            modified = re.match(r'.*(modified|updated).*',line,re.IGNORECASE)
            if modified:
                score -= 1

            # Times
            [self.potential_times.add(time) for time in timeregex.get_times(line)]
           
            # Locations
            m = re.match(r'.*(location|where)\s*[\-\:\@]?\s*(.*)', line, re.IGNORECASE)
            if m:
                self.potential_locs.add(m.group(2).strip())
            
            # Dates
            for date in dateregex.get_dates(line):
                if tag.name in ['b','em','strong']:
                    score += 5
                self.potential_dates.add((date,score))

    def reset_data(self, full=False):
        self.seminar_texts = []
        self.potential_dates = set()
        self.potential_times = set()
        self.potential_locs = set()
        if full:
            self.docs = []

    def read_doc(self, html, sub_doc=False):
        """Read html and try to find a seminar(s)
            if sub_doc, this is a piece of a document and we don't want to keep recursing"""
        
        # blocks = content_comments_extractor.analyze(html,blocks=True)
        soup = BeautifulSoup(html)

        def is_leaf_and_has_text(tag):
            # if not tag.find_all(True,limit=1):
            for x in tag.stripped_strings:
                return True
            return False

        tags = soup.find_all(is_leaf_and_has_text)
        [self.has_seminar(tag.text) for tag in tags]

        if len(self.seminar_texts) > 0 and not sub_doc:
            self.reset_data(full=True)
            table_rows = soup.find_all('tr')
            for row in table_rows:
                self.read_doc(str(row),sub_doc=True)
            self.find_seminar(tags)

        if sub_doc:
            self.reset_data()
            self.find_seminar(tags)
            
        return self.docs

    def find_seminar(self,tags):
        [self.find_info(tag) for tag in tags]
        likelihood = 0
        if self.potential_times:
            likelihood += 1
        if self.potential_dates:
            likelihood += 1
        if likelihood >= 2:             
            try:
                etime = min(self.potential_times)
            except Exception as e:
                print e
                etime = datetime(1900,1,1,0,0)
            etime = etime.strftime('%H:%M:00.032Z')
            try:
                edate = max(self.potential_dates, key=lambda x: (x[1],x[0]))[0].strftime('%Y-%m-%dT') + ''
            except:
                edate = date.today().strftime('%Y-%m-%dT')
            try:
                title = "Title"
            except:
                title = "Seminar"
            speaker = ""
            self.docs.append({'eventdate':edate+etime,
                    'title':title,
                    'speaker':speaker,
                    'path':'',
                    # 'file_content':html,
                    'recordOffset':1                        
                    })

    def has_seminar(self,s):
        for line in s.split('\n'):
            if re.match(r'.*(seminar)|(colloquium)|(forum)\s+.*', line, re.IGNORECASE):
                self.seminar_texts.append(line)
                return True
        return False



