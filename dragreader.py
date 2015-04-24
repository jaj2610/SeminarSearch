import traceback

import warc
import solr

from parse_drag import read_doc


f = warc.open(
    "heritrix-3.2.0/jobs/PsuFinalCrawl/20150413232041/warcs/WEB-20150413232119278-00000-16756~localhost.localdomain~8083.warc.gz")
s = solr.SolrConnection('http://127.0.0.1:8203/solr/collection1')
for record in f:
    try:
        if record.type == 'response':
            if "psu.edu" not in record.url:
                continue
            content = record.payload.read()
            content = content.decode('ISO-8859-1')
            s.add(URL=record.url,**read_doc(content))
            # s.commit()
            print "--------"
            print potential_times
            print potential_dates
            print potential_locs
            print record.url
    except Exception:
        print traceback.format_exc()
        pass

