import traceback
from glob import glob

import warc
import solr

from parse_drag import Parser

for fname in glob('../heritrix-3.2.0/jobs/PsuSecondFinalCrawl/20150420225655/warcs/*'):
    f = warc.open(fname)
    s = solr.SolrConnection('http://127.0.0.1:8203/solr/collection1')
    nix_list = ['css','js','png','jpg','gif','jpeg','ico']
    parser = Parser()

    while True:
        try:
            record = f.read_record()
        except IOError:
            continue
        if record:
            try:
                if record.type == 'response':
                    if "psu.edu" not in record.url:
                        continue
                    if True in [record.url.endswith(item) for item in nix_list]:
                        continue
                    try:
                        content = record.payload.read()
                        content = content[content.index('<html'):]
                        content = content.decode('ISO-8859-1')
                    except:
                        continue
                    print record.url
                    if "https" in record.url:
                        docs = parser.read_doc(content,url=record.url)
                        for doc in docs:
                            print doc['eventdate']
                            print doc['speaker']
                            print doc['location']
                            s.add(URL=record.url,**doc)
                            # s.commit()
            except Exception, IOError:
                print traceback.format_exc()
                pass
        else:
            break

