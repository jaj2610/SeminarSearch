import traceback

import warc
import solr

from parse_drag import Parser

f = warc.open(
    "../heritrix-3.2.0/jobs/PsuFinalCrawl/20150413232041/warcs/WEB-20150413232119278-00000-16756~localhost.localdomain~8083.warc.gz")
s = solr.SolrConnection('http://127.0.0.1:8203/solr/collection1')
parser = Parser()
nix_list = ['css','js','png','jpg','gif','jpeg','ico']
for record in f:
    try:
        if record.type == 'response':
            if "psu.edu" not in record.url:
                continue
            if True in [record.url.endswith(item) for item in nix_list]:
                continue
            content = record.payload.read()
            content = content.decode('ISO-8859-1')
            print record.url
            doc = parser.read_doc(content)
            if doc:
                s.add(URL=record.url,**doc)

            # s.commit()
    except Exception:
        print traceback.format_exc()
        pass

