import solr

s = solr.SolrConnection('http://127.0.0.1:8203/solr/collection1')

doc = {'URL':'test'}

s.add(URL="testest",eventdate='2015-04-08T21:10:15.932Z',title='yeah',speaker='bob',path='asdf',recordOffset=1,file_content="awesome_html yeah!!!")
s.commit()
