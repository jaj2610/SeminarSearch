from datetime import date, timedelta, datetime
import re


from dragnet import content_extractor
from bs4 import BeautifulSoup
import requests

import dateregex
import timeregex
from get_entities import get_entities


class Parser(object):

    def __init__(self):
        self.reset_data(full=True)
        self.blacklist = ['script','link','style','head']

    def find_info(self, tag):
        score = 5
        for line in filter(None, tag.text.split('\n')):

            modified = re.match(r'.*(modified|updated).*', line, re.IGNORECASE)
            if modified:
                score -= 1

            # Times
            [self.times.add(time) for time in timeregex.get_times(line)]

            # Dates
            for date in dateregex.get_dates(line):
                if date==datetime(2015,9,1,0,0):
                    print line
                if tag.name in ['b', 'em', 'strong']:
                    score += 5
                if date not in self.all_dates:
                    self.all_dates.add(date)
                    self.dates.add((date, score))

    def reset_data(self, full=False):
        self.seminar_texts = []
        self.dates = set()
        self.times = set()
        self.people = []
        self.facilities = []
        if full:
            self.docs = []
            self.all_dates = set()

    def read_doc(self, html, sub_doc=False, url=None):
        """Read html and try to find a seminar(s)
            if sub_doc, this is a piece of a document and we don't want to keep recursing"""

        if url:
            if "https" in url:
                html = requests.get(url.replace('https','http')).content.decode('utf-8').encode('ascii','ignore')

        if not sub_doc:
            self.reset_data(full=True)

        # blocks = content_comments_extractor.analyze(html,blocks=True)
        soup = BeautifulSoup(html)

        try:
            self.title = soup.title.text.decode('utf-8').encode('ascii','ignore')
        except:
            self.title = "Title"
        def is_leaf_and_has_text(tag):
            for x in tag.stripped_strings:
                return True

            return False

        tags = soup.find_all(is_leaf_and_has_text)
        [tag.decompose() for tag in tags if tag.name in self.blacklist]
        [self.has_seminar(tag.text) for tag in tags]

        if len(self.seminar_texts) > 0 and not sub_doc:
            
            table_rows = soup.find_all('tr')
            for row in table_rows:
                self.read_doc(str(row), sub_doc=True)

            self.find_seminar(tags,html)

        if sub_doc:
            self.find_seminar(tags,html)

        return self.docs

    def find_seminar(self, tags, html):
        self.reset_data()
        [self.find_info(tag) for tag in tags]
        likelihood = 0
        if self.times:
            likelihood += 1
        if self.dates:
            likelihood += 1
        if likelihood >= 2:
            self.people, self.facilities = get_entities(html)
            try:
                etime = min(self.times)
            except Exception as e:
                print e
                etime = datetime(1900, 1, 1, 0, 0)
            etime = etime.strftime('%H:%M:00.032Z')
            try:
                edate = max(self.dates, key=lambda x: (x[1], x[0]))[0].strftime('%Y-%m-%dT') + ''
            except:
                edate = date.today().strftime('%Y-%m-%dT')
                
            if self.people:
                speaker = max(self.people, key=lambda x: float(x['relevance']))['text'].encode('ascii','ignore')
                likelihood += 1
            else:
                speaker = "Speaker"
            if self.facilities:
                location = max(self.facilities, key=lambda x: float(x['relevance']))['text'].encode('ascii','ignore')
                likelihood += 1
            else:
                location = "Location"

            summary = content_extractor.analyze(html).decode('utf-8').encode('ascii','ignore')

            if likelihood >= 2:
                self.docs.append({
                    'path': '',
                    'file_content':html,
                    'summary': summary,
                    'eventdate': edate + etime,
                    'title': self.title,
                    'speaker': speaker,
                    'location': location,
                    'recordOffset': 1
                })

    def has_seminar(self, s):
        for line in s.split('\n'):
            if re.match(r'.*(seminars?)|(colloquiums?)|(forums?)\s+.*', line, re.IGNORECASE):
                self.seminar_texts.append(line)
                return True
        return False
